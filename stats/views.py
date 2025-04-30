from stats.models import UserProfile, SleeperUser, League, Season
from django.shortcuts import render, redirect
from stats import TITLE, VERSION, AUTHOR
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import NewSleeperUserForm

def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'stats/home.html', {})


def tables(request, league):
    # This dictionary passes league to the 'league' component in the dash app
    league_table = League.objects.get(nickname=league)
    years = Season.objects.values_list('year', flat=True).filter(
        league=league_table)
    initial_arguments = {'league': {'data': league}}
    context = {
        'title': TITLE,
        'version': VERSION,
        'author': AUTHOR,
        'initial_arguments': initial_arguments,
        'league': league,
        'avatar': league_table.avatar,
        'min_year': min(years),
        'max_year': max(years)}
    return render(request, "stats/tables.html", context)


@login_required
def profile(request):
    return render(request, "stats/user.html", {})

def add_sleeper_user(request):
    if request.method == 'POST':
        form = NewSleeperUserForm(request.POST, user=request.user)
        if form.is_valid():
            user_dict = form.cleaned_data.get("user_dict")
            if user_dict['new_user']:
                sleeper_user = SleeperUser.objects.create(
                    sleeper_username = user_dict["username"],
                    display_name = user_dict["display_name"],
                    sleeper_userid = user_dict["user_id"],
                    avatar = user_dict["avatar"]
                    )
            else:
                sleeper_user = user_dict["sleeper_user"]
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.sleeperusers.add(sleeper_user)
                
                
            return redirect('profile')
        else:
            messages.error(request, 'Something went wrong')
    else:
        form = NewSleeperUserForm()
    return render(request, "stats/add_sleeper_user.html", {'form': form})
