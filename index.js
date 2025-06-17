const express = require('express');
const fs = require('fs');
const path = require('path');
const nodemailer = require('nodemailer');
const crypto = require('crypto');
const schedule = require('node-schedule');

const app = express();
const PORT = 3000;

app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

const ENCRYPTED_FILE = 'capsule.tc';
const KEY_FILE = 'secret.key';
const INFO_FILE = 'capsule_info.json';

function encryptMessage(message) {
  const key = crypto.randomBytes(32);
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  let encrypted = cipher.update(message, 'utf8', 'base64');
  encrypted += cipher.final('base64');
  fs.writeFileSync(ENCRYPTED_FILE, encrypted);
  fs.writeFileSync(KEY_FILE, JSON.stringify({ key: key.toString('base64'), iv: iv.toString('base64') }));
}

function scheduleEmail(unlockTime, recipientEmail) {
  schedule.scheduleJob(new Date(unlockTime), () => {
    try {
      const encrypted = fs.readFileSync(ENCRYPTED_FILE, 'utf8');
      const { key, iv } = JSON.parse(fs.readFileSync(KEY_FILE, 'utf8'));
      const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(key, 'base64'), Buffer.from(iv, 'base64'));
      let decrypted = decipher.update(encrypted, 'base64', 'utf8');
      decrypted += decipher.final('utf8');

      const transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
          user: 'your_gmail@gmail.com', // replace with your email
          pass: 'cpdvrkjjyiigjlenr'     // replace with your app password
        }
      });

      const mailOptions = {
        from: 'your_email@gmail.com',
        to: recipientEmail,
        subject: '⏳ Your Time Capsule Message',
        text: decrypted
      };

      transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
          console.error('❌ Email error:', error);
        } else {
          console.log('✅ Email sent:', info.response);
        }
      });
    } catch (err) {
      console.error('❌ Capsule error:', err);
    }
  });
}

app.post('/save', (req, res) => {
  const { message, unlockTime, email } = req.body;
  if (message && unlockTime && email) {
    encryptMessage(message);
    fs.writeFileSync(INFO_FILE, JSON.stringify({ unlockTime, email }));
    scheduleEmail(unlockTime, email);
    res.send('✅ Time Capsule Scheduled and Encrypted!');
  } else {
    res.send('❌ Missing fields.');
  }
});

app.get('/messages', (req, res) => {
  if (fs.existsSync(ENCRYPTED_FILE)) {
    const content = fs.readFileSync(ENCRYPTED_FILE, 'utf8');
    res.send(`<h2>Encrypted Message</h2><pre>${content}</pre>`);
  } else {
    res.send('<h2>No encrypted messages found.</h2>');
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
