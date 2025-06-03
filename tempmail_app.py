import streamlit as st
import requests
import uuid
import time

# إعداد الواجهة
st.set_page_config(page_title="📧 بريد مؤقت (Mail.tm)", layout="centered")
st.title("📧 بريد مؤقت")
st.markdown("خدمة بريد مؤقت باستخدام [Mail.tm](https://mail.tm)")

# الدالة: إنشاء بريد مؤقت جديد
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

# عند الضغط على الزر
if st.button("🔁 توليد بريد جديد"):
    email, token = create_account()
    if email:
        st.session_state["email"] = email
        st.session_state["token"] = token
        st.success(f"📨 البريد المؤقت الخاص بك:\n\n`{email}`")
    else:
        st.error("❌ تعذر إنشاء البريد. حاول مرة أخرى.")

# إذا تم إنشاء البريد مسبقًا
if "email" in st.session_state and "token" in st.session_state:
    email = st.session_state["email"]
    token = st.session_state["token"]

    st.subheader("📥 صندوق الرسائل")
    headers = {"Authorization": f"Bearer {token}"}

    try:
        inbox = requests.get("https://api.mail.tm/messages", headers=headers).json()

        if inbox["hydra:member"]:
            for msg in inbox["hydra:member"]:
                st.markdown(f"### ✉️ من: {msg['from']['address']}")
                st.markdown(f"**الموضوع:** {msg['subject']}")
                st.markdown(f"**التاريخ:** {msg['createdAt']}")
                msg_detail = requests.get(f"https://api.mail.tm/messages/{msg['id']}", headers=headers).json()
                st.code(msg_detail.get("text", "لا يوجد محتوى"), language='text')
                st.markdown("---")
        else:
            st.info("لا توجد رسائل حالياً.")
    except Exception as e:
        st.error(f"فشل في جلب الرسائل: {e}")
