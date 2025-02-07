from stats.models import League, Season
from django.shortcuts import render, get_object_or_404
from stats import TITLE, VERSION, AUTHOR
from django.contrib.auth.decorators import login_required


def home(request):
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
    context = {'user':request.user.username}
    return render(request, "stats/user.html", context)
