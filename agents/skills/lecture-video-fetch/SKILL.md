---
name: lecture-video-fetch
description: >-
  Download a YouTube lecture video (including channel members-only / 멤버십 전용
  content) together with its Korean auto-captions, then extract whiteboard /
  handwriting ("판서") frames so the lecture can be turned into notes. Use this
  whenever the user wants to download a lecture or membership video, grab a
  video's captions/transcript, or prepare a video's raw materials for
  note-taking — e.g. "이 강의 영상 받아줘", "유튜브 강의 다운로드", "자막이랑 판서 캡처 뽑아줘",
  "download this lecture and pull the transcript". Pairs with the
  `lecture-video-notes` skill, which writes the actual notes from what this
  produces.
---

# Lecture video fetch

This skill prepares the three raw materials needed to write good lecture notes from a YouTube video:

1. **the video file** (so the board can be read frame-by-frame),
2. **the Korean transcript** (cleaned auto-caption), and
3. **board frames** — periodic screenshots of the handwriting/slides.

Why all three: YouTube auto-captions for math/technical lectures are rough (terms get garbled), so the **handwritten board is the reliable primary source**. The transcript gives the spoken flow and timing; the frames give the actual definitions and formulas. The downstream `lecture-video-notes` skill needs both.

## Prerequisites (check once)

- `ffmpeg` / `ffprobe` — frame extraction. (`which ffmpeg`)
- `yt-dlp` — `python3 -m yt_dlp --version`; install with `python3 -m pip install -U yt-dlp` if missing.
- A JavaScript runtime (`deno` or `node`) — YouTube serves a JS "n-challenge"; yt-dlp solves it with the EJS solver downloaded via `--remote-components ejs:github`, which needs deno/node. (`which deno node`)

## Step 1 — Membership cookies (only for members-only videos)

Members-only videos need the cookies of a browser logged into the membership account. Public videos don't need cookies, but passing them is harmless.

Ask the user which browser holds the membership login, then use `--cookies-from-browser <browser>`.

- **Chrome** cookies live outside the macOS sandbox and usually read without extra permission.
- **Safari** cookies are TCC-protected: the terminal app must have **Full Disk Access** (System Settings → Privacy & Security → Full Disk Access), otherwise you get `Operation not permitted` on `Cookies.binarycookies`. If so, either grant access (may need an app relaunch) or fall back to logging into the membership account in Chrome.

Confirm access before the big download:

```bash
python3 -m yt_dlp --cookies-from-browser chrome --remote-components ejs:github \
  --extractor-args "youtube:player_client=web" --no-playlist --skip-download \
  --print "OK | %(title)s | %(channel)s | %(duration_string)s | %(availability)s" \
  "<VIDEO_URL>"
```

`availability=subscriber_only` ⇒ members-only (cookies required); `public` ⇒ open.
If you get *"Join this channel to get access…"*, the cookies aren't a member of that channel — fix the login/browser before continuing.

## Step 2 — Download the video

Two YouTube quirks drive the flags:

- The default player clients (e.g. `android vr`) **do not get membership access** — they fail with "Join this channel" even with valid cookies. Force a client that does: `web` works for access; `tv` additionally yields the 720p DASH stream **without a PO token**. The `web` client without a PO token can only reach the 360p progressive stream (format 18).
- So for best quality use the **`tv`** client and ask for 720p:

```bash
python3 -m yt_dlp \
  --cookies-from-browser <browser> --remote-components ejs:github \
  --extractor-args "youtube:player_client=tv" --no-playlist \
  -f "136+140/bestvideo[height<=720]+bestaudio/best[height<=720]" \
  --merge-output-format mp4 --no-mtime \
  -o "<OUT_DIR>/%(title)s [%(id)s].%(ext)s" \
  "<VIDEO_URL>"
```

If `tv` fails, fall back to `--extractor-args "youtube:player_client=web"` (expect 360p). Always verify the result — yt-dlp can exit 0 yet have downloaded nothing if a client was silently blocked:

```bash
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height \
  -of default=nw=1 "<OUT_DIR>/<file>.mp4" | head
```

360p handwriting is usually legible, but 720p is noticeably clearer for dense boards — prefer 720p when available.

## Step 3 — Korean auto-captions

The `web`/`mweb` clients require a subtitles **PO token** that we don't have, so they silently yield no subs. The **`tv`** (or `tv_embedded`/`web_embedded`) client returns the Korean auto-caption without one:

```bash
python3 -m yt_dlp \
  --cookies-from-browser <browser> --remote-components ejs:github \
  --extractor-args "youtube:player_client=tv" --no-playlist --skip-download \
  --write-auto-sub --sub-lang ko --sub-format vtt \
  -o "<OUT_DIR>/%(title)s [%(id)s].%(ext)s" "<VIDEO_URL>"
```

Then clean the rolling/duplicated VTT into usable text:

```bash
python3 "<skill_dir>/scripts/clean_vtt.py" "<OUT_DIR>/<id>.ko.vtt"
# -> <OUT_DIR>/<id>.transcript_clean.txt (plain) and <id>.transcript_timed.txt (with [HH:MM:SS])
```

Outputs are named after the video id (`<id>.transcript_*.txt`) so several videos can share one season folder without clobbering each other. `<id>.transcript_timed.txt` is the more useful one downstream — it lets the notes skill anchor sections to timestamps.

## Step 4 — Extract board frames

Read the handwriting, not just the audio. Pull a frame every few minutes:

```bash
python3 "<skill_dir>/scripts/extract_frames.py" "<OUT_DIR>/<file>.mp4" --every 360 --out "<OUT_DIR>/frames"
```

`--every 360` (6 min) is a good default for a 2–2.5h lecture (~25 frames). Use a smaller interval for dense boards. The notes skill reads these images directly.

## Step 5 — Report what's ready

Tell the user the output directory and list: video file, `transcript_clean.txt` / `transcript_timed.txt`, and `frames/`. Note the membership status and quality (e.g. "720p, 멤버십"). Hand off to `lecture-video-notes`.

## Output location — place into the repo structure (default)

This project organizes lectures into 17 unit folders (`NN-<slug>/`), and keeps each lecture's recording materials in a **gitignored per-lecture subfolder** `0K-season/<LL>/` (K = 기/cohort, LL = 강 번호). Download there by default so the media sits with the right unit·lecture and stays out of git.

Work out the target **before** downloading:

- **Season `0K-season`** — from the title's "N기": `…수학교실 2기]` → `02-season`; no "기" marker means 1기 → `01-season`; "뉴진수"/3기 → `03-season`; "4기" → `04-season`.
- **Unit `NN-…`** — map the lecture to one of the 17 units. The repo's root `index.md` / `README.md` already list every video against its unit and 기, so look the video up there (by id or title) and use that unit folder. For a brand-new lecture, pick the unit whose topic matches and tell the user.
- **Lecture `<LL>`** — the 강 번호 from the title (e.g. `…4기] 19.` → `19`); the same number used in the note/asset naming.

Then point the download/caption commands at `<repo>/<NN-unit>/<0K>-season/<LL>/` — e.g. the 4기 19강 geometry lecture lands in `07-linalg-3-geometry/04-season/19/`. (If you're not inside this repo structure, fall back to a clear working folder and say where things landed.)

## Notes & gotchas

- `--remote-components ejs:github` is recommended over `ejs:npm`; without it the n-challenge fails and formats go missing.
- yt-dlp picks clients on its own for downloads; if a download mysteriously becomes "members-only" again, re-pin `player_client` explicitly.
- These videos may be membership content — treat downloads as the user's personal, authorized copies and don't redistribute.
