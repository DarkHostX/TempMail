import streamlit as st
import requests

st.set_page_config(page_title="بريد مؤقت", layout="centered")

st.title("📧 بريد مؤقت مجانًا")
st.markdown("أنشئ بريدًا مؤقتًا واستقبل الرسائل خلال ثوانٍ عبر خدمة 1secmail.")

# توليد بريد مؤقت
if 'email' not in st.session_state:
    try:
    res = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1", timeout=10)
    if res.status_code == 200:
        st.session_state.email = res.json()[0]
    else:
        st.error("حدث خطأ أثناء توليد البريد المؤقت. الرجاء المحاولة لاحقًا.")
        st.stop()
except Exception as e:
    st.error("تعذر الاتصال بخادم البريد المؤقت.")
    st.stop()


email = st.session_state.email
st.success(f"📬 بريدك المؤقت: `{email}`")

login, domain = email.split("@")

# زر لتحديث الرسائل
if st.button("🔄 تحديث الرسائل"):
    st.experimental_rerun()

# جلب الرسائل
url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
messages = requests.get(url).json()

if not messages:
    st.info("لا توجد رسائل حالياً. جرّب مجددًا بعد دقيقة.")
else:
    st.write("## 📥 الرسائل الواردة:")
    for msg in messages:
        st.write(f"**من:** {msg['from']}")
        st.write(f"**الموضوع:** {msg['subject']}")
        st.write(f"**الوقت:** {msg['date']}")

        # قراءة محتوى الرسالة
        message_id = msg['id']
        msg_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={message_id}"
        msg_detail = requests.get(msg_url).json()
        st.write("**نص الرسالة:**")
        st.code(msg_detail.get("textBody", "(لا يوجد نص)"))
        st.markdown("---")
