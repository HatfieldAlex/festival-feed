from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import CustomRegistrationForm, ProfileForm, LiveEventForm, UserEventStatusForm, SelectLiveEventForm
from django.contrib.auth.models import User
from .models import Profile, LiveEvent, UserEventStatus

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
    user = get_object_or_404(User, username=username) #this is the user object of the profile
    user_profile = user.profile
    gone_events = UserEventStatus.objects.filter(user=user, status='gone').select_related('live_event')
    going_events = UserEventStatus.objects.filter(user=user, status='going').select_related('live_event')
    want_to_go_events = UserEventStatus.objects.filter(user=user, status='gone').select_related('live_event')
    followed_users = user_profile.following.all()
    user_followers = user_profile.followers.all()

    
    return render(request, 'users/user_profile_page.html', {
        'user_profile': user_profile, 
        "gone_events": gone_events, 
        "want_to_go_events": want_to_go_events,
        "going_events": going_events,
        "followed_users": followed_users,
        "user_followers": user_followers})


def edit_profile_page(request):
    if request.method == 'POST':
        #take the forms from the inputs 
        select_live_event_form = SelectLiveEventForm(request.POST)
        live_event_status_form = UserEventStatusForm(request.POST)

        if select_live_event_form.is_valid() and live_event_status_form.is_valid():
            selected_event = select_live_event_form.cleaned_data['event'] # isolate the selelted event
            live_event_status = live_event_status_form.save(commit=False) #save the event status
            #fill in the remaining parts to the eventstatusobject instance, whcih in turn update the corresponding LiveEvent object
            live_event_status.user = request.user
            live_event_status.live_event = selected_event #updating the event part of the live_event_status
            live_event_status.save()

    

    live_event_status_form = UserEventStatusForm()
    user = request.user
    user_event_statuses = UserEventStatus.objects.filter(user=user).select_related('live_event')
    events_with_details = [{
        'name': event_status.live_event.name,
        'venue': event_status.live_event.venue,
        'year': event_status.live_event.year,
        'status': event_status.status
    } for event_status in user_event_statuses]
    
    #live_events = user.attended_events.all()

    # #setting up a dictionary to add to the context of the status of each festival
    # events_with_status = []

    # for event in live_events:
    #     try:
    #         # Try to get the status of the user for each event
    #         event_status = UserEventStatus.objects.get(user=user, live_event__id=event.id).status
    #     except UserEventStatus.DoesNotExist:
    #         # If there's no status set for an event, you can decide what to do
    #         event_status = 'No status set'  # or None, or any other placeholder

    #     # Add the event and its status to the list
    #     events_with_status.append({'event': event, 'status': event_status})

    select_live_event_form = SelectLiveEventForm()
    
    return render(request, 'users/edit_profile_page.html', {
        "events_with_details": events_with_details,
        #"user_event_statuses": user_event_statuses,
        #"live_events": live_events,
        "event_status_form": live_event_status_form,
        # "events_with_status": events_with_status,
        "select_live_event_form": select_live_event_form,
    })




# def edit_profile_page(request):
#     # # if request.method == 'POST':
#     # #     live_event_form = LiveEventForm(request.POST)
#     # #     live_event_status_form = UserEventStatusForm(request.POST)   
#     # #     if live_event_form.is_valid() and live_event_status_form.is_valid():
#     # #         live_event = live_event_form.save(commit=False)
#     # #         live_event_status = live_event_status_form.save(commit=False)
#     # #         live_event.user = request.user
#     # #         live_event.save()


#     # user = request.user
#     # event_description_form = LiveEventForm()
#     # event_status_form = UserEventStatusForm() 
#     # live_events = user.attended_events.all()
#     # return render(request, 'users/edit_profile_page.html', {
#     #     "live_events": live_events,
#     #     "event_description_form": event_description_form,
#     #     "event_status_form": event_status_form})




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


def add_new_event(request):
    if request.method == 'POST':
        #take the forms from the inputs 
        live_event_form = LiveEventForm(request.POST)

        if live_event_form.is_valid():
            #save the form inputs 
            live_event_form.save()  # Save the live event

    live_event_form = LiveEventForm()
    user = request.user



    return render(request, 'users/add_new_event.html', {
        "live_event_form": live_event_form,
    })




def live_event_search_results(request):
    query = request.GET.get('query', '')
    if query:
        results = LiveEvent.objects.filter(name__icontains=query)
    else:
        results = []

    return render(request, 'users/live_event_search_results.html', {"results": results})

def event_page(request, event_id):
    event = LiveEvent.objects.get(id=event_id)
    return render(request, 'users/event_page.html', {"event": event})