# AWS SES OTP Verification App

This is a Python application that sends a secure One-Time Password (OTP) to a user's email using **AWS Simple Email Service (SES)**, and verifies the OTP within a 5-minute validity window.

---

## ✅ Features

- ✅ 6-digit secure numeric OTP generation
- ✅ Sends email with both **HTML and plain text** using AWS SES
- ✅ Verifies OTP with **5-minute expiration**
- ✅ Handles expired and incorrect OTPs gracefully
- ✅ Prompts for OTP retry or re-sending on failure
- ✅ Modular and well-documented code

---

## ⚙️ Prerequisites

- Python 3.7+
- AWS SES account (sandbox or production)
- Verified sender email in AWS SES
- AWS credentials configured via one of:
  - AWS CLI (`aws configure`)
  - `~/.aws/credentials` file
  - Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`

---

## 📦 Installation

1. **Download the script manually:**

   - Save the Python file (e.g., `otp_app.py`) to your local directory.
   - Create a `.env` file in the same directory with your AWS credentials and settings:

     ```
     AWS_ACCESS_KEY_ID=your-access-key
     AWS_SECRET_ACCESS_KEY=your-secret-key
     AWS_REGION=ap-southeast-1
     SENDER_EMAIL=your-verified-email@example.com
     RECEIVER_EMAIL=your-verified-email@example.com
    
2. **Install dependencies:**

   ```bash
   pip install boto3 python-dotenv

3. **Steps followed:**

   Imported all the required modules (boto3, os, random, datetime, etc.) and environment variables using dotenv.
   Generated OTP using a function that creates a 6-digit secure random number.   
   Created send_otp_email() function to:   
   Send OTP using AWS SES.   
   Include both plain text and styled HTML content for the email body.   
   Stored OTPs in an in-memory dictionary (otp_store) along with their timestamp using datetime.now(timezone.utc).   
   Implemented OTP verification logic in verify_otp():   
   Checks if the entered OTP matches.   
   Ensures the OTP hasn't expired (valid for 5 minutes).   
   Designed the main loop to handle different scenarios: 
   If OTP is correct and within 5 minutes → ✅ Verification successful, exit.   
   If OTP is incorrect → ❌ Show error and allow retry.   
   If OTP is correct but expired → 🔁 Ask if the user wants a new OTP.   
   If "yes", send a new OTP and restart.   
   If "no", exit the program.

   
📬 Contact
Created by Sahil Kumar Patra
Email: sahilkumar107607kxip@gmail.com
