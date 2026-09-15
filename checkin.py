import os
import requests
import sys

def main():
    cookie = os.environ.get("IKUUU_COOKIE")
    if not cookie:
        print("错误: 未配置 IKUUU_COOKIE 环境变量")
        sys.exit(1)

    base_url = "https://ikuuu.pw"
    checkin_url = f"{base_url}/user/checkin"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": base_url,
        "Referer": f"{base_url}/user",
        "Cookie": cookie
    }

    try:
        resp = requests.post(checkin_url, headers=headers, timeout=30)
        print(f"响应状态码: {resp.status_code}")
        print(f"响应内容: {resp.text}")
        resp.raise_for_status()
        
        if "已签到" in resp.text or "checkin" in resp.text.lower():
            print("签到成功或今日已签到")
        else:
            print("签到请求已发送，请检查响应内容")
            
    except Exception as e:
        print(f"签到失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
