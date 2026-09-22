from django.urls import path

from .views import dashboard


urlpatterns = [
    # /dashboard/ URL vandha dashboard view call aagum
    path(
            "", #This means nothing extra is added to the URL.our main urls.py already has: dashboard/ + nothing I don't need any additional URL
            dashboard, #function to execut
            name="dashboard"    #This gives this URL a name/label.Instead of remembering the actual URL:
        ),
]