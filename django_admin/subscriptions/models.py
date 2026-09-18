#Django doesn't understand SQLAlchemy's So Django needs its own Python model definition to understand the existing table.
from django.db import models


class SubscriptionPlan(models.Model):#base class provided by Django for creating database models.

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    max_posts = models.IntegerField(null=True)
    max_images = models.IntegerField(null=True)
    max_comments = models.IntegerField(null=True)
    max_likes = models.IntegerField(null=True)
    is_active = models.BooleanField()

    class Meta:
        db_table = "subscription_plans"
        managed = False #not creating a second copy of the tables because we use:
        #Django. Don't create, alter, or delete it using Django migrations.
    def __str__(self): #Oru object-ai human-readable text-a display panna help pannum.
        return self.name
#object create pannumbodhu, self  current plan-a refer pannum.

class BillingHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    plan_id = models.IntegerField()
    amount = models.IntegerField()
    transaction_id = models.CharField(max_length=100)
    invoice_path = models.CharField(max_length=255, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = "billing_history"
        managed = False

    def __str__(self):
        return self.transaction_id