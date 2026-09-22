from django.shortcuts import render #Django HTML template-a browser-ku return panna use pannuvom
#Business Logic Like FastAPI routers
# Create your views here.

def dashboard(request): #Browser-la /dashboard/ request vandha, indha function execute aagum.
    # User Dashboard HTML page-a render pannum
    return render(
        request, #This HTML response belongs to this current browser request
        "subscriptions/dashboard.html" #file-a Django browser-la display pannum
    )