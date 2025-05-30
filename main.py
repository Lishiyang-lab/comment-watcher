import os
import requests
import hashlib
import time
from bs4 import BeautifulSoup
from datetime import datetime

# 設定 LINE Bot
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

# 已發送的留言紀錄（防止重複通知）
sent_hashes = set()

def get_latest_comments():
    url = "https://www.cmoney.tw/forum/user/7840723"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    comments = soup.select("pre.textRule_text")
    return [comment.text.strip() for comment in comments]

def send_line_notify(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post(url, headers=headers, json=data)

def check_for_updates():
    comments = get_latest_comments()
    for comment in comments:
        hashcode = hashlib.md5(comment.encode()).hexdigest()
        if hashcode not in sent_hashes:
            send_line_notify(f"新留言：\n{comment}")
            sent_hashes.add(hashcode)

if __name__ == "__main__":
    print(f"[{datetime.now()}] 啟動留言監聽器...")
    while True:
        check_for_updates()
        time.sleep(60)  # 每 60 秒檢查一次
