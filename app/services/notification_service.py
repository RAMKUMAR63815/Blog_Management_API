#What , WHEN and WHY to send email
# ============================================================
# notification_service.py
# Handles notification logic for likes and comments
# ============================================================

from datetime import datetime

from .email_service import send_email
# Imports the reusable email-sending function
#
# notification_service.py decides:
# - what happened
# - who performed the activity
# - which post was affected
# - what email subject/body should be
#
# email_service.py actually sends that email through SMTP


# ============================================================
# COMMENT NOTIFICATION
# ============================================================

def send_comment_notification(
    post_author_email: str,
    commenter_username: str,
    post_title: str,
    comment_text: str
):
    # This function creates the notification
    # when somebody comments on a blog post


    timestamp = datetime.now().strftime(
        "%Y-%m-%d %I:%M %p"
    )
    # Gets the current date and time
    #
    # Example:
    # 2026-09-21 10:30 AM
    #
    # Timestamp is required by the assignment


    subject = "New comment on your blog post"
    # Email subject


    message = f"""
Hello,

{commenter_username} has commented on your blog post.

Post Title:
{post_title}

Comment:
{comment_text}

Activity Type:
Comment

Timestamp:
{timestamp}

Thank you,
Blog Management API
"""
    # Creates the actual notification email content
    #
    # Assignment requires:
    # 1. Post Title
    # 2. Name of user who commented
    # 3. Activity type
    # 4. Timestamp


    return send_email(
        to_email=post_author_email,
        subject=subject,
        message=message
    )
    # Passes the prepared email to email_service.py
    #
    # notification_service.py -> creates notification
    # email_service.py        -> sends notification


# ============================================================
# LIKE NOTIFICATION
# ============================================================

def send_like_notification(
    post_author_email: str,
    liker_username: str,
    post_title: str
):
    # This function creates the notification
    # when somebody likes a blog post


    timestamp = datetime.now().strftime(
        "%Y-%m-%d %I:%M %p"
    )
    # Gets the current date and time


    subject = "Someone liked your blog post"
    # Email subject


    message = f"""
Hello,

{liker_username} liked your blog post.

Post Title:
{post_title}

Activity Type:
Like

Timestamp:
{timestamp}

Thank you,
Blog Management API
"""
    # Creates the actual notification email content
    #
    # Assignment requires:
    # 1. Post Title
    # 2. Name of user who liked
    # 3. Activity type
    # 4. Timestamp


    return send_email(
        to_email=post_author_email,
        subject=subject,
        message=message
    )
    # Sends the prepared notification through email_service.py