 #Give me Django's Admin functionality.
#Show models in Admin Panel
# Register your models here.

from django.contrib import admin
from .models import SubscriptionPlan, BillingHistory 


@admin.register(SubscriptionPlan)  #Take these two models from my app's models.py
class SubscriptionPlanAdmin(admin.ModelAdmin):#ModelAdmin is a Django class that controls how a model appears and behaves inside Django Admin.

    list_display = (
        "id",
        "name",
        "price",
        "max_posts",
        "max_images",
        "max_comments",
        "max_likes",
        "is_active",
    )
    ordering = (
        "id",
    )

@admin.register(BillingHistory)
class BillingHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user_id",
        "plan_id",
        "amount",
        "transaction_id",
        "invoice_path",
        "start_date",
        "end_date",
        "created_at",
    )

    list_display_links = (
        "id",
        "transaction_id",
    )

    ordering = (
        "-created_at",
      
    )
