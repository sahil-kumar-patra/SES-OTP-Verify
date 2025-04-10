import boto3 
import os
import random
import time
from datetime import datetime, timedelta
from botocore.exceptions import BotoCoreError, ClientError
from datetime import timezone

# Global in-memory OTP store
otp_store = {}

# AWS SES Configuration (region)
AWS_REGION = "ap-southeast-1"  # Update this if needed
SENDER = "sahilkumar107607kxip@gmail.com"  # Must be pre-verified in SES


def generate_otp():
    """Generates a secure 6-digit numeric OTP."""
    return f"{random.randint(100000, 999999)}"


def send_otp_email(recipient_email, otp):
    """Sends the OTP email using AWS SES (both HTML and plain text)."""
    subject = "Your One-Time Password (OTP)"
    body_text = f"Your OTP is: {otp}\nIt is valid for 5 minutes."
    body_html = f"""<html>
    <head>
      <style>
        .otp-box {{
          font-family: Arial, sans-serif;
          background-color: #f9f9f9;
          padding: 20px;
          border-radius: 10px;
          border: 1px solid #e0e0e0;
          max-width: 400px;
          margin: auto;
        }}
        .otp-code {{
          font-size: 24px;
          font-weight: bold;
          color: #2d3748;
          margin: 20px 0;
        }}
        .footer {{
          font-size: 12px;
          color: #888888;
          margin-top: 20px;
        }}
      </style>
    </head>
    <body>
      <div class="otp-box">
        <h2>🔐 Your One-Time Password (OTP)</h2>
        <p>Please use the following OTP to complete your verification:</p>
        <div class="otp-code">{otp}</div>
        <p>This OTP is valid for <strong>5 minutes</strong>.</p>
        <div class="footer">
          If you did not request this OTP, please ignore this email.
        </div>
      </div>
    </body>
    </html>"""


    client = boto3.client("ses", region_name=AWS_REGION)

    try:
        response = client.send_email(
            Source=SENDER,
            Destination={"ToAddresses": [recipient_email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Text": {"Data": body_text},
                    "Html": {"Data": body_html},
                },
            },
        )
        print("✅ OTP email sent successfully!")
        return True
    except ClientError as e:
        print(f"❌ Error sending email: {e.response['Error']['Message']}")
    except BotoCoreError as e:
        print(f"❌ BotoCoreError: {e}")
    return False


def store_otp(email, otp):
    """Stores OTP with timestamp."""
    otp_store[email] = {
        "otp": otp,
        "timestamp": datetime.now(timezone.utc)
    }


def verify_otp(email, user_input_otp):
    """Verifies the OTP with 5-minute expiration."""
    if email not in otp_store:
        return "❌ No OTP requested for this email."

    record = otp_store[email]
    current_time = datetime.now(timezone.utc)

    if current_time - record["timestamp"] > timedelta(minutes=5):
        del otp_store[email]
        return "❌ OTP has expired. Please request a new one."

    if record["otp"] == user_input_otp:
        del otp_store[email]
        return "✅ OTP verified successfully!"
    else:
        return "❌ Incorrect OTP. Please try again."


def main():
    print("=== AWS SES OTP Verification App ===")
    recipient_email = "sahil.patra@teleglobals.com"

    while True:
        otp = generate_otp()
        if not send_otp_email(recipient_email, otp):
            print("❌ Failed to send OTP. Please check your SES setup and try again.")
            return

        store_otp(recipient_email, otp)
        print("\n📧 An OTP has been sent to your email.")

        while True:
            user_otp = input("Enter the OTP: ").strip()
            result = verify_otp(recipient_email, user_otp)

            if result == "✅ OTP verified successfully!":
                print(result)
                return  # Exit the program

            elif result == "❌ OTP has expired. Please request a new one.":
                print(result)
                choice = input("🔁 Do you want to resend a new OTP? (yes/no): ").strip().lower()
                if choice == "yes":
                    break  # Break inner loop to resend OTP
                else:
                    print("👋 Exiting OTP verification.")
                    return

            else:
                print(result)  # Invalid OTP, keep retrying



if __name__ == "__main__":
    main()
