# crm_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Role, Teacher, CustomField
from .forms import UserRegistrationForm, UserLoginForm, CustomFieldForm

# Registration view
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# Login view
def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

# Logout view
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('/login')

# Home view (dashboard)
login_required
def home(request):
    return render(request, 'crm_app/home.html')

# User List view (for admin/senior teacher)
# @login_required
# def user_list(request):
#     if request.user.teacher.role.name == 'Admin':  # Assuming 'Admin' is the role for senior teachers
#         users = Teacher.objects.all()
#         return render(request, 'crm_app/user_list.html', {'users': users})
#     else:
#         messages.error(request, 'Access denied. Only senior teachers can view user list.')
#         return redirect('/home')
# @login_required
# def user_list(request):
#     try:
#         if request.user.teacher.role.name == 'Admin':
#             users = Teacher.objects.all()
#             return render(request, 'crm_app/user_list.html', {'users': users})
#     except Teacher.DoesNotExist:
#         print("Teacher Does Not Exist")

#     messages.error(request, 'Access denied. Only senior teachers can view user list.')
#     return redirect('/')
# from django.contrib.auth.decorators import login_required

@login_required
def user_list(request):
    users = Teacher.objects.all()
    print(f"Number of users: {users.count()}")
    return render(request, 'crm_app/user_list.html', {'users': users})

# User Detail view (for admin/senior teacher)
@login_required
def user_detail(request, user_id):
    user = get_object_or_404(Teacher, pk=user_id)
    if request.user.teacher.role.name == 'Admin' or request.user == user:  # Admin or user can view their own details
        return render(request, 'crm_app/user_detail.html', {'user': user})
    else:
        messages.error(request, 'Access denied. Only senior teachers and the user can view user details.')
        return redirect('/')

# Create Dynamic Field view (for admin/senior teacher)
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden

@login_required
def create_dynamic_field(request):
    try:
        teacher = request.user.teacher  # Try to access the teacher relationship
        if teacher.role.name == 'Sr Teacher':  # Assuming 'Admin' is the role for senior teachers
            if request.method == 'POST':
                form = CustomFieldForm(request.POST)
                if form.is_valid():
                    custom_field = form.save()
                    messages.success(request, 'Custom field created successfully.')
                    return redirect('home')
            else:
                form = CustomFieldForm()
            return render(request, 'crm_app/create_dynamic_field.html', {'form': form})
        else:
            messages.error(request, 'Access denied. Only senior teachers can create dynamic fields.')
            return redirect('home')
    except ObjectDoesNotExist:
        messages.error(request, 'User has no teacher. Please contact the administrator to set up your account.')
        return HttpResponseForbidden('Access forbidden: User has no teacher relationship.')

# @login_required
# def create_dynamic_field(request):
#     try:
#         if request.user.teacher.role.name == 'Admin':  # Assuming 'Admin' is the role for senior teachers
#             if request.method == 'POST':
#                 form = CustomFieldForm(request.POST)
#                 if form.is_valid():
#                     custom_field = form.save()
#                     messages.success(request, 'Custom field created successfully.')
#                     return redirect('home')
#             else:
#                 form = CustomFieldForm()
#             return render(request, 'crm_app/create_dynamic_field.html', {'form': form})
#     except ObjectDoesNotExist:
#         pass 
    
#     messages.error(request, 'Access denied. Only senior teachers can create dynamic fields.')
#     return redirect('/')

# @login_required
# def create_dynamic_field(request):
#     if request.user.teacher.role.name == 'Admin':  # Assuming 'Admin' is the role for senior teachers
#         if request.method == 'POST':
#             form = CustomFieldForm(request.POST)
#             if form.is_valid():
#                 custom_field = form.save()
#                 messages.success(request, 'Custom field created successfully.')
#                 return redirect('/home')
#         else:
#             form = CustomFieldForm()
#         return render(request, 'crm_app/create_dynamic_field.html', {'form': form})
#     else:
#         messages.error(request, 'Access denied. Only senior teachers can create dynamic fields.')
#         return redirect('/home')

# Edit Dynamic Field view (for admin/senior teacher)
@login_required
def edit_dynamic_field(request, field_id):
    if request.user.teacher.role.name == 'Admin':  # Assuming 'Admin' is the role for senior teachers
        custom_field = get_object_or_404(CustomField, pk=field_id)
        if request.method == 'POST':
            form = CustomFieldForm(request.POST, instance=custom_field)
            if form.is_valid():
                form.save()
                messages.success(request, 'Custom field updated successfully.')
                return redirect('/home')
        else:
            form = CustomFieldForm(instance=custom_field)
        return render(request, 'crm_app/edit_dynamic_field.html', {'form': form, 'custom_field': custom_field})
    else:
        messages.error(request, 'Access denied. Only senior teachers can edit dynamic fields.')
        return redirect('/home')

# Delete Dynamic Field view (for admin/senior teacher)
@login_required
def delete_dynamic_field(request, field_id):
    if request.user.teacher.role.name == 'Admin':  # Assuming 'Admin' is the role for senior teachers
        custom_field = get_object_or_404(CustomField, pk=field_id)
        if request.method == 'POST':
            custom_field.delete()
            messages.success(request, 'Custom field deleted successfully.')
            return redirect('/home')
        return render(request, 'crm_app/delete_dynamic_field.html', {'custom_field': custom_field})
    else:
        messages.error(request, 'Access denied. Only senior teachers can delete dynamic fields.')
        return redirect('/home')
