from django.urls import path

from .views import dashboard,auth_success,login_view


urlpatterns = [
    # /dashboard/ URL vandha dashboard view call aagum
    
        # This displays login.html
    path(
        "login/",
        login_view,
        name="login"
    ),
    
    path(
            "", #This means nothing extra is added to the URL.our main urls.py already has: dashboard/ + nothing I don't need any additional URL
            dashboard, #function to execut
            name="dashboard"    #This gives this URL a name/label.Instead of remembering the actual URL:
        ),
           path(
        "auth-success/",
        auth_success,
        name="auth_success"
    ),
]