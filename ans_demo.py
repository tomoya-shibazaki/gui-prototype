import streamlit as st
import requests
import pandas as pd
import json

# --- 1. 定義：ステータス変換マッピング ---
STATUS_MAP = {
    1: {"label": "大幅に低い (Much below usual)", "color": "red"},
    2: {"label": "低い (Below usual)", "color": "orange"},
    3: {"label": "通常通り (Usual)", "color": "green"},
    4: {"label": "高い (Above usual)", "color": "blue"},
    5: {"label": "大幅に高い (Much above usual)", "color": "purple"}
}

def get_polar_nightly_recharge(access_token):
    # 本来は日付を動的に設定（例：昨日や今日）
    # url = "https://www.polaraccesslink.com/v3/users/nightly-recharge"
    # ここではテスト用に直近のデータを取得する想定
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    # 全履歴を取得する場合
    response = requests.get('https://www.polaraccesslink.com/v3/users/nightly-recharge', headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"APIエラー: {response.status_code}")
        return None

# --- 2. Streamlit UI 構築 ---
st.title("🏥 Polar ANS 評価システム")

access_token = st.sidebar.text_input("Polar Access Token", type="password")

if access_token:
    data = get_polar_nightly_recharge(access_token)
    
    if data and "recharges" in data:
        # 最新の1件を取得
        latest = data["recharges"][-1] 
        ans_val = latest.get("ans_charge", 0.0)
        ans_stat = latest.get("ans_charge_status", 3)
        date_str = latest.get("date")

        st.subheader(f"📅 測定日: {date_str}")

        # スコア表示（-10.0 ～ +10.0）
        # 0が「いつも通り」なので、deltaにans_valをそのまま入れると分かりやすい
        st.metric(label="ANS Charge (個人平均との乖離)", value=ans_val, delta=f"{ans_val:.1f}")

        # ステータスの判定表示
        status_info = STATUS_MAP.get(ans_stat, {"label": "不明", "color": "gray"})
        st.markdown(f"### 現在のコンディション: :{status_info['color']}[{status_info['label']}]")

        # 判断ロジック
        st.divider()
        if ans_stat <= 2:
            st.error("🚨 【負荷軽減】自律神経の回復が不十分です。ストレッチや軽作業に留めてください。")
        elif ans_stat == 3:
            st.success("✅ 【通常通り】予定通りのメニューを推奨します。")
        else:
            st.info("🔥 【積極的負荷】回復状態が非常に良好です。一段階上のトレーニングも検討可能です。")
            
    else:
        st.warning("Nightly Recharge のデータが見つかりませんでした。")
else:
    st.info("サイドバーに Access Token を入力してください。")