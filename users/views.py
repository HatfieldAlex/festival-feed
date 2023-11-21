from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomRegistrationForm, ProfileForm
from django.contrib.auth.models import User
from .models import Profile

def home(request):
    user = request.user
    user_profile = user.profile
    return render(request, 'users/home.html', {"user_profile": user_profile})

def register(request):
    if request.method == 'POST':
        user_form = CustomRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user  # Link the profile to the user
            new_profile.save()
            # Log the user in or redirect them to a login page
            return redirect('login')  # Redirect to a desired URL after successful registration
    else:
        user_form = CustomRegistrationForm()
        profile_form = ProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/register.html', context)


# def register(request):
#     if request.method == 'POST':
#         form = CustomRegistrationForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             return redirect('login')
#     else:
#         form = CustomRegistrationForm()
#     return render(request, 'users/register.html', {"form": form})