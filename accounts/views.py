from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import CustomUser, OTP, Report
from .forms import OTPForm, ReportForm
import random, string
from datetime import date

def generate_otp():
    return str(random.randint(100000, 999999))

def only_letters(s):
    return ''.join(ch for ch in s if ch.isalpha())

def generate_username_from_name(name):
    base = only_letters(name).lower() or "user"
    base = base[:20]
    username = base
    while CustomUser.objects.filter(username=username).exists():
        username = base + ''.join(random.choice(string.ascii_lowercase) for _ in range(3))
        username = username[:20]
    return username

def generate_temp_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def register(request):
    context = {}
    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        context.update({'name': name, 'email': email, 'phone': phone, 'address': address})

        if action == 'send_otp':
            if not name or not name.replace(' ', '').isalpha():
                messages.error(request, "Name must contain only letters.")
                return render(request, 'accounts/register.html', context)
            if not phone.isdigit():
                messages.error(request, "Phone must contain only numbers.")
                return render(request, 'accounts/register.html', context)
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return render(request, 'accounts/register.html', context)

            username = generate_username_from_name(name)
            temp_password = generate_temp_password(8)

            user = CustomUser.objects.create(
                username=username,
                first_name=name,
                email=email,
                phone=phone,
                address=address,
                is_active=False,
                admin_verified=False,
            )
            user.set_password(temp_password)
            user.save()

            email_code = generate_otp()
            phone_code = generate_otp()
            OTP.objects.create(user=user, otp=email_code, purpose='email_verification')
            OTP.objects.create(user=user, otp=phone_code, purpose='phone_verification')

            print("EMAIL OTP:", email_code)
            print("PHONE OTP:", phone_code)

            context['otp_sent'] = True
            context['user_id'] = user.id
            request.session['temp_username'] = username
            request.session['temp_password'] = temp_password
            messages.success(request, "OTPs generated (see terminal). Enter both OTPs to complete registration.")
            return render(request, 'accounts/register.html', context)

        if action == 'register':
            user_id = request.POST.get('user_id')
            email_otp = request.POST.get('email_otp', '').strip()
            phone_otp = request.POST.get('phone_otp', '').strip()
            user = get_object_or_404(CustomUser, id=user_id)

            email_ok = OTP.objects.filter(user=user, otp=email_otp, purpose='email_verification').exists()
            phone_ok = OTP.objects.filter(user=user, otp=phone_otp, purpose='phone_verification').exists()

            if not email_ok or not phone_ok:
                messages.error(request, "Invalid OTP(s).")
                context['otp_sent'] = True
                context['user_id'] = user_id
                return render(request, 'accounts/register.html', context)

            user.email_verified = True
            user.phone_verified = True
            user.admin_verified = True
            user.is_active = True
            user.status = 'approved'
            user.save()

            OTP.objects.filter(user=user).delete()

            request.session['reg_number'] = user.registration_number
            request.session['temp_username'] = request.session.get('temp_username')
            request.session['temp_password'] = request.session.get('temp_password')

            return redirect('success')

    return render(request, 'accounts/register.html', context)

