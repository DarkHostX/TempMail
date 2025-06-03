import streamlit as st
import requests
import uuid

# إعداد الواجهة
st.set_page_config(page_title="📧 بريد مؤقت (Mail.tm)", layout="centered")
st.title("📧 بريد مؤقت")
st.markdown("خدمة بريد مؤقت باستخدام [Mail.tm](https://mail.tm)")

# دالة: إنشاء بريد مؤقت جديد
def create_account():
    domain_resp = requests.get("https://api.mail.tm/domains")
    domain = domain_resp.json()["hydra:member"][0]["domain"]

    username = f"user_{uuid.uuid4().hex[:8]}"
    email = f"{username}@{domain}"
    password = uuid.uuid4().hex

    account_data = {
        "address": email,
        "password": password
    }

    create = requests.post("https://api.mail.tm/accounts", json=account_data)

    if create.status_code == 201:
        token_resp = requests.post("https://api.mail.tm/token", json=account_data)
        token = token_resp.json()["token"]
        return email, token
    else:
        return None, None

# توليد بريد عند الضغط
if st.button("🔁 توليد بريد جديد"):
    email, token = create_account()
    if email:
        st.session_state["email"] = email
        st.session_state["token"] = token
        st.success(f"📨 البريد المؤقت الخاص بك:\n\n`{email}`")
    else:
        st.error("❌ تعذر إنشاء البريد. حاول مرة أخرى.")

# إذا تم إنشاء البريد مسبقًا
if "email" in st.sessio
