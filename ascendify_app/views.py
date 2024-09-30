from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile, TextChannel, Message
from django.urls import reverse
from django.http import HttpResponseRedirect

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
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    # Extract data from climbing_stats (assuming keys like 'completed_routes' and 'highest_grade' exist)
    climbing_stats = profile.climbing_stats if profile.climbing_stats else {}
    completed_routes = climbing_stats.get('completed_routes', 'N/A')
    highest_grade = climbing_stats.get('highest_grade', 'N/A')
    experience_level = climbing_stats.get('experience_level', 'N/A')
    
    context = {
        'user': request.user,
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
            return redirect('profile')

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

def find_spots(request):
    return render(request, 'ascendify_app/find_spots.html')


def community(request):
    return render(request, 'ascendify_app/community.html')


def events(request):
    return render(request, 'ascendify_app/events.html')