from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Faculty
from .forms import FacultyForm, UserRegistrationForm

# ============================
# Faculty Registration
# ============================
def faculty_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            Faculty.objects.create(
                user=user,
                name=user.username,
                promotion_status='Pending'
            )

            messages.success(request, "Registration successful. Please log in.")
            return redirect('faculty_login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserRegistrationForm()
    return render(request, 'core/faculty_register.html', {'user_form': user_form})

# ============================
# Faculty Login
# ============================
def faculty_login(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=username_or_email)
            username = user_obj.username
        except User.DoesNotExist:
            username = username_or_email

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('faculty_dashboard')
        else:
            messages.error(request, "Invalid username/email or password")
    return render(request, "core/faculty_login.html")

# ============================
# Faculty Dashboard
# ============================
@login_required(login_url='faculty_login')
def faculty_dashboard(request):
    faculty = get_object_or_404(Faculty, user=request.user)

    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            faculty = form.save(commit=False)
            faculty.calculate_api_score()  # auto calculate API score
            faculty.save()
            messages.success(request, "Profile updated. API score calculated.")
            return redirect('faculty_dashboard')
    else:
        form = FacultyForm(instance=faculty)

    return render(request, 'core/faculty_dashboard.html', {
        'form': form,
        'faculty': faculty
    })

# ============================
# Faculty Logout
# ============================
def faculty_logout(request):
    logout(request)
    return redirect('faculty_login')

# --------------------
# Admin Login
# --------------------
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Only staff allowed
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials")
    return render(request, "core/admin_login.html")

# --------------------
# Admin Dashboard
# --------------------
def admin_dashboard(request):
    faculties = Faculty.objects.all()
    return render(request, 'core/admin_dashboard.html', {'faculties': faculties})

# --------------------
# Update Promotion Status
# --------------------
def update_promotion_status(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)

    if request.method == "POST":
        promotion_status = request.POST.get("promotion_status")

        # If promoted, update rank
        if promotion_status == "Promoted":
            # Example rank change logic
            if faculty.current_rank == "Assistant Professor":
                faculty.current_rank = "Associate Professor"
            elif faculty.current_rank == "Associate Professor":
                faculty.current_rank = "Professor"
            # You can add more rank progression rules here

        faculty.promotion_status = promotion_status
        faculty.save()
        return redirect('admin_dashboard')

    return render(request, 'core/update_promotion_status.html', {'faculty': faculty})
# ============================
# Admin View Faculty Profile
# ============================
@staff_member_required(login_url='admin_login')
def view_faculty(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    return render(request, 'core/view_faculty.html', {'faculty': faculty})
