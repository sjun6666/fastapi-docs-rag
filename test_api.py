#读：无
#写：logs/app.log
#预期 预期 400 422 502 522实际r1：422  r2 400 r 502  r3：500#修复后 r3为503
import requests
from fastapi.testclient import TestClient
import api

client = TestClient(api.app, raise_server_exceptions=False)         # 不用启动服务，直接在代码里发请求

def fake_fail(*args, **kwargs):       # 替身：不管传什么参数，都直接抛异常
    raise RuntimeError("模拟 DeepSeek 失败")
def fake_fail2(*args, **kwargs):
    raise requests.HTTPError("401")
api.answer = fake_fail                # 把 api 里用的 answer 换成替身
r = client.post("/ask", json={"question": "怎么声明路径参数"})
r1 = client.post("/ask", json={})
r2= client.post("/ask", json={"question":" "})
api.answer = fake_fail2
r3 = client.post("/ask", json={"question": "怎么声明路径参数"})
assert r.status_code == 502
assert r1.status_code == 422
assert r2.status_code == 400
assert r3.status_code == 502