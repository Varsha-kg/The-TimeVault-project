# The-TimeVault-project
A Time Capsule Web App where:  Users enter a message, email, and future date/time.  The message is encrypted and stored securely.  At the scheduled time, it's automatically decrypted and sent to the recipient’s email using Nodemailer.  Everything is built using Node.js, Express.js, and optional Python CLI tools.
DESCRIPTION:
**TimeVault** is a secure time capsule web and CLI application built with **Node.js**, **Python**, and **Express.js**. It lets users:
- 🔐 Encrypt a personal message
- 📅 Schedule it for future delivery
- 📧 Automatically send the decrypted message via email at the scheduled time
---
## 🌟 Features

- AES-256 encryption of messages
- Web-based frontend (`index.html`) + Node.js backend
- CLI-based encryption & decryption using Python
- Scheduled email delivery using `nodemailer` and `node-schedule`
- Secure `.tc` file format for capsules
- Metadata tracking with JSON files
---
## 🛠️ Tech Stack

- **Frontend:** HTML/CSS
- **Backend:** Node.js (Express.js)
- **Encryption & CLI:** Python (`cryptography`, `smtplib`, `datetime`)
- **Scheduling:** `node-schedule`, `cron`
- **Emailing:** `nodemailer` (Node.js), `smtplib` (Python)
---
## 📁 Folder Structure
The TimeVault Project/
├── public/
│ └── index.html

├── node_modules/

├── index.js # Express backend (Node.js)


├── time_capsule.py # Encrypt message CLI (Python)

├── send_time_capsule.py # Scheduled decrypt + email (Python)

├── email_capsule.py # Helper for sending emails (Python)

├── vault.txt # Stores encrypted messages (ignored)

├── capsule.tc # Encrypted message file

├── secret.key # Encryption key (ignored)

├── capsule_info.json # Metadata of capsules

├── package.json # Node.js config

└── .gitignore

🚀 How to Run

### 🔧 Setup

1. Clone the repository  :

   git clone https://github.com/your-username/the-timevault-project.git
   cd the-timevault-project
   \
Install Node.js dependencies
 a) npm install
 b)pip install cryptography

**Run Web Server**
node index.js
**🔐 Run CLI Encryption**
python time_capsule.py
**📬 Schedule Email Delivery**
python send_time_capsule.py

---
**📝 Notes**
secret.key and .tc files are excluded from GitHub

Don't forget to configure your email in email_capsule.py and allow less secure apps or use an app password.

**📄 License**
This project is for academic/demo purposes only. No license applied.

END...
