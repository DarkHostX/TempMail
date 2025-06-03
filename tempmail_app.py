import streamlit as st
import requests

st.set_page_config(page_title="بريد مؤقت", layout="centered", page_icon="📧")

st.title("📧 بريد مؤقت")
st.markdown("خدمة بريد مؤقت آمنة وسريعة - بديل مهمل")

if st.button("🔁 توليد بريد جديد"):
    try:
        res = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        email = res.json()[0]
        st.session_state['email'] = email
        st.success(f"تم توليد البريد المؤقت:\n\n📨 `{email}`")
    except:
        st.error("تعذر توليد البريد. حاول مرة أخرى.")

if 'email' in st.session_state:
    email = st.session_state['email']
    login, domain = email.split("@")

    st.subheader("📥 صندوق الرسائل")
    try:
        inbox_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        response = requests.get(inbox_url)
        messages = response.json()

        if messages:
            for msg in messages:
                st.markdown(f"### 📨 من: {msg['from']}")
                st.markdown(f"**الموضوع:** {msg['subject']}")
                st.markdown(f"**التاريخ:** {msg['date']}")
                msg_id = msg['id']
                msg_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}"
                msg_detail = requests.get(msg_url).json()
                st.code(msg_detail['textBody'], language='html')
                st.markdown("---")
        else:
            st.info("لا توجد رسائل حالياً.")
    except:
        st.warning("تعذر جلب الرسائل.")
