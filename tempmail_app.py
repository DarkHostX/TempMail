import requests
from bs4 import BeautifulSoup

# الخطوة 1: إرسال طلب للموقع
url = "https://www.mohmal.com/ar"
headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(url, headers=headers)

# الخطوة 2: تحليل المحتوى باستخدام BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# مثال: طباعة كل العناوين <h1>
for h1 in soup.find_all("h1"):
    print(h1.text.strip())

# مثال: استخراج البريد المؤقت (إذا وُجد داخل عنصر محدد)
email_div = soup.find("div", {"id": "email"})
if email_div:
    print("📧 البريد المؤقت:", email_div.text.strip())
else:
    print("لم يتم العثور على البريد.")
