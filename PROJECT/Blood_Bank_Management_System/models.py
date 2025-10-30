from django.db import models
from django.db import models
from django.contrib.auth.models import User  # Default Django User
from datetime import date, timedelta

class Donor(models.Model):
    # Link donor to Django User (username, first_name, last_name, email, password)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Extra donor-specific fields
    age = models.IntegerField()

    gender = models.CharField(
        max_length=10,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other"),
        ]
    )

    contact_number = models.CharField(max_length=15, unique=True)

    blood_group = models.CharField(
        max_length=3,
        choices=[
            ("A+", "A+"), ("A-", "A-"),
            ("B+", "B+"), ("B-", "B-"),
            ("O+", "O+"), ("O-", "O-"),
            ("AB+", "AB+"), ("AB-", "AB-"),
        ]
    )

    pincode = models.CharField(max_length=6)

 

    @staticmethod
    def can_donate_again(donor):
        last_donation = Marked_as_Donated.objects.filter(donor=donor).order_by("-date_donated").first()
        if last_donation:
            return (date.today() - last_donation.date_donated) >= timedelta(days=90)
        return True


    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"

class Hospital(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    contact_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name.username   # or self.name.get_full_name()


class Marked_as_Donated(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    date_donated = models.DateField(auto_now_add=True)
    marked_by = models.CharField(max_length=255)  # hospital name
    otp = models.CharField(max_length=6, blank=True, null=True)  # store OTP for verification

    def __str__(self):
        return f"{self.donor.user.username} donated on {self.date_donated}"

    @staticmethod
    def can_donate_again(donor):
        last_donation = Marked_as_Donated.objects.filter(donor=donor).order_by("-date_donated").first()
        if last_donation:
            return (date.today() - last_donation.date_donated) >= timedelta(days=90)
        return True

 