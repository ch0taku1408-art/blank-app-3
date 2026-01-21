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
st.write("筋トレ種目・重量・回数を入力すると、推定1RMを計算します。")

# -----------------------------
# 種目選択
# -----------------------------
st.subheader("トレーニング内容")

exercise = st.selectbox(
    "種目を選択してください",
    [
        "ベンチプレス",
        "デッドリフト",
        "スクワット",
        "インクラインプレス",
        "ショルダープレス",
        "ローイング",
        "アームカール",
        "ハンマーカール",
        "サイドレイズ",
        "キックバック"
    ]
)

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
# 計算関数
# -----------------------------
def calc_1rm(weight, reps, formula):
    if formula == "Epley式":
        return weight * (1 + reps / 30)
    else:  # Brzycki式
        return weight * 36 / (37 - reps)

# -----------------------------
# 出力
# -----------------------------
if weight > 0 and reps > 0:
    one_rm = calc_1rm(weight, reps, formula)

    st.subheader("結果")

    st.markdown(f"### 🏋️ 種目: **{exercise}**")

    st.metric(
        label="推定1RM",
        value=f"{one_rm:.1f} kg"
    )

    st.write("#### 参考重量（%1RM）")
    col1, col2, col3 = st.columns(3)
    col1.metric("70%", f"{one_rm * 0.7:.1f} kg")
    col2.metric("80%", f"{one_rm * 0.8:.1f} kg")
    col3.metric("90%", f"{one_rm * 0.9:.1f} kg")

    st.info(
        f"計算式: {formula}\n\n"
        "※ 1RMは推定値であり、実際の最大重量とは誤差があります。"
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

- **Epley式（低回数で行った人向け）**  
  1RM = 重量 × (1 + 回数 / 30)
　Epley式は、比較的低回数で行ったときに使われやすい計算方式で、低回数なら精度の高い1RMが算出されやすいです
- **Brzycki式（高回数で行った人向け）**  
  1RM = 重量 × 36 / (37 − 回数)
　Bzrcki式では高回数になるほど、1RMの値が高くなりすぎないように設定されている計算方式です。　""")
    

