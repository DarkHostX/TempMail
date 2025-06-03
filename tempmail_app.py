import streamlit as st
import requests

st.set_page_config(page_title="بريد مؤقت", layout="centered")

st.title("📧 بريد مؤقت مجانًا")
st.markdown("أنشئ بريدًا مؤقتًا واستقبل الرسائل خلال ثوانٍ.")

# توليد بريد مؤقت
if 'email' not in st.session_state:
    try:
        res = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1", timeout=10)
        st.write("📡 رد الخادم (للتصحيح):", res.text)  # فقط لأغراض التحقق، يمكنك إزالته لاحقًا

        res.raise_for_status()
        data = res.json()

        if isinstance(data, list) and data:
            st.session_state.email = data[0]
        else:
            st.error("❌ لم يتم توليد بريد مؤقت. حاول مرة أخرى.")
            st.stop()

    except Exception as e:
        st.error(f"🚫 حدث خطأ أثناء الاتصال بخادم البريد المؤقت:\n\n{str(e)}")
        st.stop()

email = st.session_state.email
st.success(f"📬 بريدك المؤقت: `{email}`")

login, domain = email.split("@")

# زر لتحديث الرسائل
if st.button("🔄 تحديث الرسائل"):
    st.experimental_rerun()

# جلب الرسائل
try:
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
    messages = requests.get(url, timeout=10).json()

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
            msg_detail = requests.get(msg_url, timeout=10).json()
            st.write("**نص الرسالة:**")
            st.code(msg_detail.get("textBody", "(لا يوجد نص)"))
            st.markdown("---")
except Exception as e:
    st.error(f"⚠️ تعذر جلب الرسائل:\n\n{str(e)}")
