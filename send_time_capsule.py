import yagmail
import schedule
import time
import json
from datetime import datetime
from cryptography.fernet import Fernet

# Load unlock info
try:
    with open("capsule_info.json", "r") as f:
        info = json.load(f)
    unlock_time_str = info["unlock_time"]
    recipient_email = info["recipient_email"]
except Exception as e:
    print(f"❌ Failed to read unlock time: {e}")
    exit()

# Format unlock time
unlock_time_obj = datetime.strptime(unlock_time_str, "%Y-%m-%d %H:%M")
unlock_time_formatted = unlock_time_obj.strftime("%H:%M")

print(f"⏰ [LOG] Waiting to send message at {unlock_time_formatted} on {unlock_time_obj.date()}...")

def send_email():
    print("📨 [LOG] Trying to send email...")
    if datetime.now() >= unlock_time_obj:
        print(f"📅 [LOG] Today: {datetime.today().date()}, Unlock Date: {unlock_time_obj.date()}")
        try:
            with open("secret.key", "rb") as kf:
                key = kf.read()
            cipher = Fernet(key)
            with open("capsule.tc", "rb") as cf:
                encrypted_msg = cf.read()
            decrypted_msg = cipher.decrypt(encrypted_msg).decode()

            # Your App Password here
            sender_email = "sender_gmail@gmail.com"
            app_password = "mrajjbmdcgklfqmn"  # Replace this

            yag = yagmail.SMTP(sender_email, app_password)
            yag.send(to=recipient_email, subject="⏳ Your Time Capsule Message", contents=decrypted_msg)
            print("✅ Email sent successfully!")
            return schedule.CancelJob
        except Exception as e:
            print(f"❌ Failed to send: {e}")
    else:
        print("⏳ [LOG] Not yet unlock time.")

# Schedule the send
schedule.every().day.at(unlock_time_formatted).do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)
