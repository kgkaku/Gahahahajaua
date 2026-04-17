import requests
import json
import os

session = requests.Session()
HEADERS = {
    "User-Agent": "Toffee/8.8.0 (Linux;Android 7.1.2) ExoPlayerLib/2.18.6",
    "X-Device-Id": "868a562ab378666e",
    "client-api-header": "angM1aXCHQLmmSW6cDlpXMD6tLdwnhMoUeaBBFKmd98bX6Vrae5xCMbm4gg0+u33rnxeGQDZNr2GD1tW0cWwKEpWimNlGqXVQGhpiIBz1JFxN+OxXcQqaMPrjwUhCyI5mO1DGyNv18+Z2EpmHtVnLzV9SrGsQWu4oRKjxE8QIMsRs6LrvL6hWGPlOGQke/qb5QxQZNetPzI39jHhX7Zi2XrCMIT4a+gk2Wu1c3wIybwkqknPcTp4Bj1cEF3Q+q1dV05SBhzpEDfoR2BLyQ6dV3LvmY6MNKxbUjby7hMsg35lFl2Df2mZsr7C27309w/qWi8lLXDjB7B1MozIGKn8rw3bXY5YlrPKBKztyiisAjQQi7kc5ISXyGSwRmhciwkciuitsSL0LlqHY7/Qkkh71EtaK3XEgVpLdH8zRCsTwfu1iIVPiDwTycuuBy4XWkcNnd0iLB35yftQpiL8HfpO2jQnrAwzePxszJ7mewVG+M0P/qyTBD52NkPR8uW0AZmDKp5LHTCGf7sqldDzpZvU+gsSdvtsBUcmHzjINGEoyXk="
}

def fetch_toffee():
    channels = []
    # সরাসরি লাইভ ক্যারেক্টরি ফেচ করা হচ্ছে
    url = "https://content-prod.services.toffeelive.com/toffee/BD/DK/android-mobile/rail/generic/editorial-dynamic?filters=v_type:channels;subType:Live_TV&page=1"
    
    try:
        r = session.get(url, headers=HEADERS, timeout=20)
        items = r.json().get('list', [])
        
        for item in items:
            m_id = item.get('media', [{}])[0].get('mediaId')
            if m_id:
                # মেইন ডোমেইন দিয়ে লিঙ্ক রেজলভ করা
                token_url = f"https://prod-api.toffeelive.com/v1/playback/token/{m_id}"
                try:
                    p_res = session.get(token_url, headers=HEADERS, timeout=15)
                    if p_res.status_code == 200:
                        stream_data = p_res.json().get('data', {})
                        stream_link = stream_data.get('url')
                        cookie = p_res.cookies.get('Edge-Cache-Cookie')
                        
                        if stream_link:
                            channels.append({
                                "name": item.get('title'),
                                "logo": item.get('images', [{}])[0].get('path', ""),
                                "link": stream_link,
                                "cookie": cookie
                            })
                except: continue
        return channels
    except: return []

def save_output(data):
    if not data: return
    # ১. আপনার কাঙ্ক্ষিত JSON ফরম্যাট
    with open('toffee_channel_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    # ২. OTT Navigator M3U ফরম্যাট
    with open('toffee_OTT_Navigator.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for ch in data:
            f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}", {ch["name"]}\n')
            f.write(f'#EXTHTTP:{{"cookie":"{ch["cookie"]}"}}\n{ch["link"]}\n')

if __name__ == "__main__":
    channels = fetch_toffee()
    save_output(channels)
