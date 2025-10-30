import random
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings

from .forms import DonorSignupForm


# Step 1: Signup -> Generate OTP
def donor_signup(request):
    if request.method == "POST":
        form = DonorSignupForm(request.POST)
        if form.is_valid():
            # Temporarily store user data in session (not saved in DB yet)
            request.session['signup_data'] = form.cleaned_data

            # Generate OTP
            otp = str(random.randint(100000, 999999))
            print("otp:",otp)
            request.session['otp'] = otp

            # Send OTP to donor's email
            send_mail(
                "Donor Signup OTP Verification from Emergency Blood Alert",
                f"Your OTP is {otp}",
                settings.DEFAULT_FROM_EMAIL,
                [form.cleaned_data["email"]],
                fail_silently=False,
            )

            return redirect("verify_otp")
    else:
        form = DonorSignupForm()
    return render(request, "donor_signup.html", {"form": form})


# Step 2: OTP Verification
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")
        signup_data = request.session.get("signup_data")

        if entered_otp == session_otp and signup_data:
            # Create User + Donor only after OTP is correct
            form = DonorSignupForm(signup_data)
            if form.is_valid():
                user = form.save()

                # Auto login donor
                login(request, user)

                # Clear session
                request.session.pop("otp", None)
                request.session.pop("signup_data", None)

                return redirect("home")  # Redirect to home after signup
        else:
            return render(request, "verify_otp.html", {"error": "Invalid OTP"})

    return render(request, "verify_otp.html")

def home(request):
    return render(request, "home.html")

# from django.shortcuts import render
# from .models import Donor

# def hospital_dashboard(request):
#     donors = Donor.objects.all()

#     # Filtering
#     blood_group = request.GET.get('blood_group')
#     pincode = request.GET.get('pincode')
#     search = request.GET.get('search')

#     if blood_group and blood_group != "All":
#         donors = donors.filter(blood_group=blood_group)
#     if pincode:
#         donors = donors.filter(pincode=pincode)
#     if search:
#         donors = donors.filter(user__username__icontains=search)

#     # Sorting
#     sort_by = request.GET.get('sort_by')
#     if sort_by in ['age', 'blood_group', 'pincode']:
#         donors = donors.order_by(sort_by)

#     return render(request, "hospital_dashboard.html", {
#         "donors": donors,
#         "selected_blood_group": blood_group or "All",
#         "search_query": search or "",
#         "sort_by": sort_by or "",
#     })

# from django.shortcuts import redirect, get_object_or_404
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib import messages

# def send_email_to_donor(request, user_id):
#     if request.method == "POST":
#         user = get_object_or_404(User, id=user_id)
#         email = user.email

#         # Send email
#         send_mail(
#             "Alert Blood Bank Notification",
#             f"Hello {user.username}, this is a notification from the Blood Bank.",
#             "if you intersted",
#             "call:XXXXX XXXXX",
#             settings.DEFAULT_FROM_EMAIL,
#             [email],
#             fail_silently=False,
#         )
#         messages.success(request, f"Email sent to {user.username}")
#     return redirect('hospital_dashboard')

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from .models import Hospital