def success(request):
    reg_number = request.session.pop('reg_number', None)
    temp_username = request.session.pop('temp_username', None)
    temp_password = request.session.pop('temp_password', None)
    return render(request, 'accounts/success.html', {
        'registration_number': reg_number,
        'temp_username': temp_username,
        'temp_password': temp_password
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_blocked:
                messages.error(request, "Your account has been blocked by admin.")
                return render(request, 'accounts/login.html')
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login_view')

@login_required(login_url='login_view')
def dashboard(request):
    user = request.user
    if user.is_blocked:
        messages.error(request, "Your account is blocked.")
        return redirect('login_view')

    reports = user.reports.all()
    return render(request, 'accounts/dashboard.html', {
        'user': user,
        'reports': reports,
        'today': date.today()
    })

@login_required(login_url='login_view')
@require_http_methods(["POST"])
def change_username(request):
    user = request.user
    new_username = request.POST.get('new_username', '').strip()
    if not new_username.isalpha():
        messages.error(request, "Username must contain only letters!")
        return redirect('dashboard')
    if CustomUser.objects.filter(username=new_username).exists():
        messages.error(request, "Username already taken!")
        return redirect('dashboard')
    user.username = new_username
    user.save()
    messages.success(request, "Username updated successfully!")
    return redirect('dashboard')

@login_required(login_url='login_view')
@require_http_methods(["POST"])
def change_password(request):
    user = request.user
    old_password = request.POST.get('old_password')
    new_password1 = request.POST.get('new_password1')
    new_password2 = request.POST.get('new_password2')
    if not user.check_password(old_password):
        messages.error(request, "Old password is incorrect!")
        return redirect('dashboard')
    if new_password1 != new_password2:
        messages.error(request, "New passwords do not match!")
        return redirect('dashboard')
    if len(new_password1) < 6:
        messages.error(request, "Password must be at least 6 characters!")
        return redirect('dashboard')
    user.set_password(new_password1)
    user.save()
    messages.success(request, "Password changed successfully!")
    return redirect('dashboard')

@login_required(login_url='login_view')
def change_email(request):
    user = request.user
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'send_otp':
            new_email = request.POST.get('new_email', '').strip()
            if CustomUser.objects.filter(email=new_email).exclude(id=user.id).exists():
                messages.error(request, "Email already registered!")
                return redirect('change_email')
            otp = generate_otp()
            OTP.objects.create(user=user, otp=otp, purpose='email_verification')
            print("EMAIL OTP:", otp)
            request.session['pending_email'] = new_email
            messages.success(request, "OTP sent! Check terminal.")
            return render(request, 'accounts/change_email.html', {'otp_sent': True})
        if action == 'verify':
            otp = request.POST.get('otp', '').strip()
            new_email = request.session.get('pending_email')
            if not OTP.objects.filter(user=user, otp=otp, purpose='email_verification').exists():
                messages.error(request, "Invalid OTP!")
                return render(request, 'accounts/change_email.html', {'otp_sent': True})
            user.email = new_email
            user.email_verified = True
            user.save()
            OTP.objects.filter(user=user, purpose='email_verification').delete()
            del request.session['pending_email']
            messages.success(request, "Email changed successfully!")
            return redirect('dashboard')
    return render(request, 'accounts/change_email.html')

@login_required(login_url='login_view')
def change_phone(request):
    user = request.user
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'send_otp':
            new_phone = request.POST.get('new_phone', '').strip()
            if not new_phone.isdigit():
                messages.error(request, "Phone must contain only numbers!")
                return redirect('change_phone')
            if CustomUser.objects.filter(phone=new_phone).exclude(id=user.id).exists():
                messages.error(request, "Phone already registered!")
                return redirect('change_phone')
            otp = generate_otp()
            OTP.objects.create(user=user, otp=otp, purpose='phone_verification')
            print("PHONE OTP:", otp)
            request.session['pending_phone'] = new_phone
            messages.success(request, "OTP sent! Check terminal.")
            return render(request, 'accounts/change_phone.html', {'otp_sent': True})
        if action == 'verify':
            otp = request.POST.get('otp', '').strip()
            new_phone = request.session.get('pending_phone')
            if not OTP.objects.filter(user=user, otp=otp, purpose='phone_verification').exists():
                messages.error(request, "Invalid OTP!")
                return render(request, 'accounts/change_phone.html', {'otp_sent': True})
            user.phone = new_phone
            user.phone_verified = True
            user.save()
            OTP.objects.filter(user=user, purpose='phone_verification').delete()
            del request.session['pending_phone']
            messages.success(request, "Phone changed successfully!")
            return redirect('dashboard')
    return render(request, 'accounts/change_phone.html')

@login_required(login_url='login_view')
def change_address(request):
    user = request.user
    if request.method == 'POST':
        new_address = request.POST.get('new_address', '').strip()
        user.pending_address = new_address
        user.save()
        # auto-approve pending_address immediately
        if user.pending_address:
            user.address = user.pending_address
            user.pending_address = ""
            user.save()
        messages.success(request, "Address updated (auto-approved).")
        return redirect('dashboard')
    return render(request, 'accounts/change_address.html')

@login_required(login_url='login_view')
def submit_report(request):
    user = request.user
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = user
            report.save()
            messages.success(request, "Report submitted successfully!")
            return redirect('my_reports')
    else:
        form = ReportForm(initial={'report_date': date.today()})
    return render(request, 'accounts/submit_report.html', {'form': form, 'today': date.today()})

@login_required(login_url='login_view')
def my_reports(request):
    user = request.user
    reports = user.reports.all()
    return render(request, 'accounts/my_reports.html', {'reports': reports})