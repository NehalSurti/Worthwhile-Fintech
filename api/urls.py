from django.urls import path
from api import views

urlpatterns = [
    # path('get-csrf-token', views.get_csrf_token, name='get-csrf-token'),
    path('contact-us', views.contactus, name="contactus"),
]