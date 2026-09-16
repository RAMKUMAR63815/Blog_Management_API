import os
import smtplib #Python's built-in library for communicating with an SMTP mail server

from dotenv import load_dotenv
from email.mime.text import MIMEText #The actual email body is plain text
from email.mime.multipart import MIMEMultipart #Create an empty email envelope from,to,subject


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# EMAIL CONFIGURATION
# =========================================================

SMTP_SERVER = os.getenv(
    "SMTP_SERVER",
    "smtp.gmail.com" #none means use default
)

SMTP_PORT = int(
    os.getenv(
        "SMTP_PORT",
        "587"
    )
)

EMAIL_USERNAME = os.getenv(
    "EMAIL_USERNAME",
    ""
)

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD",#Gmail App Password
    ""
)


# =========================================================
# SEND EMAIL
# =========================================================

def send_email(
    to_email: str,
    subject: str,
    message: str
):

    # -----------------------------------------------------
    # Check email configuration
    # -----------------------------------------------------

    if not EMAIL_USERNAME or not EMAIL_PASSWORD:

        print("\n========================================")
        print("EMAIL CONFIGURATION ERROR")
        print("========================================")
        print("EMAIL_USERNAME or EMAIL_PASSWORD is missing.")
        print("Please check your .env file.")
        print("========================================\n")

        return False


    # -----------------------------------------------------
    # Create email
    # -----------------------------------------------------

    email = MIMEMultipart() #Create email

    email["From"] = EMAIL_USERNAME
    email["To"] = to_email
    email["Subject"] = subject

    email.attach(
        MIMEText(
            message,
            "plain"
        )
    )


    # -----------------------------------------------------
    # Send email through Gmail
    # -----------------------------------------------------

    try:

        print("\n========================================")
        print("SENDING EMAIL")
        print("========================================")
        print(f"From : {EMAIL_USERNAME}")
        print(f"To   : {to_email}")
        print(f"Subject : {subject}")
        print("========================================")

        #Python's built-in library for sending email using SMTP -is class inside smtplib use to communicate with a mail server
        with smtplib.SMTP( #This connects my Python application to the SMTP server. with --->After sending the email, the SMTP connection is properly closed
            SMTP_SERVER,
            SMTP_PORT
        ) as server:

            server.ehlo() #This is an SMTP communication command (Hello, this client is connecting and these are the capabilities it supports)

            server.starttls() #upgrades this SMTP connection to a secure encrypted connection using TLS

            server.ehlo() #capabilities for the secured connection.Now that we're communicating securely, let's identify ourselves again and establish the SMTP capabilities for the secure session

            server.login( #This authenticates our application with Gmail.
                EMAIL_USERNAME,
                EMAIL_PASSWORD
            )

            server.send_message(
                email
            )


        print(
            f"Email sent successfully to {to_email}"
        )

        return True


    except smtplib.SMTPAuthenticationError:

        print(
            "Email sending failed: Gmail authentication failed."
        )

        print(
            "Check your Gmail App Password."
        )

        return False


    except Exception as e:

        print(
            f"Email sending failed: {e}"
        )

        return False


# =========================================================
# COMMENT NOTIFICATION
# =========================================================

def send_comment_notification(
    post_author_email: str,
    commenter_username: str,
    post_title: str,
    comment_text: str
):

    subject = "New comment on your blog post"


    message = f"""
Hello,

{commenter_username} has commented on your blog post.

Post:
{post_title}

Comment:
{comment_text}

Thank you,
Blog Management API
"""


    return send_email(
        to_email=post_author_email,
        subject=subject,
        message=message
    )


# =========================================================
# LIKE NOTIFICATION
# =========================================================

def send_like_notification(
    post_author_email: str,
    liker_username: str,
    post_title: str
):

    subject = "Someone liked your blog post"


    message = f"""
Hello,

{liker_username} liked your blog post.

Post:
{post_title}

Thank you,
Blog Management API
"""


    return send_email(
        to_email=post_author_email,
        subject=subject,
        message=message
    )