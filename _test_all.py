"""全量接口测试脚本（整合后 9 个接口）"""
import sys
import io

# 强制 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import requests
import threading
import time
import uvicorn
from app.main import create_app

app = create_app()

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="error")

t = threading.Thread(target=run_server, daemon=True)
t.start()
time.sleep(4)  # 等待启动完成（假日数据首次需要从CDN拉取）

BASE = "http://127.0.0.1:8080"

tests = [
    ("健康检查", f"{BASE}/health", None),
    ("日期综合查询", f"{BASE}/public-china-holiday/date", {"params": {"date": "2025-10-01"}}),
    ("假日查询", f"{BASE}/public-china-holiday/holiday/query", {"params": {"date": "2025-10-01"}}),
    ("假日列表", f"{BASE}/public-china-holiday/holiday/list", {"params": {"year": 2025}}),
    ("工作日判断", f"{BASE}/public-china-holiday/workday", {"params": {"date": "2025-10-01"}}),
    ("工作日推算", f"{BASE}/public-china-holiday/workday/calculate", {"params": {"start_date": "2025-09-01", "workdays": 10}}),
    ("工作日计数", f"{BASE}/public-china-holiday/workday/calculate", {"params": {"start_date": "2025-10-01", "end_date": "2025-10-31"}}),
    ("节气列表", f"{BASE}/public-china-holiday/solar-term/list", {"params": {"year": 2025}}),
    ("节气当前", f"{BASE}/public-china-holiday/solar-term/current", {"params": {"date": "2025-10-01"}}),
    # -- 多语言测试
    ("英语-假日查询", f"{BASE}/public-china-holiday/holiday/query", {"params": {"date": "2025-10-01", "lang": "en"}}),
    ("日语-日期查询", f"{BASE}/public-china-holiday/date", {"params": {"date": "2025-10-01", "lang": "ja"}}),
    ("韩语-节气列表", f"{BASE}/public-china-holiday/solar-term/list", {"params": {"year": 2025, "lang": "ko"}}),
    ("越南语-工作日", f"{BASE}/public-china-holiday/workday", {"params": {"date": "2025-10-01", "lang": "vi"}}),
    ("西班牙语-假日列表", f"{BASE}/public-china-holiday/holiday/list", {"params": {"year": 2025, "lang": "es"}}),
    ("法语-日期查询", f"{BASE}/public-china-holiday/date", {"params": {"date": "2025-10-01", "lang": "fr"}}),
    ("德语-节气当前", f"{BASE}/public-china-holiday/solar-term/current", {"params": {"date": "2025-10-01", "lang": "de"}}),
    ("无效语言-校验", f"{BASE}/public-china-holiday/date", {"params": {"date": "2025-10-01", "lang": "xx"}}),
]

passed = 0
failed = 0
for name, url, kwargs in tests:
    try:
        r = requests.get(url, timeout=10, **(kwargs or {}))
        d = r.json()
        # "无效语言" 测试预期返回错误（400 或 422）
        if "无效语言" in name:
            if r.status_code in (400, 422):
                print(f"[PASS] {name} (预期错误, 实际{r.status_code})")
                passed += 1
            else:
                print(f"[FAIL] {name}: 预期错误状态码, 实际status={r.status_code}")
                failed += 1
        elif d.get("code") == 200 and d.get("data") is not None:
            print(f"[PASS] {name}")
            passed += 1
        else:
            print(f"[FAIL] {name}: code={d.get('code')}, message={d.get('message')}")
            failed += 1
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
        failed += 1

print(f"\n总计: {passed}/{passed + failed} 通过")
if failed > 0:
    sys.exit(1)
