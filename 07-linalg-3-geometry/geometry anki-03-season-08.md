# geometry anki-03-season-08

## 문제

### 1. 벡터의 크기(길이)와 두 벡터 사이의 각도는 무엇으로 정의되는가? (선형대수)

### 2. $\mathbb{R}^2$ 에서 $(1,0),(0,1)$ 이 서로 수직이고 각각 크기가 1이라고 말할 수 있는 근거는 무엇인가?

### 3. 내적을 $2\times2$ 행렬(계량 행렬)로 나타낼 때, 그 성분은 어떻게 정해지는가?

### 4. 표준내적(dot product)으로 두 벡터 $(a,b),(c,d)$ 의 내적과, 벡터 $(x,y)$ 의 크기는?

### 5. 다변수 미적분의 그레디언트 벡터 $\nabla f=\left(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_n}\right)$ 가 "그 자체로는 미분이 아니다"라고 말하는 이유는?

### 6. 내적을 항등행렬(표준내적)로 택한 기하학과, 다른 내적을 택한 기하학을 각각 무엇이라 부르는가?

## 해답

### 1. 벡터의 크기(길이)와 두 벡터 사이의 각도는 무엇으로 정의되는가? (선형대수)
- 둘 다 <b>내적(inner product)</b>으로 정의된다.<br>$\lVert v\rVert=\sqrt{\langle v,v\rangle}$, $\cos\theta=\dfrac{\langle u,v\rangle}{\lVert u\rVert\,\lVert v\rVert}$<br>분모·분자가 모두 내적이므로 크기·각도는 내적의 결과물이다. 내적을 선언하는 일이 곧 크기·각도를 정하는 일.

### 2. $\mathbb{R}^2$ 에서 $(1,0),(0,1)$ 이 서로 수직이고 각각 크기가 1이라고 말할 수 있는 근거는 무엇인가?
- 그렇게 정해야 할 절대적 당위는 없다. 그것은 <b>표준내적(dot product)을 $\mathbb{R}^2$ 에 줬다는 대전제</b> 아래에서만 성립한다.<br>다른 내적을 고르면 $(1,0)$ 의 크기가 2일 수도, $(1,0),(0,1)$ 의 사잇각이 $90^\circ$ 가 아닐 수도 있다.

### 3. 내적을 $2\times2$ 행렬(계량 행렬)로 나타낼 때, 그 성분은 어떻게 정해지는가?
- 표준기저의 내적값으로 정해진다.<br>$\langle (x_1,y_1),(x_2,y_2)\rangle = \begin{pmatrix} x_1 & y_1 \end{pmatrix}\begin{pmatrix} \langle e_1,e_1\rangle & \langle e_1,e_2\rangle \\ \langle e_2,e_1\rangle & \langle e_2,e_2\rangle \end{pmatrix}\begin{pmatrix} x_2 \\ y_2 \end{pmatrix}$<br>가운데 행렬을 항등행렬로 택하면 표준내적 $x_1x_2+y_1y_2$ 가 된다.

### 4. 표준내적(dot product)으로 두 벡터 $(a,b),(c,d)$ 의 내적과, 벡터 $(x,y)$ 의 크기는?
- $\langle (a,b),(c,d)\rangle = ac+bd$<br>$\lVert (x,y)\rVert = \sqrt{x^2+y^2}$<br>계량 행렬을 항등행렬 $\begin{pmatrix}1&0\\0&1\end{pmatrix}$ 로 택한 경우.

### 5. 다변수 미적분의 그레디언트 벡터 $\nabla f=\left(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_n}\right)$ 가 "그 자체로는 미분이 아니다"라고 말하는 이유는?
- 이 표현은 <b>유클리드 공간(표준내적)이라는 대전제</b>를 깔고 있기 때문이다.<br>$(1,0),(0,1)$ 이 수직이고 크기가 1일 때만 이 표현이 진짜 미분이다. 다른 내적을 쓰면 올바른 그레디언트(최급강하 방향)는 달라진다.

### 6. 내적을 항등행렬(표준내적)로 택한 기하학과, 다른 내적을 택한 기하학을 각각 무엇이라 부르는가?
- 표준내적 → <b>유클리드 기하학(Euclidean geometry)</b>.<br>다른 내적(다 프로덕트가 아닌 내적) → <b>비유클리드 기하학 / 리만 기하학(Riemannian geometry)</b>. 점마다 다른 내적을 줄 때 그 내적을 <b>리만 계량(Riemannian metric)</b> 이라 부른다.
