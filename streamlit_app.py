import streamlit as st

# -----------------------------
# ページ設定
# -----------------------------
st.set_page_config(
    page_title="1RM Calculator",
    page_icon="💪",
    layout="centered"
)

st.title("💪 最大挙上重量（1RM）計算アプリ")
st.write("重量と回数を入力すると、推定1RMを計算します。")

# -----------------------------
# 入力
# -----------------------------
st.subheader("入力")

weight = st.number_input(
    "使用重量 (kg)",
    min_value=0.0,
    step=2.5
)

reps = st.number_input(
    "回数",
    min_value=1,
    max_value=20,
    step=1
)

formula = st.selectbox(
    "計算式を選択",
    ["Epley式", "Brzycki式"]
)

# -----------------------------
# 計算
# -----------------------------
def calc_1rm(weight, reps, formula):
    if formula == "Epley式":
        return weight * (1 + reps / 30)
    else:  # Brzycki
        return weight * 36 / (37 - reps)

if weight > 0 and reps > 0:
    one_rm = calc_1rm(weight, reps, formula)

    # -----------------------------
    # 出力
    # -----------------------------
    st.subheader("結果")
    st.metric(
        label="推定1RM",
        value=f"{one_rm:.1f} kg"
    )

    st.info(
        f"計算式: {formula}\n\n"
        "※ 推定値であり、実測値とは誤差があります。"
    )
else:
    st.warning("重量と回数を入力してください。")

# -----------------------------
# 補足説明
# -----------------------------
with st.expander("1RMとは？"):
    st.write("""
**1RM（One Repetition Maximum）**とは、
ある種目を「1回だけ」持ち上げられる最大重量のことです。

このアプリでは、以下の推定式を使用しています。

- **Epley式**  
  1RM = 重量 × (1 + 回数 / 30)

- **Brzycki式**  
  1RM = 重量 × 36 / (37 − 回数)
""")
