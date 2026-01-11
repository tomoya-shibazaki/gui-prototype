import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Polar リハビリ支援", layout="wide")
st.title("🏥 リハビリ意思決定支援: ANSステータス可視化")

# --- 0. 設定項目（サイドバー） ---
st.sidebar.header("ユーザー設定")
# ユーザーID入力項目の追加
user_id = st.sidebar.text_input("ユーザーIDを入力してくださ", placeholder="")

if not user_id:
    st.info("左側のサイドバーにユーザーIDを入力してください。")
    st.stop()

# --- 1. 仮データ作成 ---
# 本来はここで取得した user_id と access_token を使い API 呼び出しを行う
days = [datetime.today() - timedelta(days=i) for i in range(7)][::-1]
ans_status = np.random.uniform(30, 90, size=7)  # ANSスコア: 0〜100

data = pd.DataFrame({
    "日付": days,
    "ANSステータス": ans_status
})

# --- 2. グラフ表示 ---
st.subheader(f"👤 対象ユーザー: {user_id}")

fig = px.line(data, x="日付", y="ANSステータス", markers=True,
              title="過去1週間のANSステータス推移",
              labels={"ANSステータス": "自律神経回復度"})
fig.add_hline(y=60, line_dash="dash", line_color="green", annotation_text="攻めてもOK", annotation_position="top left")
fig.add_hline(y=40, line_dash="dash", line_color="red", annotation_text="負荷控えめ", annotation_position="bottom left")

st.plotly_chart(fig, use_container_width=True)

# --- 3. 当日の意思決定 ---
today_ans = ans_status[-1]
yesterday_ans = ans_status[-2]
ans_diff = today_ans - yesterday_ans

st.subheader("今日のリハビリ負荷判断")

# 差分を表示するメトリクス
st.metric(label="現在のANSステータス", value=f"{today_ans:.1f}", delta=f"{ans_diff:.1f} (前日比)")

if today_ans >= 60:
    st.success(f"判定: 安全に負荷をかけてOK")
elif today_ans >= 40:
    st.warning(f"判定: 負荷は中程度に調整")
else:
    st.error(f"判定: リハビリは軽め or 休息推奨")

# --- 4. 説明テキスト ---
st.markdown(f"""
---
**現場スタッフ向けメモ ({user_id} 様の状態):**
- **ANSステータス**が高いほど心身の回復度が高く、負荷をかけたリハビリが可能です。
- 数値が急落している場合は、本人が「大丈夫」と言っても**生理的な疲労**が溜まっているサインです。
- このデータに基づき、無理な追い込みを避けることで「転倒事故防止」と「早期回復」の両立を実現します。
""")
