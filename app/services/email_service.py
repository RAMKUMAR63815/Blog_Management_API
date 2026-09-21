#HOW to send email
#To keep all email logic in one reusable place.
# ============================================================
# email_service.py
# Handles email sending using SMTP
# ============================================================

import os
import smtplib  # Python's built-in library for communicating with an SMTP mail server

from dotenv import load_dotenv

from email.mime.text import MIMEText
# MIMEText creates the actual plain-text email body

from email.mime.multipart import MIMEMultipart
# MIMEMultipart creates the email container/envelope
# where we can add From, To, Subject and Body


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()
# Loads SMTP settings from the .env file


# ============================================================
# EMAIL CONFIGURATION
# ============================================================

SMTP_SERVER = os.getenv(
    "SMTP_SERVER",
    "smtp.gmail.com"
)
# SMTP_SERVER = address of the email server
# Example:
# Gmail    -> smtp.gmail.com
# Mailtrap -> Mailtrap SMTP server


SMTP_PORT = int(
    os.getenv(
        "SMTP_PORT",
        "587"
    )
)
# SMTP_PORT = port number used by the SMTP server
# 587 is commonly used for STARTTLS


EMAIL_USERNAME = os.getenv(
    "EMAIL_USERNAME",
    ""
)
# Email account username
# Usually this is the sender email address


EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD",
    ""
)
# Password or SMTP credential
# For Gmail this can be an App Password
# For Mailtrap this will be the Mailtrap SMTP credential


# ============================================================
# SEND EMAIL
# ============================================================

def send_email(
    to_email: str,
    subject: str,
    message: str
):
    # send_email() is a reusable function
    # responsible only for sending an email
    #
    # It does NOT decide:
    # - who liked the post
    # - who commented
    # - which post was liked
    # - what notification message should be created
    #
    # Those responsibilities belong to notification_service.py

    if not EMAIL_USERNAME or not EMAIL_PASSWORD:
        # Check whether email configuration exists

        print("EMAIL CONFIGURATION ERROR")
        print("EMAIL_USERNAME or EMAIL_PASSWORD is missing.")
        print("Please check your .env file.")

        return False


    # ========================================================
    # CREATE EMAIL
    # ========================================================

    email = MIMEMultipart()
    # Creates the email container


    email["From"] = EMAIL_USERNAME
    # Sender email address


    email["To"] = to_email
    # Receiver email address


    email["Subject"] = subject
    # Email subject


    email.attach(
        MIMEText(
            message,
            "plain"
        )
    )
    # Adds the actual email message/body
    # "plain" means plain text email


    # ========================================================
    # CONNECT TO SMTP SERVER AND SEND EMAIL
    # ========================================================

    try:

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        ) as server:
            # Creates connection with SMTP server
            #
            # "with" automatically closes the SMTP connection
            # after email sending is completed

            server.ehlo()
            # Identifies our application to the SMTP server
            # and asks the server about its available capabilities


            server.starttls()
            # Starts TLS encryption
            # This protects the SMTP connection


            server.ehlo()
            # Identifies again after TLS encryption
            # and refreshes the SMTP server capabilities


            server.login(
                EMAIL_USERNAME,
                EMAIL_PASSWORD
            )
            # Logs into the SMTP server
            # using the configured username and password


            server.send_message(
                email
            )
            # Sends the complete email object


        print(
            f"Email sent successfully to {to_email}"
        )

        return True


    # ========================================================
    # EMAIL AUTHENTICATION ERROR
    # ========================================================

    except smtplib.SMTPAuthenticationError:

        print(
            "Email sending failed: "
            "SMTP authentication failed."
        )

        print(
            "Check your email username and password."
        )

        return False


    # ========================================================
    # OTHER EMAIL ERRORS
    # ========================================================

    except Exception as e:

        print(
            f"Email sending failed: {e}"
        )

        return False