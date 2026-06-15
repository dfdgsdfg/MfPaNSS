# linear algebra anki-03-season-01

## 문제

### 1. 내적 행렬 $A=\begin{pmatrix}3&1\\1&3\end{pmatrix}$로 정의한 내적에서 $\langle(1,0),(1,0)\rangle$을 구하시오.

### 2. 내적 행렬 $A=\begin{pmatrix}3&1\\1&3\end{pmatrix}$에서 $\langle(1,0),(0,1)\rangle$을 구하시오.

### 3. 내적 행렬 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$에서 $(1,0)$과 $(0,1)$의 사잇각 $\theta$의 $\cos\theta$와 근삿값을 구하시오.

### 4. 내적을 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$로 바꾼 공간에서 $x^2+y^2=1$을 만족하는 점들을 모으면 어떤 모양인가? 그 이유는?

### 5. 벡터공간에는 길이와 각도가 처음부터 주어져 있는가? 언제 정해지는가?

### 6. 기저(basis)와 두 벡터 사이의 각도는 서로 관계가 있는가?

### 7. 대칭행렬(예: 내적 행렬 $\begin{pmatrix}a&b\\b&c\end{pmatrix}$)의 고유값과 고유벡터는 어떤 성질을 갖는가?

### 8. $2\times2$ 행렬 $M$에 대해 $M\mathbf{x}=\mathbf{0}$일 때, $\det M\neq 0$이면 해 $\mathbf{x}$는 무엇인가?

### 9. 고유벡터를 구할 때 왜 $\det(A-\lambda I)=0$이어야 하는지 모순 논법으로 설명하시오.

### 10. 내적 행렬 $A=\begin{pmatrix}3&1\\1&3\end{pmatrix}$의 고유값을 $\det(A-\lambda I)=0$으로 구하시오.

### 11. 내적 행렬 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$의 고유값 $\lambda=4,\ \lambda=2$에 대응하는 고유벡터를 각각 구하시오.

### 12. 내적 행렬 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$에서 두 고유벡터 $(1,1)$과 $(1,-1)$의 내적을 구하고 직교 여부를 판정하시오.

### 13. 내적 행렬 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$에서 $(1,0)$과 $(1,1)$은 직교하는가?

### 14. 내적 행렬 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$에서 고유벡터 $(1,1),(1,-1)$의 길이를 각각 구하시오.

### 15. $\mathbb{R}^2$에서 점을 $(x,y)$ 좌표로 쓰고 내적을 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$처럼 행렬로 쓰는 것은 무엇을 전제하고 있는가?

## 해답

### 1. 내적 행렬 $A=\begin{pmatrix}3&1\\1&3\end{pmatrix}$로 정의한 내적에서 $\langle(1,0),(1,0)\rangle$을 구하시오.
- $3$<br>$\begin{pmatrix}1&0\end{pmatrix}\begin{pmatrix}3&1\\1&3\end{pmatrix}\begin{pmatrix}1\\0\end{pmatrix}=3$. 따라서 $\|(1,0)\|=\sqrt3$.

### 2. 내적 행렬 $A=\begin{pmatrix}3&1\\1&3\end{pmatrix}$에서 $\langle(1,0),(0,1)\rangle$을 구하시오.
- $1$<br>$\begin{pmatrix}1&0\end{pmatrix}\begin{pmatrix}3&1\\1&3\end{pmatrix}\begin{pmatrix}0\\1\end{pmatrix}=1$. 표준 내적이라면 $0$(직교)인데, 이 내적에서는 $0$이 아니다.

### 3. 내적 행렬 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$에서 $(1,0)$과 $(0,1)$의 사잇각 $\theta$의 $\cos\theta$와 근삿값을 구하시오.
- $\cos\theta=\dfrac13 \approx 70.5^\circ$<br>$\cos\theta=\dfrac{\langle(1,0),(0,1)\rangle}{\|(1,0)\|\,\|(0,1)\|}=\dfrac{1}{\sqrt3\cdot\sqrt3}=\dfrac13$.

### 4. 내적을 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$로 바꾼 공간에서 $x^2+y^2=1$을 만족하는 점들을 모으면 어떤 모양인가? 그 이유는?
- 찌그러진 타원이 된다.<br>$x^2+y^2=1$을 만족하는 점들의 집합 자체는 같지만, 새 내적에서는 그 점들의 거리가 일정하지 않다. "$x^2+y^2$은 원점까지의 거리"라는 선입견을 버려야 한다.

### 5. 벡터공간에는 길이와 각도가 처음부터 주어져 있는가? 언제 정해지는가?
- 아니다. 벡터공간은 본래 집합 + 선형연산(덧셈·스칼라곱)일 뿐이며, 직선들의 위치·눈금(길이)·각도기는 주어져 있지 않다.<br>길이와 각도는 <b>내적을 줘야</b> 비로소 정의된다($\|v\|=\sqrt{\langle v,v\rangle}$, $\langle u,v\rangle=\|u\|\|v\|\cos\theta$).

