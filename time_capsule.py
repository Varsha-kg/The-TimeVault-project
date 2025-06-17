import json
from datetime import datetime
from cryptography.fernet import Fernet

# Get user input
message = input("📨 Enter the message to encrypt: ")
unlock_str = input("⏰ Enter unlock date and time (YYYY-MM-DD HH:MM): ")
recipient_email = input("📧 Enter the recipient email: ")

# Parse unlock time
try:
    unlock_time = datetime.strptime(unlock_str, "%Y-%m-%d %H:%M")
except ValueError:
    print("❌ Invalid date format. Use YYYY-MM-DD HH:MM.")
    exit()

# Generate encryption key
key = Fernet.generate_key()
cipher = Fernet(key)
encrypted_msg = cipher.encrypt(message.encode())

# Save encrypted message and key
with open("capsule.tc", "wb") as f:
    f.write(encrypted_msg)

with open("secret.key", "wb") as f:
    f.write(key)

# Save unlock info
info = {
    "unlock_time": unlock_time.strftime("%Y-%m-%d %H:%M"),
    "recipient_email": recipient_email
}

with open("capsule_info.json", "w") as f:
    json.dump(info, f)

print("✅ Time capsule created and saved!")
print("📁 Files: capsule.tc, secret.key, capsule_info.json")
