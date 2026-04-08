import smtplib
import time
import re
from email.mime.text import MIMEText

# إعدادات SMTP (بدلها بمزودك)
SMTP_SERVER = "smtp.sendgrid.net"
SMTP_PORT = 587
USERNAME = "apikey"
PASSWORD = "YOUR_API_KEY"

FROM_EMAIL = "you@example.com"
SUBJECT = "Ihr Angebot"

BATCH_SIZE = 10
DELAY_BETWEEN_BATCH = 1.5  # 1.5 ثانية

# تحقق من الإيميل
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# قراءة الإيميلات
with open("data.txt", "r") as f:
    emails = [e.strip() for e in f if is_valid_email(e.strip())]

# قراءة الرسالة
with open("message.html", "r", encoding="utf-8") as f:
    html_content = f.read()

valid = []
refused = []

def send_email(server, to_email):
    msg = MIMEText(html_content, "html", "utf-8")
    msg["Subject"] = SUBJECT
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    try:
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        return False

# الاتصال بالسيرفر
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(USERNAME, PASSWORD)

    # إرسال على شكل حزم
    for i in range(0, len(emails), BATCH_SIZE):
        batch = emails[i:i+BATCH_SIZE]

        for email in batch:
            try:
                if send_email(server, email):
                    valid.append(email)
                    print("OK:", email)
                else:
                    refused.append(email)
                    print("FAIL:", email)
            except:
                refused.append(email)

        # التأخير بين الحزم
        time.sleep(DELAY_BETWEEN_BATCH)

# حفظ النتائج
with open("datavalid.txt", "w") as f:
    f.write("\n".join(valid))

with open("datarefus.txt", "w") as f:
    f.write("\n".join(refused))

print("تم الانتهاء من الإرسال ✅")
