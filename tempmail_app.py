<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>بريد مؤقت | بديل مهمل</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #f7f7f7;
      margin: 0;
      padding: 0;
      direction: rtl;
      text-align: center;
    }
    header {
      background-color: #2c3e50;
      color: white;
      padding: 1rem;
    }
    .container {
      margin: 2rem auto;
      padding: 2rem;
      background: white;
      max-width: 600px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .email-box {
      font-size: 1.2rem;
      background-color: #ecf0f1;
      padding: 1rem;
      border-radius: 8px;
      margin-bottom: 1rem;
      direction: ltr;
      text-align: left;
    }
    button {
      padding: 0.7rem 1.5rem;
      font-size: 1rem;
      border: none;
      border-radius: 6px;
      background-color: #3498db;
      color: white;
      cursor: pointer;
    }
    button:hover {
      background-color: #2980b9;
    }
    .inbox {
      text-align: right;
      margin-top: 2rem;
    }
    .message {
      border-bottom: 1px solid #ccc;
      padding: 1rem 0;
    }
  </style>
</head>
<body>
  <header>
    <h1>بريد مؤقت</h1>
    <p>خدمة بريد مؤقت آمنة وسريعة - بديل مهمل</p>
  </header>

  <div class="container">
    <div class="email-box" id="email">جارٍ توليد بريدك المؤقت...</div>
    <button onclick="generateEmail()">🔁 توليد بريد جديد</button>

    <div class="inbox" id="inbox">
      <h2>📥 صندوق الرسائل</h2>
      <p>لا توجد رسائل حالياً.</p>
    </div>
  </div>

  <script>
    function generateEmail() {
      fetch("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        .then(res => res.json())
        .then(data => {
          const email = data[0];
          document.getElementById("email").textContent = email;
        })
        .catch(() => {
          document.getElementById("email").textContent = "تعذر توليد البريد. حاول مرة أخرى.";
        });
    }
    generateEmail();
  </script>
</body>
</html>
