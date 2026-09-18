from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import uuid4  #generates a random unique ID
import os

from reportlab.pdfgen import canvas  #Think of canvas as a blank drawing board for PDFs

from ..database import get_db
from ..models import User, SubscriptionPlan, BillingHistory
from ..dependencies import get_current_user


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


# =========================================================
# GET ALL SUBSCRIPTION PLANS
# =========================================================

@router.get("/plans")
def get_subscription_plans(
    db: Session = Depends(get_db)
):
    plans = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.is_active == True
    ).all()

    return plans


# =========================================================
# UPGRADE SUBSCRIPTION
# =========================================================

@router.post("/upgrade/{plan_id}")
def upgrade_subscription(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Find selected plan
    plan = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.id == plan_id,
        SubscriptionPlan.is_active == True
    ).first()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found."
        )

    # Prevent upgrading to the same plan
    if current_user.subscription_plan_id == plan.id:
        raise HTTPException(
            status_code=400,
            detail="You are already subscribed to this plan."
        )

    # Subscription dates
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=30)

    # Generate fake transaction ID
    transaction_id = f"TXN_{uuid4().hex[:12].upper()}"  #give unique id .hex remove eyephen .give upto first 12 digit .convert to uppercase

    # =====================================================
    # CREATE INVOICE FOLDER
    # =====================================================

    invoice_dir = "media/invoices"
    os.makedirs(invoice_dir, exist_ok=True)

    invoice_filename = f"invoice_{transaction_id}.pdf"
    invoice_file_path = os.path.join(
        invoice_dir,
        invoice_filename
    )

    # =====================================================
    # CREATE FAKE INVOICE PDF
    # =====================================================

    pdf = canvas.Canvas(invoice_file_path)  #Create an empty PDF

    # Title
    pdf.setTitle("Subscription Invoice")

    # Header
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 800, "BLOG MANAGEMENT API")

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(220, 770, "SUBSCRIPTION INVOICE")

    # Line
    pdf.line(50, 750, 550, 750)

    # Customer Details
    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 720, f"User ID:")
    pdf.drawString(200, 720, str(current_user.id))

    pdf.drawString(50, 695, f"Plan Name:")
    pdf.drawString(200, 695, plan.name)

    pdf.drawString(50, 670, f"Amount:")
    pdf.drawString(200, 670, f"Rs. {plan.price}")

    pdf.drawString(50, 645, f"Transaction ID:")
    pdf.drawString(200, 645, transaction_id)

    pdf.drawString(50, 620, f"Start Date:")
    pdf.drawString(200, 620, str(start_date))

    pdf.drawString(50, 595, f"End Date:")
    pdf.drawString(200, 595, str(end_date))

    # Line
    pdf.line(50, 560, 550, 560)

    # Footer
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 520, "Thank you for your subscription!")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        50,
        500,
        "This is a system-generated invoice."
    )

    pdf.save()

    # =====================================================
    # CREATE BILLING HISTORY
    # =====================================================

    billing = BillingHistory(
        user_id=current_user.id,
        plan_id=plan.id,
        amount=plan.price,
        transaction_id=transaction_id,
        invoice_path=f"/media/invoices/{invoice_filename}",
        start_date=start_date,
        end_date=end_date
    )

    db.add(billing)

    # =====================================================
    # UPDATE USER PLAN
    # =====================================================

    current_user.subscription_plan_id = plan.id

    db.commit()
    db.refresh(billing)

    return {
        "message": f"Successfully upgraded to {plan.name} plan.",
        "plan": plan.name,
        "amount": plan.price,
        "transaction_id": transaction_id,
        "invoice": billing.invoice_path,
        "start_date": start_date,
        "end_date": end_date
    }


# =========================================================
# GET CURRENT USER BILLING HISTORY
# =========================================================

@router.get("/billing")
def get_billing_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    billing_history = db.query(BillingHistory).filter(
        BillingHistory.user_id == current_user.id
    ).order_by(
        BillingHistory.created_at.desc()
    ).all()

    return billing_history