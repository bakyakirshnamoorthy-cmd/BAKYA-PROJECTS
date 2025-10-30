from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Donor


# class DonorSignupForm(UserCreationForm):
#     # Extra fields for donor
#     email = forms.EmailField(required=True)
#     age = forms.IntegerField(required=True)
#     gender = forms.ChoiceField(
#         choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
#         required=True
#     )
#     contact_number = forms.CharField(max_length=15, required=True)
#     blood_group = forms.ChoiceField(
#         choices=[
#             ("A+", "A+"), ("A-", "A-"),
#             ("B+", "B+"), ("B-", "B-"),
#             ("O+", "O+"), ("O-", "O-"),
#             ("AB+", "AB+"), ("AB-", "AB-"),
#         ],
#         required=True
#     )
#     pincode = forms.CharField(max_length=6, required=True)

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ("username", "email")

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data["email"]

#         user.set_unusable_password()

#         if commit:
#             user.save()
#             Donor.objects.create(
#                 user=user,
#                 age=self.cleaned_data["age"],
#                 gender=self.cleaned_data["gender"],
#                 contact_number=self.cleaned_data["contact_number"],
#                 blood_group=self.cleaned_data["blood_group"],
#                 pincode=self.cleaned_data["pincode"],
#             )
#         return user

# class DonorSignupForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     age = forms.IntegerField(required=True)
#     gender = forms.ChoiceField(
#         choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
#         required=True
#     )
#     contact_number = forms.CharField(max_length=15, required=True)
#     blood_group = forms.ChoiceField(
#         choices=[
#             ("A+", "A+"), ("A-", "A-"),
#             ("B+", "B+"), ("B-", "B-"),
#             ("O+", "O+"), ("O-", "O-"),
#             ("AB+", "AB+"), ("AB-", "AB-"),
#         ],
#         required=True
#     )
#     pincode = forms.CharField(max_length=6, required=True)

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ("username", "email")  # password fields ignored

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # 🚫 remove password fields from form
#         self.fields.pop('password1', None)
#         self.fields.pop('password2', None)

#     def save(self, commit=True):
#         user = super(UserCreationForm, self).save(commit=False)
#         user.email = self.cleaned_data["email"]
#         user.set_unusable_password()  # no password assigned

#         if commit:
#             user.save()
#             Donor.objects.create(
#                 user=user,
#                 age=self.cleaned_data["age"],
#                 gender=self.cleaned_data["gender"],
#                 contact_number=self.cleaned_data["contact_number"],
#                 blood_group=self.cleaned_data["blood_group"],
#                 pincode=self.cleaned_data["pincode"],
#             )
#         return user
class DonorSignupForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        required=True
    )
    contact_number = forms.CharField(max_length=15, required=True)
    blood_group = forms.ChoiceField(
        choices=[
            ("A+", "A+"), ("A-", "A-"),
            ("B+", "B+"), ("B-", "B-"),
            ("O+", "O+"), ("O-", "O-"),
            ("AB+", "AB+"), ("AB-", "AB-"),
        ],
        required=True
    )
    pincode = forms.CharField(max_length=6, required=True)

    class Meta:
        model = User
        fields = ("username", "email")  # password fields ignored

    def save(self, commit=True):
        user = super(forms.ModelForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_unusable_password()

        if commit:
            user.save()
            Donor.objects.create(
                user=user,
                age=self.cleaned_data["age"],
                gender=self.cleaned_data["gender"],
                contact_number=self.cleaned_data["contact_number"],
                blood_group=self.cleaned_data["blood_group"],
                pincode=self.cleaned_data["pincode"],
            )
        return user


from django.shortcuts import render, redirect
from django.contrib import messages

from django import forms
from django.contrib.auth.models import User
from .models import Hospital

class HospitalSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Hospital
        fields = ['address', 'contact_number']

    def save(self, commit=True):
        # Create User first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        # Link User with Hospital
        hospital = super().save(commit=False)
        hospital.name = user
        if commit:
            hospital.save()
        return hospital
