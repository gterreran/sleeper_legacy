from stats.models import League, Season
from django.shortcuts import render, get_object_or_404
from stats import TITLE, VERSION, AUTHOR



def tables(request,league):
    #This dictionary passes league to the 'league' component in the dash app
    l = League.objects.get(nickname=league)
    years = Season.objects.values_list('year', flat=True).filter(league=l)
    initial_arguments = {'league':{'data':league}}
    context={'title': TITLE, 'version': VERSION, 'author': AUTHOR, 'initial_arguments': initial_arguments, 'league': league, 'avatar': l.avatar, 'min_year': min(years), 'max_year': max(years)}
    return render(request, "stats/tables.html", context)

def personal_page(request, league, user):
    l = get_object_or_404(League, nickname=league)
    seasons = Season.objects.filter(league=l)
    context = {'user': user, 'league': league}
    return render(request, "stats/user.html", context)