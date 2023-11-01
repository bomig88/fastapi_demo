### FastAPI Demo Project

#### 1. import
- FastAPI
- Uvicorn

---

#### 2. run
- uvicorn main:app --reload --host=0.0.0.0 --port=8000
- 소스 코드상에서 바로 호출도 가능
```
import uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
---

#### 3. docs
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

---

#### 참고한 사이트 링크
- https://lucky516.tistory.com/109