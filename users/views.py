from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import CustomRegistrationForm, ProfileForm, LiveEventForm
from django.contrib.auth.models import User
from .models import Profile, LiveEvent

def home(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = user.profile
        return render(request, 'users/home.html', {"user_profile": user_profile})
    else:
        return render(request, 'users/home.html')

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

def user_profile_page(request, username):
    #user = request.user
    user = get_object_or_404(User, username=username)
    user_profile = user.profile
    live_events = LiveEvent.objects.filter(user=user)
    followed_users = user_profile.following.all()
    return render(request, 'users/user_profile_page.html', {
        'user_profile': user_profile, 
        "live_events": live_events, 
        "followed_users": followed_users})

def edit_profile_page(request):

    live_events = LiveEvent.objects.filter(user=request.user)


    if request.method == 'POST':
        form = LiveEventForm(request.POST)
        if form.is_valid():
            live_event = form.save(commit=False)
            live_event.user = request.user
            live_event.save()
            form = LiveEventForm()
            return render(request, 'users/edit_profile_page.html', {"form": form, "live_events": live_events})
    else:
        form = LiveEventForm()
        return render(request, 'users/edit_profile_page.html', {"form": form, "live_events": live_events})
    

def delete_event(request, event_id):
    if request.method == 'POST':
        event = LiveEvent.objects.get(id=event_id)
        event.delete()
        return redirect('edit_profile_page') 
    

def friend_search(request):
    all_users = Profile.objects.all()
    return render(request, 'users/friend_search.html', {"all_users": all_users})

def follow_user(request, username):
    following_user_profile = get_object_or_404(Profile, user=request.user)

    followed_user = get_object_or_404(User, username=username)
    followed_user_profile = get_object_or_404(Profile, user=followed_user)

    following_user_profile.follow(followed_user_profile)
    return redirect('friend_search')

    
def unfollow_user(request, username):
    following_user_profile = get_object_or_404(Profile, user=request.user)

    followed_user = get_object_or_404(User, username=username)
    followed_user_profile = get_object_or_404(Profile, user=followed_user)

    following_user_profile.unfollow(followed_user_profile)
    return redirect('friend_search')