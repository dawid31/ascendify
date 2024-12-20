from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile, TextChannel, Message, Route, Event
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.models import User
import requests
from .forms import LocationForm, EventForm
from dotenv import load_dotenv
import os

def index(request):
    return render(request, 'ascendify_app/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Login failed. Check fields and try again.')

    return render(request, 'ascendify_app/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            auth_login(request, user)  # Automatically log in the user after registration
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'ascendify_app/register.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request, user_id=None):
    if user_id:
        profile_user = get_object_or_404(User, id=user_id)
    else:
        profile_user = request.user

    profile = get_object_or_404(Profile, user=profile_user)
    
    # Extract data from climbing_stats
    climbing_stats = profile.climbing_stats if profile.climbing_stats else {}
    completed_routes = climbing_stats.get('completed_routes', 'N/A')
    highest_grade = climbing_stats.get('highest_grade', 'N/A')
    experience_level = climbing_stats.get('experience_level', 'N/A')

    context = {
        'user': profile_user,
        'profile': profile,
        'completed_routes': completed_routes,
        'highest_grade': highest_grade,
        'experience_level': experience_level,
    }
    return render(request, 'ascendify_app/new_profile.html', context)




@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('index')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'ascendify_app/edit_profile.html', context)


@login_required
def forum(request):
    """View to list all text channels."""
    text_channels = TextChannel.objects.prefetch_related('messages').all()
    return render(request, 'ascendify_app/forum.html', {'text_channels': text_channels})

@login_required
def channel_discussion_view(request, channel_id):
    """View to display the full discussion for a specific text channel."""
    channel = get_object_or_404(TextChannel, id=channel_id)
    return render(request, 'ascendify_app/channel_discussion.html', {'channel': channel})

@login_required
def send_message(request, channel_id):
    """View to handle sending a new message to a text channel."""
    channel = get_object_or_404(TextChannel, id=channel_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(author=request.user, channel=channel, content=content)
            return HttpResponseRedirect(reverse('channel_discussion', args=[channel.id]))  # Redirect to the discussion view

    return redirect('channel_discussion', channel_id=channel.id)  # Redirect back to the channel if not a POST request

def search(request):
    query = request.GET.get('q')
    if query:
        # Search across Route, TextChannel, and Event models
        routes = Route.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        )
        communities = TextChannel.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        events = Event.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        )
        messages = Message.objects.filter(
            Q(content__icontains=query) | Q(author__username__icontains=query) | Q(channel__name__icontains=query))
    else:
        routes = communities = events = messages = []

    context = {
        'routes': routes,
        'communities': communities,
        'events': events,
        'query': query,
        'messages': messages
    }
    return render(request, 'ascendify_app/search_results.html', context)




def community(request):
    return render(request, 'ascendify_app/community.html')


def event_list(request):
    events = Event.objects.all()
    return render(request, 'ascendify_app/events_list.html', {'events': events})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('events')
    else:
        form = EventForm()
    
    return render(request, 'ascendify_app/create_event.html', {'form': form})

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user not in event.attendees.all():
        event.attendees.add(request.user)
    return redirect('events')


@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user in event.attendees.all():
        event.attendees.remove(request.user)
    return redirect('events')


def find_indoor_spots(request):
    spots = []
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data.get('city')
            
            # Google Geocoding API call
            geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={api_key}'
            geocode_response = requests.get(geocode_url).json()

            if geocode_response.get('results'):
                location = geocode_response['results'][0]['geometry']['location']
                latitude = location['lat']
                longitude = location['lng']

                # Google Places API call to find bouldering spots
                places_url = (
                    f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
                    f'?location={latitude},{longitude}'
                    f'&keyword=bouldering'
                    f'&rankby=distance'
                    f'&key={api_key}'
                )
                places_response = requests.get(places_url).json()
                spots = places_response.get('results', [])

    else:
        form = LocationForm()

    return render(request, 'ascendify_app/find_indoor_spots.html', {'form': form, 'spots': spots, 'api_key': api_key})


def find_outdoor_spots(request):
    spots = []
    load_dotenv()
    form = LocationForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        region = form.cleaned_data.get('city')  # Assume 'city' field is used for region search
        
        query = {
            'query': f"""
            query {{
              areas(filter: {{area_name: {{match: "{region}"}}}}) {{
                area_name
                children {{
                  area_name
                  metadata {{
                    lat
                    lng
                  }}
                  media {{
                    mediaUrl
                  }}
                }}
              }}
            }}
            """
        }

        openbeta_api_url = "https://api.openbeta.io/graphql"
        headers = {"Content-Type": "application/json"}
        response = requests.post(openbeta_api_url, json=query, headers=headers).json()
        
        areas = response['data']['areas'] if response.get('data') else []
        for area in areas:
            for child in area.get('children', []):
                # Only add spots that have media
                if child.get('media'):
                    media_url = f"https://media.openbeta.io{child['media'][0]['mediaUrl']}"
                    spots.append({
                        'name': child['area_name'],
                        'lat': child['metadata']['lat'],
                        'lng': child['metadata']['lng'],
                        'image': media_url
                    })

    return render(request, 'ascendify_app/find_outdoor_spots.html', {'form': form, 'spots': spots})

pattern = 'https://media.openbeta.io' + 'mediaUrl'
'''np. https://media.openbeta.io /u/6fd95718-8fe1-4adb-a140-3e5565f8a7b4/QGHfwkzgWn.jpg'''