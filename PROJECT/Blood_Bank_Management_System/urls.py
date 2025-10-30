# your_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.about, name="about"),
    path("signup/", views.donor_signup, name="donor_signup"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("home/", views.home, name="home"),
    path('hospital/dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('hospital/send-email/<int:user_id>/<int:hospital_id>/', views.send_email_to_donor, name='send_email_to_donor'),
    path("hospital/signup/", views.hospital_signup, name="hospital_signup"),
    path("login/", views.login_view, name="login"),
    path("donor/<int:donor_id>/send-otp/", views.send_otp_to_donor, name="send_otp_to_donor"),
    path("donor/verify-otp/", views.verify_donation_otp, name="verify_donation_otp"),
    path("donation-history/<int:donor_id>/", views.donation_history, name="donation_history"),
    path("send-email-filtered/", views.send_email_to_filtered, name="send_email_to_filtered"),
]
