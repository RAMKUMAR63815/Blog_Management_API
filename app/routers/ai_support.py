from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models import AIChatLog
from ..schemas import AIChatRequest, AIChatResponse


# ============================================================
# AI SUPPORT ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/ai-support",
    tags=["AI Support"]
)


# ============================================================
# FAQ FUNCTION
# ============================================================

def get_faq_response(message: str):
    # User message-ah lowercase convert pannrom and remove spaces.
    # So "Billing", "BILLING", "billing"
    # ellame same-ah compare panna mudiyum.
    message = message.lower().strip()


    # --------------------------------------------------------
    # CREATE POST
    # --------------------------------------------------------

    if (
        "create post" in message
        or "create a post" in message
        or "new post" in message
    ):
        return (
            "To create a post, go to the Posts section, "
            "click Create Post, enter the title and content, "
            "then submit the post."
        )


    # --------------------------------------------------------
    # EDIT POST
    # --------------------------------------------------------

    if (
        "edit post" in message
        or "update post" in message
    ):
        return (
            "To edit a post, open your post from My Posts, "
            "click Edit, update the required information, "
            "and save the changes."
        )


    # --------------------------------------------------------
    # DELETE POST
    # --------------------------------------------------------

    if (
        "delete post" in message
        or "remove post" in message
    ):
        return (
            "To delete a post, open your own post and "
            "use the Delete option. Only the post owner "
            "can delete their own post."
        )


    # --------------------------------------------------------
    # SUBSCRIPTION
    # --------------------------------------------------------

    if (
        "subscription" in message
        or "plan" in message
    ):
        return (
            "You can choose an available subscription plan "
            "from the Subscription section. Each plan can "
            "have different post, image, comment, and like limits."
        )


    # --------------------------------------------------------
    # BILLING
    # --------------------------------------------------------

    if (
        "billing" in message
        or "invoice" in message
        or "payment" in message
    ):
        return (
            "You can check your billing information and "
            "invoice details from the billing or subscription "
            "section."
        )


    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    if (
        "dashboard" in message
        or "analytics" in message
    ):
        return (
            "The dashboard shows your personal statistics "
            "such as total posts, comments, likes received, "
            "and post views."
        )


    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

    if (
        "profile" in message
        or "account" in message
    ):
        return (
            "You can manage your account information from "
            "your profile section."
        )


    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    if (
        "hello" in message
        or "hi" in message
        or "hey" in message
    ):
        return (
            "Hello! I'm your Blog Support Assistant. "
            "I can help you with posts, subscriptions, "
            "billing, profiles, and dashboard questions."
        )


    # --------------------------------------------------------
    # DEFAULT RESPONSE
    # --------------------------------------------------------

    return (
        "I'm sorry, I don't have an answer for that yet. "
        "Please ask about creating, editing, or deleting posts, "
        "subscriptions, billing, profiles, or dashboard analytics."
    )


# ============================================================
# AI SUPPORT API
# ============================================================

@router.post(
    "/",
    response_model=AIChatResponse
)
def ai_support(
    request: AIChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # --------------------------------------------------------
    # USER QUESTION
    # --------------------------------------------------------

    # Frontend-la irundhu vandha question.
    user_message = request.message


    # --------------------------------------------------------
    # GET ANSWER
    # --------------------------------------------------------

    # Ippo real AI use pannala.
    # First FAQ based response generate pannrom.
    answer = get_faq_response(
        user_message
    )


    # --------------------------------------------------------
    # SAVE CHAT LOG
    # --------------------------------------------------------

    # User question + answer database-la save pannrom.
    chat_log = AIChatLog(
        user_id=current_user.id,
        question=user_message,
        response=answer
    )

    db.add(chat_log)

    db.commit()


    # --------------------------------------------------------
    # RETURN RESPONSE
    # --------------------------------------------------------


    # Frontend-ku AI answer return pannrom.
    return {
        "response": answer
    }