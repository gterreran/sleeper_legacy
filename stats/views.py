from django.http import HttpResponse
from stats.models import League, Season, User, Username, Matchup
from django.shortcuts import render, get_object_or_404



def index(request,league):
    l = get_object_or_404(League, nickname=league)
    seasons = Season.objects.filter(league=l)
    users = User.objects.filter(seasons__in=seasons).distinct()

    people = {p:{'record':[0,0,0], 'total_points':0} for p in users.values_list('person', flat = True)}

    record = {p1:{p2:[0,0,0] for p2 in people} for p1 in people}

    for s in seasons:
        for m in Matchup.objects.filter(season=s):
            person1 = User.objects.get(user_id = m.user1).person
            person2 = User.objects.get(user_id = m.user2).person
            people[person1]['total_points']+=m.user1_score
            people[person2]['total_points']+=m.user2_score
            if m.user1_score > m.user2_score:
                record[person1][person2][0]+=1
                people[person1]['record'][0]+=1
                record[person2][person1][1]+=1
                people[person2]['record'][1]+=1
            elif m.user1_score < m.user2_score:
                record[person1][person2][1]+=1
                people[person1]['record'][1]+=1
                record[person2][person1][0]+=1
                people[person2]['record'][0]+=1
            else:
                record[person1][person2][2]+=1
                record[person2][person1][2]+=1
                people[person1]['record'][2]+=1
                people[person2]['record'][2]+=1
            

    for p in people:
        people[p]['percentage'] = 100*people[p]['record'][0]/(people[p]['record'][0]+people[p]['record'][1])
    

    print(request.GET.get('id', None))
    order_by = request.GET.get('order_by', 'defaultOrderField')
    #print('-->',order_by)
    #{k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
    
    context = {"league":league, "record": record, "people": people}
    return render(request, "stats/index.html", context)

def personal_page(request, league, user):
    l = get_object_or_404(League, nickname=league)
    seasons = Season.objects.filter(league=l)
    context = {'user': user, 'league': league}
    return render(request, "stats/user.html", context)