### 6. 기저(basis)와 두 벡터 사이의 각도는 서로 관계가 있는가?
- 관계가 없다.<br>기저는 "그 벡터들을 선형결합해서 공간의 모든 원소를 만든다"까지를 뜻할 뿐이다. 사이의 각도·길이는 내적이 없으면 말할 수 없다. "$(1,0),(0,1)$이 기저다"와 "그 길이가 각각 $1$이고 직교한다"는 서로 다른 주장이다.

### 7. 대칭행렬(예: 내적 행렬 $\begin{pmatrix}a&b\\b&c\end{pmatrix}$)의 고유값과 고유벡터는 어떤 성질을 갖는가?
- 고유값은 모두 <b>실수</b>이고, 서로 다른 고유값에 대응하는 고유벡터는 서로 <b>직교</b>한다(직교는 표준 내적값이 $0$이라는 뜻).<br>내적 행렬은 항상 대칭행렬이므로 이 성질이 그대로 적용된다.

### 8. $2\times2$ 행렬 $M$에 대해 $M\mathbf{x}=\mathbf{0}$일 때, $\det M\neq 0$이면 해 $\mathbf{x}$는 무엇인가?
- $\mathbf{x}=\mathbf{0}$(영벡터)뿐이다.<br>$\det M\neq0$이면 역행렬 $M^{-1}$이 존재하므로 $\mathbf{x}=M^{-1}\mathbf{0}=\mathbf{0}$. 비자명한 해가 있으려면 $\det M=0$이어야 한다.

### 9. 고유벡터를 구할 때 왜 $\det(A-\lambda I)=0$이어야 하는지 모순 논법으로 설명하시오.
- 고유벡터는 $\mathbf{x}\neq\mathbf{0}$이어야 한다. $(A-\lambda I)\mathbf{x}=\mathbf{0}$에서 만약 $\det(A-\lambda I)\neq0$이면 역행렬이 존재해 $\mathbf{x}=\mathbf{0}$만 남아 모순이다.<br>따라서 비영벡터 해가 존재하려면 $\det(A-\lambda I)=0$이 강제된다.

### 10. 내적 행렬 $A=\begin{pmatrix}3&1\\1&3\end{pmatrix}$의 고유값을 $\det(A-\lambda I)=0$으로 구하시오.
- $\lambda=4,\ 2$<br>$\det\begin{pmatrix}3-\lambda&1\\1&3-\lambda\end{pmatrix}=(3-\lambda)^2-1=\lambda^2-6\lambda+8=0 \Rightarrow \lambda=4,2$.<br>※ 영상에서는 한때 고유값을 더듬어 말했으나 계산상 정확한 값은 $4$와 $2$이다.

### 11. 내적 행렬 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$의 고유값 $\lambda=4,\ \lambda=2$에 대응하는 고유벡터를 각각 구하시오.
- $\lambda=4$: $(1,1)$, $\lambda=2$: $(1,-1)$ (스칼라배 모두 가능)<br>$\lambda=4$: $(3-4)x+y=0\Rightarrow x=y$. $\lambda=2$: $(3-2)x+y=0\Rightarrow x=-y$.

### 12. 내적 행렬 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$에서 두 고유벡터 $(1,1)$과 $(1,-1)$의 내적을 구하고 직교 여부를 판정하시오.
- $\langle(1,1),(1,-1)\rangle=0$이므로 직교한다.<br>$\begin{pmatrix}1&1\end{pmatrix}\begin{pmatrix}3&1\\1&3\end{pmatrix}\begin{pmatrix}1\\-1\end{pmatrix}=0$. 대칭행렬의 고유벡터가 직교한다는 성질의 확인이다.

### 13. 내적 행렬 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$에서 $(1,0)$과 $(1,1)$은 직교하는가?
- 직교하지 않는다($\langle(1,0),(1,1)\rangle=4\neq0$).<br>$\begin{pmatrix}1&0\end{pmatrix}\begin{pmatrix}3&1\\1&3\end{pmatrix}\begin{pmatrix}1\\1\end{pmatrix}=4$. 새 내적에서는 $(1,0),(0,1)$을 기준으로 삼는 것이 의미가 떨어진다.

### 14. 내적 행렬 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$에서 고유벡터 $(1,1),(1,-1)$의 길이를 각각 구하시오.
- $\|(1,1)\|=\sqrt8=2\sqrt2,\quad \|(1,-1)\|=\sqrt4=2$<br>$\langle(1,1),(1,1)\rangle=8,\ \langle(1,-1),(1,-1)\rangle=4$. 두 길이가 달라서, 둘을 더하고 뺀 벡터는 다시 직교하지 않는다.

### 15. $\mathbb{R}^2$에서 점을 $(x,y)$ 좌표로 쓰고 내적을 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$처럼 행렬로 쓰는 것은 무엇을 전제하고 있는가?
- 표준기저 $(1,0),(0,1)$를 전제하고 있다.<br>좌표 표현과 행렬 표현 자체가 이미 표준기저를 깔고 있는 것이라, $(x,y)$ 앞에 행렬을 바로 곱해도 별도의 변환이 필요 없다(표준기저로 표현된 내적을 보고 있는 것).
