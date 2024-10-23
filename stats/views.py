from django.http import HttpResponse
from stats.models import League, Season, User, Username, Matchup
from django.shortcuts import render, get_object_or_404



def tables(request,league):
    l = get_object_or_404(League, nickname=league)
    seasons = Season.objects.filter(league=l)
    users = User.objects.filter(seasons__in=seasons).distinct()

    people = users.values_list('person', flat = True)

    record = {p1:{p2:[0,0] for p2 in people} for p1 in people}

    phases = request.POST.getlist('checks[]')

    for s in seasons:
        for m in Matchup.objects.filter(season=s):
            winner = User.objects.get(user_id = m.winner_id, seasons = s).person
            loser = User.objects.get(user_id = m.loser_id, seasons = s).person
            record[winner][loser][0]+=1
            record[loser][winner][1]+=1

            

    # for p in people:
    #     people[p]['percentage'] = 100*people[p]['record'][0]/(people[p]['record'][0]+people[p]['record'][1])
    
    #print('-->',order_by)
    #{k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
    
    context = {"league":league, "record": record, "people": people}
    initial_arguments = {'league':{'data':league}}
    context={'initial_arguments': initial_arguments}
    return render(request, "stats/tables.html", context)

def personal_page(request, league, user):
    l = get_object_or_404(League, nickname=league)
    seasons = Season.objects.filter(league=l)
    context = {'user': user, 'league': league}
    return render(request, "stats/user.html", context)