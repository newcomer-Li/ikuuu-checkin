import os
import requests
import sys


def main():
    # 1. 从环境变量获取 Cookie
    cookie = os.environ.get("IKUUU_COOKIE")
    if not cookie:
        print("错误: 未配置 IKUUU_COOKIE 环境变量")
        sys.exit(1)

    # 2. 清理首尾空格和换行符（防止粘贴时带入非法字符）
    cookie = cookie.strip().replace("\n", "").replace("\r", "")

    # 3. 设置请求地址
    base_url = "https://ikuuu.pw"
    checkin_url = f"{base_url}/user/checkin"

    # 4. 构建请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": base_url,
        "Referer": f"{base_url}/user",
        "Cookie": cookie
    }

    # 5. 发送签到请求
    try:
        print(f"正在向 {checkin_url} 发送签到请求...")
        resp = requests.post(checkin_url, headers=headers, timeout=30)

        print(f"响应状态码: {resp.status_code}")
        print(f"响应内容: {resp.text}")

        # 6. 判断签到结果
        if resp.status_code == 200:
            try:
                data = resp.json()
                ret = data.get("ret", 0)
                msg = data.get("msg", "")

                if ret == 1:
                    print(f"✅ 签到成功: {msg}")
                elif "已签到" in msg or "已经签到" in msg:
                    print(f"✅ 今日已签到: {msg}")
                else:
                    print(f"⚠️ 签到返回异常: ret={ret}, msg={msg}")
                    sys.exit(1)
            except Exception:
                # 非 JSON 响应
                if "已签到" in resp.text:
                    print("✅ 今日已签到")
                else:
                    print(f"⚠️ 响应不是标准 JSON 格式")
                    sys.exit(1)
        else:
            print(f"❌ 请求失败，状态码: {resp.status_code}")
            sys.exit(1)

    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请检查网络或域名")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 签到失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
