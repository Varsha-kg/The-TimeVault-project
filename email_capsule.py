import yagmail
import schedule
import time
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

# === CONFIGURATION ===
SENDER_EMAIL = "varshakg18@gmail.com"           # <-- Replace with your Gmail
EMAIL_PASSWORD = "cpdv rkmy iigj lenr"       # <-- Replace with your Gmail App Password
RECEIVER_EMAIL = "varshakg15@gmail.com"     # <-- Replace with recipient email

UNLOCK_DATE = datetime.today().strftime("%Y-%m-%d")  # Send email today
SEND_TIME = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")  # Send 1 minute from now

ENCRYPTED_FILE = "capsule.tc"
KEY_FILE = "secret.key"

# === ENCRYPT MESSAGE ===
print("🎁 Creating your encrypted time capsule...")
message = input("📨 Enter your secret message: ")

# Encrypt and save
key = Fernet.generate_key()
cipher = Fernet(key)

with open(KEY_FILE, "wb") as kf:
    kf.write(key)

with open(ENCRYPTED_FILE, "wb") as ef:
    ef.write(cipher.encrypt(message.encode()))

print("✅ Capsule created and encrypted.")
print(f"⏰ Scheduling email for {SEND_TIME} daily...")

# === EMAIL SENDING FUNCTION ===
def send_email():
    today = datetime.today().strftime("%Y-%m-%d")
    print("📨 [LOG] Trying to send email...")
    print(f"📅 [LOG] Today: {today}, Unlock Date: {UNLOCK_DATE}")

    if today == UNLOCK_DATE:
        print("🔓 [LOG] Unlock date matched.")

        try:
            with open(KEY_FILE, "rb") as kf:
                saved_key = kf.read()
            with open(ENCRYPTED_FILE, "rb") as ef:
                encrypted_msg = ef.read()

            decryptor = Fernet(saved_key)
            decrypted_msg = decryptor.decrypt(encrypted_msg).decode()

            yag = yagmail.SMTP(SENDER_EMAIL, EMAIL_PASSWORD)
            yag.send(to=RECEIVER_EMAIL, subject="⏳ Your Time Capsule Message", contents=decrypted_msg)

            print("✅ Email sent successfully!")

        except Exception as e:
            print(f"❌ Email sending failed: {e}")
    else:
        print(f"🔒 Not yet time. Unlock date is {UNLOCK_DATE}.")

# === SCHEDULING ===
schedule.every().day.at(SEND_TIME).do(send_email)

# === LOOP ===
while True:
    schedule.run_pending()
    time.sleep(1)
