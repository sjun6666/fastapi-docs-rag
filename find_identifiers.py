#读 test_questions.json chunks.json
#写：data/regression_code.json
#预期 结果是30个
#预期120 实际 201
#预期生成 13 道题，expected_doc 互不相同
from ingest import load_data,save_data
import re
import os
import sys
def is_camel(name):
    return any(c.isupper() for c in name[1:]) and any(c.islower() for c in name)

tests = load_data("data/test_questions.json")
all_chunks = load_data("data/chunks.json")
ids={}
used_chunks=set()
for test in tests:
    used_chunks.add(test["expected_doc"])
for chunk in all_chunks:
    if chunk["doc_id"] in used_chunks:
        continue
    names = re.findall(r"`([A-Za-z_][A-Za-z0-9_.]*)`", chunk["text"])
    for i in names:
        if i not in ids:
            ids[i] = set()
        ids[i].add(chunk["doc_id"])
single=[]
for item in ids:
    if len(ids[item])== 1:
        if is_camel(item) or "_"in item:
            single.append(item)
results=sorted(single)

picked = ["HTTPBasicCredentials","HTTPSRedirectMiddleware","SecurityBase",
          "openapi_tags","FASTAPI_ENV","swagger_ui_parameters","app.swagger_ui_oauth2_redirect_url",
          "Jinja2Templates","HTTPBearer","openapi_extra","response_model_exclude_unset",
          "BackgroundTasks","default_response_class"]
ends = []
for name in picked:
    expected_doc = list(ids[name])[0]
    end = {
        "question":f"`{name}` 有什么作用？",
        "type":"代码名",
        "expected_doc":expected_doc,
        "identifier":name,
    }
    ends.append(end)
end_ex_id=set()
for item in ends:
    end_ex_id.add(item["expected_doc"])
assert len(ends) == 13
assert len(end_ex_id) == 13
if os.path.exists("data/regression_code.json"):
    print("data/regression_code.json 已存在，不覆盖")
    sys.exit(0)
save_data(ends,"data/regression_code.json")
