from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User, Group
from chat.models import Ticket
from core.models import UserProfile


def home(request):
    """
    Renders the home page.
    """
    return render(request, 'home.html')


def user_login(request):
    """
    Logs the user in and redirects them to the home page if they have submitted the login form
    successfully. Otherwise just renders the login page.
    """

    # We capture the page that the user was trying to access, so that
    # we can redirect them to it if they login successfully.
    if request.method == 'GET':
        next = request.GET.get('next')


    # If the user has just submitted the login form
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next = request.GET.get('next')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next) if next else HttpResponseRedirect(reverse('core.views.dashboard'))
            else:
                return render(request, 'login.html', {'account_deleted': True})
        else:
            return render(request, 'login.html', {'login_invalid': True})
    else:  # If the user is just looking to view the login page (hasn't submitted form)
        return render(request, 'login.html', {'next': next})


def user_logout(request):
    """
    Logs the user out and renders the home page with a message informing them that
    they've just logged out.
    """
    logout(request)
    return render(request, 'home.html', {'just_logged_out': True})


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html', {'register_success': True})
        else:
            return render(request, 'register.html', {'form': form})

    args = {}
    args.update(csrf(request))

    args['form'] = UserCreationForm()

    return render_to_response('register.html', args)


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user = user)
    return render(request, 'user_profile.html', {'user': user,
                                                 'userProfile': profile})


@login_required
@permission_required("is_superuser")
def user_permission_change(request, username):
    user = User.objects.get(username=username)
    if request.method == "POST":
        group = request.POST['choice']
        user.groups.add(Group.objects.get(name=group))
    else:
        print "Hello, error! This should only be called on a POST request."

    return render(request, 'user_permissions.html', {'user':user,
                                                     'userProfile': UserProfile.objects.get(user=user)})




def sidebar_ticket_list(request, project_id):
    """
    From the project_id and the logged in user we can generate the list of tickets
    that the user can see. Returns a rendered template of a list of tickets which
    is dynamically injected into the sidebar using Ajax.
    """
    tickets = Ticket.objects.query()
    return render(request, 'ajax/dashboard/sidebar_ticket_list.html', {'tickets': tickets})
