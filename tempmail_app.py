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

# زر توليد بريد جديد
if st.button("🔁 توليد بريد جديد"):
    email, token = create_account()
    if email:
        st.session_state["email"] = email
        st.session_state["token"] = token
        st.success(f"📨 البريد المؤقت الخاص بك:\n\n`{email}`")
    else:
        st.error("❌ تعذر إنشاء البريد. حاول مرة أخرى.")

# التحقق من وجود بريد مخزن في الجلسة
if "email" in st.session_state and "token" in st.session_state:
    email = st.session_state["email"]
    token = st.session_state["token"]

    st.subheader("📥 صندوق الرسائل")

    # زر تحديث الرسائل
    if st.button("🔄 تحديث الرسائل"):
        st.session_state["refresh"] = True

    # عرض الرسائل
    headers = {"Authorization": f"Bearer {token}"}
    try:
        inbox = requests.get("https://api.mail.tm/messages", headers=headers).json()

        if inbox["hydra:member"]:
            for msg in inbox["hydra:member"]:
    msg_detail = requests.get(
        f"https://api.mail.tm/messages/{msg['id']}", headers=headers
    ).json()

    message_text = msg_detail.get("text") or msg_detail.get("html") or "📭 لا يوجد محتوى"

    with st.container():
        st.markdown(
            f"""
            <div style="background-color:#f9f9f9;padding:15px;border-radius:12px;border:1px solid #ccc;margin-bottom:15px;">
                <h4 style="margin-bottom:5px;">✉️ من: {msg['from']['address']}</h4>
                <p><strong>📝 الموضوع:</strong> {msg['subject']}</p>
                <p><strong>📅 التاريخ:</strong> {msg['createdAt']}</p>
                <hr style="margin:10px 0;">
                <div style="white-space:pre-wrap;background:#fff;border:1px solid #eee;padding:10px;border-radius:6px;">
                    {message_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

                # تفاصيل الرسالة
                msg_detail = requests.get(
                    f"https://api.mail.tm/messages/{msg['id']}", headers=headers
                ).json()

                message_text = msg_detail.get("text")
                if not message_text:
                    message_text = msg_detail.get("html")

                if message_text:
                    st.markdown("#### محتوى الرسالة:")
                    st.code(message_text, language="html")
                else:
                    st.info("📭 لا يوجد محتوى قابل للعرض في هذه الرسالة.")

                st.markdown("---")
        else:
            st.info("لا توجد رسائل حالياً.")
    except Exception as e:
        st.error(f"فشل في جلب الرسائل: {e}")
