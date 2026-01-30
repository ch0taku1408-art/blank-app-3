import streamlit as st
from supabase import create_client
import requests



url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# 二重保存防止フラグ
if "saved" not in st.session_state:
    st.session_state.saved = False

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
        "ベンチプレス","デッドリフト","スクワット",
        "インクラインプレス","ショルダープレス",
        "ローイング","アームカール","ハンマーカール",
        "サイドレイズ","キックバック"
    ]
)
exercise_map = {
    "ベンチプレス": "bench press",
    "デッドリフト": "deadlift",
    "スクワット": "squat",
    "インクラインプレス": "incline press",
    "ショルダープレス": "shoulder press",
    "ローイング": "rowing",
    "アームカール": "biceps curl",
    "ハンマーカール": "hammer curl",
    "サイドレイズ": "lateral raise",
    "キックバック": "triceps kickback"
}

exercise_en = exercise_map[exercise]
# -----------------------------
# 入力
# -----------------------------
st.subheader("入力")

weight = st.number_input("使用重量 (kg)", min_value=0.0, step=2.5)
reps = st.number_input("回数", min_value=1, max_value=20, step=1)

formula = st.selectbox("計算式を選択", ["Epley式", "Brzycki式"])

# -----------------------------
# 計算関数
# -----------------------------
def calc_1rm(weight, reps, formula):
    if formula == "Epley式":
        return weight * (1 + reps / 30)
    else:
        return weight * 36 / (37 - reps)
# -----------------------------
# -----------------------------

   

# -----------------------------
# 出力
# -----------------------------
if weight > 0 and reps > 0:
    one_rm = calc_1rm(weight, reps, formula)

    st.subheader("結果")
    st.markdown(f"### 🏋️ 種目: **{exercise}**")
    st.metric(label="推定1RM", value=f"{one_rm:.1f} kg")
        # -----------------------------
    # -----------------------------
        # -----------------------------
    # 種目の詳細情報（Wger）
    # -----------------------------
    st.divider()
    st.subheader("📚 種目の詳細情報")

    desc, category, muscles = get_exercise_info(exercise_en)

    if desc:
        st.markdown(f"**カテゴリ:** {category}")
        st.markdown(f"**主に使う筋肉:** {', '.join(muscles)}")
        st.markdown("**種目の説明:**")
        st.markdown(desc, unsafe_allow_html=True)
    else:
        st.info("この種目の詳細情報は見つかりませんでした。")

    # -----------------------------
    def get_exercise_info(exercise_name_en):
     url = "https://wger.de/api/v2/exerciseinfo/"
     params = {
        "limit": 200
      }

     response = requests.get(url, params=params)
     data = response.json()["results"]

     for ex in data:
        for t in ex["translations"]:
            name = t["name"]
            description = t["description"]

            if exercise_name_en.lower() in name.lower():
                category = ex["category"]["name"]
                muscles = [m["name"] for m in ex["muscles"]]
                return description, category, muscles

     return None, None, None


    # -----------------------------
    
    st.write("#### 参考重量（%1RM）")
    col1, col2, col3 = st.columns(3)
    col1.metric("70%", f"{one_rm * 0.7:.1f} kg")
    col2.metric("80%", f"{one_rm * 0.8:.1f} kg")
    col3.metric("90%", f"{one_rm * 0.9:.1f} kg")

    # -----------------------------
    # 保存処理
    # -----------------------------
    if st.button("この結果を保存する"):
        try:
            supabase.table("records").insert({
                "exercise": exercise,
                "weight": weight,
                "reps": reps,
                "one_rm": float(one_rm)
            }).execute()
            st.session_state.saved = True
        except Exception as e:
            st.error(e)

    if st.session_state.saved:
        st.success("記録をSupabaseに保存しました！")
        st.session_state.saved = False

    st.info(
        f"計算式: {formula}\n\n"
        "※ 1RMは推定値であり、実際の最大重量とは誤差があります。"
    )
else:
    st.warning("重量と回数を入力してください。")

# -----------------------------
# 履歴表示（追加部分）
# -----------------------------
st.divider()
st.subheader("📊 過去の記録")

try:
    records = supabase.table("records").select("*").order("id", desc=True).limit(10).execute().data

    if records:
        for r in records:
            st.write(
                f"{r['created_at']} ｜ {r['exercise']} ｜ "
                f"{r['weight']}kg × {r['reps']}回 → 1RM: {r['one_rm']:.1f}kg"
            )
    else:
        st.info("まだ記録がありません。")

except Exception as e:
    st.error(e)

# -----------------------------
# 補足説明
# -----------------------------
with st.expander("1RMとは？"):
    st.write("""
**1RM（One Repetition Maximum）**とは、
ある種目を「1回だけ」持ち上げられる最大重量のことです。

- **Epley式**: 1RM = 重量 × (1 + 回数 / 30)
- **Brzycki式**: 1RM = 重量 × 36 / (37 − 回数)


このアプリでは、以下の推定式を使用しています。

- **Epley式（低回数で行った人向け）**  
  1RM = 重量 × (1 + 回数 / 30)
　Epley式は、比較的低回数で行ったときに使われやすい計算方式で、低回数なら精度の高い1RMが算出されやすいです
- **Brzycki式（高回数で行った人向け）**  
  1RM = 重量 × 36 / (37 − 回数)
　Bzrcki式では高回数になるほど、1RMの値が高くなりすぎないように設定されている計算方式です。　""")
    

