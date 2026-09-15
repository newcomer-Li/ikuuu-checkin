import os
import requests
import sys


def checkin_one(cookie, index):
    """签到单个账号"""
    cookie = cookie.strip().replace("\n", "").replace("\r", "")
    if not cookie:
        return False, "Cookie 为空"

    base_url = "https://ikuuu.pw"
    checkin_url = f"{base_url}/user/checkin"
    user_url = f"{base_url}/user"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": base_url,
        "Referer": user_url,
        "Cookie": cookie
    }

    try:
        resp = requests.post(checkin_url, headers=headers, timeout=30)

        if resp.status_code != 200:
            return False, f"HTTP {resp.status_code}"

        try:
            data = resp.json()
            ret = data.get("ret", 0)
            msg = data.get("msg", "")
            if ret == 1:
                return True, msg
            elif "已签到" in msg or "已经签到" in msg:
                return True, f"今日已签到: {msg}"
            else:
                return False, f"ret={ret}, msg={msg}"
        except Exception:
            if "已签到" in resp.text:
                return True, "今日已签到"
            return False, f"非 JSON 响应: {resp.text[:100]}"

    except requests.exceptions.Timeout:
        return False, "请求超时"
    except requests.exceptions.ConnectionError:
        return False, "连接失败"
    except Exception as e:
        return False, str(e)


def main():
    # 1. 收集所有以 IKUUU_COOKIE_ 开头的环境变量
    cookie_map = {}
    for key, value in os.environ.items():
        if key.startswith("IKUUU_COOKIE_") and value.strip():
            # 按编号排序，保证执行顺序稳定
            cookie_map[key] = value.strip()

    if not cookie_map:
        print("❌ 未找到任何 Cookie（请检查 Secret 配置）")
        sys.exit(1)

    # 按编号排序，例如 IKUUU_COOKIE_1, IKUUU_COOKIE_2, ...
    sorted_keys = sorted(cookie_map.keys(), key=lambda k: int(k.split("_")[-1]) if k.split("_")[-1].isdigit() else 999)

    print(f"📋 共检测到 {len(sorted_keys)} 个账号\n")

    # 2. 逐个签到
    ok_count = 0
    fail_count = 0

    for i, key in enumerate(sorted_keys, 1):
        print(f"===== 账号 #{i} ({key}) =====")
        success, msg = checkin_one(cookie_map[key], i)
        if success:
            print(f"✅ 账号 #{i} 签到成功: {msg}\n")
            ok_count += 1
        else:
            print(f"❌ 账号 #{i} 签到失败: {msg}\n")
            fail_count += 1

    # 3. 汇总
    print("=" * 50)
    print(f"📊 汇总: 成功 {ok_count} 个, 失败 {fail_count} 个")
    print("=" * 50)

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
