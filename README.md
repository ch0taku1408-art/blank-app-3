# 💪 最大挙上重量（1RM）計算アプリ

## 🌐 デモURL
https://blank-app-jerh8wa8b78.streamlit.app/

## 🧩 このアプリは何？
このアプリは、筋トレ大好きなみんなが一度は気になるであろう1RM、つまり最大挙上重量について簡単に知ることができる画期的なアプリです！

## ✨ できること
- 種目別に1RMを算出できます
- 2種類（Epley式かBrzycki式）の方法で算出可能
- データの保存
## 🖥️ 使い方
1. 種目を選択する
2. 重量と回数を入力
3. Epley式かBrzycki式かを選択し1RMを算出
4. 算出した記録は保存可能

## 📸 画面イメージ
<img width="569" height="880" alt="スクリーンショット 2026-01-28 141638" src="https://github.com/user-attachments/assets/85eff78d-fcb9-4048-a5dc-aea196b2365e" />


## 🧠 使用している推定式
このアプリでは以下の推定式を使用しています。

- Epley式: ...1RM = 重量 × (1 + 回数 / 30)
- Brzycki式: ...1RM = 重量 × 36 / (37 − 回数)

## 🛠️ 使用技術
- Python
- Streamlit
- Supabase
- pandas

## 🚀 ローカルで動かす方法
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
