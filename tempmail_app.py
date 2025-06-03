import streamlit as st
import requests
import uuid

# إعداد الصفحة
st.set_page_config(page_title="📧 بريد مؤقت", layout="centered")
st.markdown("""
    <style>
        body { direction: rtl; text-align: right; }
        .msg-card {
            background-color:#f9f9f9;
            padding:15px;
            border-radius:12px;
            border:1px solid #ccc;
            margin-bottom:15px;
        }
        .msg-content {
            white-space: pre-wrap;
            background: #fff;
            border: 1px solid #eee;
            padding: 10px;
            border-radius: 6px;
            direction: ltr;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📧 بريد مؤقت")
st.markdown("خدمة بريد مؤقت آمنة وسريعة - بديل مهمل")

# دالة لإنشاء حساب مؤقت
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

# توليد بريد جديد
if st.button("🔁 توليد بريد جديد"):
    email, token = create_account()
    if email:
        st.session_state["email"] = email
        st.session_state["token"] = token
        st.success("✅ تم توليد البريد بنجاح!")
    else:
        st.error("❌ تعذر توليد البريد. حاول مرة أخرى.")

# عرض البريد الحالي مع زر نسخ
if "email" in st.session_state and "token" in st.session_state:
    email = st.session_state["email"]
    token = st.session_state["token"]

    st.markdown("### 📨 بريدك المؤقت:")
    st.code(email)

    if st.button("📋 نسخ البريد"):
        st.toast("📋 تم نسخ البريد إلى الحافظة!")

    st.subheader("📥 صندوق الرسائل")

    if st.button("🔄 تحديث الرسائل"):
        st.session_state["refresh"] = True

    headers = {"Authorization": f"Bearer {token}"}
    try:
        inbox = requests.get("https://api.mail.tm/messages", headers=headers).json()

        if inbox["hydra:member"]:
            for msg in inbox["hydra:member"]:
                msg_detail = requests.get(
                    f"https://api.mail.tm/messages/{msg['id']}", headers=headers
                ).json()

                message_text = msg_detail.get("text") or msg_detail.get("html") or "📭 لا يوجد محتوى"

                st.markdown(
                    f"""
                    <div class="msg-card">
                        <strong>✉️ من:</strong> {msg['from']['address']}<br>
                        <strong>📝 الموضوع:</strong> {msg['subject']}<br>
                        <strong>📅 التاريخ:</strong> {msg['createdAt']}<hr>
                        <div class="msg-content">{message_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("📭 لا توجد رسائل حالياً.")
    except Exception as e:
        st.error(f"❌ فشل في جلب الرسائل: {e}")
