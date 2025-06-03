import streamlit as st
import requests
import random
import string

st.set_page_config(page_title="بريد مؤقت", layout="centered")
st.title("📧 بريد مؤقت باستخدام Mail.tm")

# 🔁 توليد بريد مؤقت وهمي (للتجربة فقط)
def generate_random_email():
    domain = "mail.tm"
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{username}@{domain}", username, domain

# 📨 توليد البريد عند أول تشغيل
if 'email' not in st.session_state:
    email, username, domain = generate_random_email()
    st.session_state.email = email
    st.session_state.username = username
    st.session_state.domain = domain

email = st.session_state.email
username = st.session_state.username
domain = st.session_state.domain

# ✅ عرض البريد
st.success(f"📬 بريدك المؤقت: `{email}`")
st.info("⚠️ هذه نسخة تجريبية لعرض بريد مؤقت فقط، لا تستقبل رسائل حقيقية.")

# زر لتحديث البريد
if st.bu