def send_email_to_donor(request, user_id, hospital_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        email = user.email

        # If hospital_id is the User.id (owner of hospital account)
        hospital = get_object_or_404(Hospital, name__id=hospital_id)

        subject = "Alert Blood Bank Notification"
        message = (
            f"Hello {user.username},\n\n"
            f"This is a notification from the Blood Bank.\n"
            f"Hospital Name: {hospital.name.username}\n"
            f"If you are interested, please call: {hospital.contact_number}\n"
            f"And visit the address: {hospital.address}.\n\n"
            "Thank you!"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        messages.success(request, f"Email sent to {user.username}")

    return redirect('hospital_dashboard')


# def send_email_to_donor(request, user_id, hospital_id):
#     if request.method == "POST":
#         user = get_object_or_404(User, id=user_id)
#         email = user.email
#         hospital = get_object_or_404(Hospital, id=hospital_id)

#         subject = "Alert Blood Bank Notification"
#         message = (
#             f"Hello {user.username},\n\n"
#             f"This is a notification from the Blood Bank.\n"
#             f"Hospital Name: {hospital.username}\n"
#             f"If you are interested, please call: {hospital.contact_number}\n\n"
#             f"And visit address{hospital.address}.\n"
#             "Thank you!"
#         ) 

#         send_mail(
#             subject,
#             message,
#             settings.DEFAULT_FROM_EMAIL,
#             [email],
#             fail_silently=False,
#         )

#         messages.success(request, f"Email sent to {user.username}")

#     return redirect('hospital_dashboard')


 


# def hospital_login(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("hospital_dashboard")
#         else:
#             return render(request, "hospital_login.html", {"error": "Invalid credentials"})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import HospitalSignupForm

def hospital_signup(request):
    if request.method == "POST":
        form = HospitalSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hospital registered successfully! You can now log in.")
            return redirect("login")  # redirect to your login page
    else:
        form = HospitalSignupForm()
    return render(request, "hospital_signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)   # log the user in
            messages.success(request, f"Welcome {user.username}!")
            return redirect("hospital_dashboard")   # redirect to your home/dashboard page
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")
    
    return render(request, "hospital_login.html")


import random
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from .models import Donor, Marked_as_Donated

# def send_otp_to_donor(request, donor_id):
#     donor = get_object_or_404(Donor, user_id=donor_id)

#     # Check eligibility (90 days rule)
#     if not Marked_as_Donated.can_donate_again(donor):
#         messages.error(request, "Donor cannot donate again before 90 days.")
#         return redirect("hospital_dashboard")

#     otp = str(random.randint(100000, 999999))

#     # Send email
#     send_mail(
#         "Donation OTP Verification",
#         "Donor cannot donate again before 90 days",
#         f{{ Hospital }}"request.user.username",
#         f{{ contact_number }}"request.user.phone_number",
#         f"Dear {donor.user.username},\n\nYour OTP for marking donation is {otp}.",
#         "yourhospital@example.com",
#         [donor.user.email],
#         fail_silently=False,
#     )

#     # Temporarily store OTP in session
#     request.session["donor_otp"] = otp
#     request.session["donor_id"] = donor.id

#     messages.info(request, f"OTP sent to {donor.user.email}")
#     return redirect("verify_donation_otp")


import random
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Donor, Marked_as_Donated, Hospital

def send_otp_to_donor(request, donor_id):
    donor = get_object_or_404(Donor, user_id=donor_id)

    # Check eligibility (90 days rule)
    if not Marked_as_Donated.can_donate_again(donor):
        messages.error(request, "Donor cannot donate again before 90 days.")
        return redirect("hospital_dashboard")

    # Generate OTP
    otp = str(random.randint(100000, 999999))

    # Get hospital info (assuming hospital is linked to logged-in user)
    try:
        hospital = Hospital.objects.get(name=request.user)
    except Hospital.DoesNotExist:
        hospital = None

    # Email content
    subject = "Blood Donation OTP Verification"
    message = f"""
Dear {donor.user.username},

Thank you for your willingness to donate blood at {hospital.name if hospital else "our hospital"}.

Your One-Time Password (OTP) for confirming this donation is: {otp}

⚠️ Please note: A donor is not eligible to donate again within 90 days of the last donation.

If you did not initiate this request, please contact us immediately at {hospital.contact_number if hospital else "our helpline"}.

Best regards,  
{hospital.name if hospital else "Hospital Team"}
"""

    # Send email
    send_mail(
        subject,
        message.strip(),
        "yourhospital@example.com",  # official hospital email
        [donor.user.email],
        fail_silently=False,
    )

    # Store OTP in session
    request.session["donor_otp"] = otp
    request.session["donor_id"] = donor.id

    messages.info(request, f"OTP sent to {donor.user.email}")
    return redirect("verify_donation_otp")


def verify_donation_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        donor_id = request.session.get("donor_id")
        donor = get_object_or_404(Donor, id=donor_id)

        if entered_otp == request.session.get("donor_otp"):
            # Save donation record
            Marked_as_Donated.objects.create(
                donor=donor,
                marked_by=request.user.username,  # hospital user
                otp=entered_otp,
            )
            messages.success(request, f"{donor.user.username} marked as donated.")
            # Clear OTP session
            del request.session["donor_otp"]
            del request.session["donor_id"]
            return redirect("hospital_dashboard")
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "verify_donation_otp.html")

from django.shortcuts import render
from .models import Donor

# def hospital_dashboard(request):
#     donors = Donor.objects.all()

#     # Filtering
#     blood_group = request.GET.get('blood_group')
#     pincode = request.GET.get('pincode')
#     search = request.GET.get('search')

#     if blood_group and blood_group != "All":
#         donors = donors.filter(blood_group=blood_group)
#     if pincode:
#         donors = donors.filter(pincode=pincode)
#     if search:
#         donors = donors.filter(user__username__icontains=search)

#     # Sorting
#     sort_by = request.GET.get('sort_by')
#     if sort_by in ['age', 'blood_group', 'pincode']:
#         donors = donors.order_by(sort_by)

#     # ✅ Add eligibility check for each donor
#     donor_data = []
#     for donor in donors:
#         donor_data.append({
#             "donor": donor,
#             "can_donate": Donor.can_donate_again(donor)
#         })

#     return render(request, "hospital_dashboard.html", {
#         "donors": donor_data,
#         "selected_blood_group": blood_group or "All",
#         "search_query": search or "",
#         "sort_by": sort_by or "",
#     })
def hospital_dashboard(request):
    donors = Donor.objects.all()

    # Get filters
    blood_group = request.GET.get('blood_group')
    pincode = request.GET.get('pincode')
    search = request.GET.get('search')
    sort_by = request.GET.get('sort_by')

    # Apply filters
    if blood_group and blood_group != "All":
        donors = donors.filter(blood_group=blood_group)
    if pincode:
        donors = donors.filter(pincode=pincode)
    if search:
        donors = donors.filter(user__username__icontains=search)

    # Apply sorting
    if sort_by in ['age', 'blood_group', 'pincode']:
        donors = donors.order_by(sort_by)

    # ✅ Build donor data list with eligibility
    donor_data = []
    for donor in donors:
        can_donate = Donor.can_donate_again(donor)
        donor_data.append({
            "donor": donor,
            "can_donate": can_donate
        })

    # ✅ Remove not eligible donors if user applied blood group or pincode filter
    if (blood_group and blood_group != "All") or pincode:
        donor_data = [d for d in donor_data if d["can_donate"]]

    return render(request, "hospital_dashboard.html", {
        "donors": donor_data,
        "selected_blood_group": blood_group or "All",
        "search_query": search or "",
        "sort_by": sort_by or "",
    })


from django.shortcuts import render, get_object_or_404
from .models import Donor, Marked_as_Donated

def donation_history(request, donor_id):
    donor = get_object_or_404(Donor, user_id=donor_id)
    history = Marked_as_Donated.objects.filter(donor=donor).order_by("-date_donated")

    return render(request, "donation_history.html", {
        "donor": donor,
        "history": history,
    })

from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from .models import Donor, Marked_as_Donated

def send_email_to_filtered(request):
    if request.method == "POST":
        blood_group = request.POST.get("blood_group")
        pincode = request.POST.get("pincode")
        search = request.POST.get("search")

        donors = Donor.objects.all()

        # Apply filters
        if blood_group and blood_group != "All":
            donors = donors.filter(blood_group=blood_group)
        if pincode:
            donors = donors.filter(pincode=pincode)
        if search:
            donors = donors.filter(user__username__icontains=search)

        # Exclude not eligible (90 days rule)
        eligible_donors = [d for d in donors if Marked_as_Donated.can_donate_again(d)]

        if not eligible_donors:
            messages.warning(request, "No eligible donors found for this filter.")
            return redirect("hospital_dashboard")

        # Collect emails
        recipient_list = [d.user.email for d in eligible_donors if d.user.email]

        # Send email (bulk message)
        send_mail(
            subject="Urgent Blood Donation Request",
            message="Dear donor,\n\nWe are in urgent need of blood donations. "
                    "If you are eligible, kindly visit the hospital at the earliest.\n\nThank you!",
            from_email="yourhospital@example.com",
            recipient_list=recipient_list,
            fail_silently=False,
        )

        messages.success(request, f"Email sent to {len(recipient_list)} eligible donors.")
        return redirect("hospital_dashboard")

    return redirect("hospital_dashboard")


def about(request):
    return render(request, "enterance.html")

'''
emergency blood fetcher management system  this project contain donar regestration form filed like name,age,blood_group,email,pin code,email otp and hospital restration for conatian hospital name ,address,pin code,phone number ,password after registraion hospital can login hospital dashbord home appear donar name pincode age blood_group,send email for blood request,marks donate reveice manual otp from donar for conformation of donate blood and mute 90 in this id history  button contain bolld donation records hospital name  '''