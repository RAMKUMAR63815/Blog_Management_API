from app.database import SessionLocal
from app.models import SubscriptionPlan


db = SessionLocal()

try:
    # Check whether plans already exist
    existing_plans = db.query(sq).count()

    if existing_plans > 0:
        print("Subscription plans already exist.")
    else:
        basic = SubscriptionPlan(
            name="Basic",
            price=0,
            max_posts=1,
            max_images=1,
            max_comments=10,
            max_likes=10,
            is_active=True
        )

        premium = SubscriptionPlan(
            name="Premium",
            price=499,
            max_posts=2,
            max_images=2,
            max_comments=50,
            max_likes=50,
            is_active=True
        )

        pro = SubscriptionPlan(
            name="Pro",
            price=999,
            max_posts=None,
            max_images=None,
            max_comments=None,
            max_likes=None,
            is_active=True
        )

        db.add(basic)
        db.add(premium)
        db.add(pro)

        db.commit()

        print("Basic, Premium and Pro plans added successfully.")

finally:
    db.close()