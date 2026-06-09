#!/usr/bin/env python3
"""강의 영상에서 판서(손글씨/슬라이드) 프레임을 일정 간격으로 추출.

손글씨 판서는 자동자막보다 정확한 1차 소스다. 노트를 쓰기 전에 이 프레임들을 직접 읽어
정의·수식·강사가 던진 질문을 확인한다.

사용:  python extract_frames.py <video> [--every 360] [--start 0] [--out frames] [--scale 900]
       --every : 프레임 간격(초). 기본 360(6분). 판서가 빽빽하면 더 짧게.
       --start : 시작 지점(초). 인트로 잡담을 건너뛰려면 키운다.
       --scale : 가로 픽셀. 손글씨 가독성을 위해 900 권장.
파일명: f_<분4자리>m.png  (예: f_0072m.png = 72분 지점)
"""
import subprocess, sys, os, argparse

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("--every", type=int, default=360)
ap.add_argument("--start", type=int, default=0)
ap.add_argument("--out", default="frames")
ap.add_argument("--scale", type=int, default=900)
a = ap.parse_args()

dur = float(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=nw=1:nk=1", a.video]).decode().strip())

os.makedirs(a.out, exist_ok=True)
made, t = [], a.start
while t < dur:
    mm = int(t // 60)
    outp = os.path.join(a.out, f"f_{mm:04d}m.png")
    subprocess.run(["ffmpeg", "-y", "-ss", str(t), "-i", a.video,
                    "-frames:v", "1", "-vf", f"scale={a.scale}:-1", outp],
                   capture_output=True)
    if os.path.exists(outp):
        made.append(outp)
    t += a.every

print(f"duration={dur/60:.1f}min  extracted={len(made)} frames -> {a.out}/")
