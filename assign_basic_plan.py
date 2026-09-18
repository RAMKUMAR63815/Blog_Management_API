from app.database import SessionLocal
from app.models import User, SubscriptionPlan


db = SessionLocal()

try:
    basic_plan = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.name == "Basic"
    ).first()

    if not basic_plan:
        print("Basic plan not found.")
    else:
        users = db.query(User).filter(
            User.subscription_plan_id.is_(None)
        ).all()

        for user in users:
            user.subscription_plan_id = basic_plan.id

        db.commit()

        print(f"Basic plan assigned to {len(users)} user(s).")

finally:
    db.close()