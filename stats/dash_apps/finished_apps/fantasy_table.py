from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
from dash import dash_table
import dash_daq as daq
import inspect
from stats.models import League, Season, User, Matchup
from django.shortcuts import get_object_or_404

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def debug():
    '''
    This is just for debuggin purposes. It prints the function in which it is called,
    and the line at which it is called.
    '''
    
    print('{} fired. Line {}.'.format(inspect.stack()[1][3],inspect.stack()[1][2]))


app = DjangoDash('fantasy_table')#, external_stylesheets=external_stylesheets)

tabs_styles = {"height": "44px"}
tabs_container_styles = {"width": "49%", "display": "inline-block"}

app.layout = html.Div([
    dcc.Store(id='league', data=[]),
    html.Div(
        dcc.Tabs(
            [
                dcc.Tab(
                    dash_table.DataTable(
                        id='records_table',
                        columns=[{'name':'col1', 'id':'col2'}, {'name':'col2', 'id': 'col2'}],
                        data=[{'col1':[1,2,3], 'col2':[1,2,3]}]
                    ),
                    label='Records'
                ),

                dcc.Tab(
                    dash_table.DataTable(
                        id='standings_table',
                        columns=[{'name':'col1', 'id':'col2'}, {'name':'col2', 'id': 'col2'}],
                        data=[{'col1':[4,5,6], 'col2':[4,5,6]}],
                        sort_action="native",
                        sort_mode="multi"
                    ),
                    label='Standings'
                )
            ],
            style=tabs_styles,
        ),
        style=tabs_container_styles,
    ),
    html.Div([
        daq.BooleanSwitch(
            id = 'rs_switch',
            on=True,
            label="Regular season",
            labelPosition="right"
        ),
        daq.BooleanSwitch(
            id = 'po_switch',
            on=True,
            label="Playoffs",
            labelPosition="right"
        )
    ],
    style=tabs_container_styles,
    ),
    html.Div(id='dummy')
    
])

@app.callback(
    Output("records_table",'columns'),
    Output("records_table",'data'),
    Output("standings_table",'columns'),
    Output("standings_table",'data'),
    #---------------------
    Input("rs_switch",'on'),
    Input("po_switch",'on'),
    #---------------------
    State("league",'data')
)
def at_load2(rs, po, league):
    debug()

    l = get_object_or_404(League, nickname=league)
    seasons = Season.objects.filter(league=l)
    users = User.objects.filter(seasons__in=seasons).distinct()

    people = users.values_list('person', flat = True)

    record = {p1:{p2:[0,0] for p2 in people} for p1 in people}

    for s in seasons:
        for m in Matchup.objects.filter(season=s):
            if m.week < s.playoff_week_start and rs:
                winner = User.objects.get(user_id = m.winner_id, seasons = s).person
                loser = User.objects.get(user_id = m.loser_id, seasons = s).person
                record[winner][loser][0]+=1
                record[loser][winner][1]+=1
            elif m.week >= s.playoff_week_start and po:
                winner = User.objects.get(user_id = m.winner_id, seasons = s).person
                loser = User.objects.get(user_id = m.loser_id, seasons = s).person
                record[winner][loser][0]+=1
                record[loser][winner][1]+=1

    
    record_table_cols = [{'name':p, 'id':p} for p in record]
    record_table_cols = [{'name': 'Manager', 'id':'manager'}] + record_table_cols

    record_table_data = []
    for p1 in record:
        record_table_data.append({'manager':p1})
        for p2 in record[p1]:
            record_table_data[-1][p2]=f'{record[p1][p2][0]} - {record[p1][p2][1]}'


    standings_table_cols=[
        {'name':'Manager', 'id':'manager'},
        {'name':'N. of Seasons', 'id':'seasons'},
        {'name':'Total points', 'id':'total_points'},
        {'name':'Overall record', 'id':'record'},
        {'name':'Weekly HS', 'id':'highest_scorer'},
        {'name':'Weekly LS', 'id':'lowest_scorer'},
        {'name':'Overall HS', 'id':'highest_score'},
        {'name':'Overall LS', 'id':'lowest_score'},
        {'name':'Luck factor', 'id':'luck_factor'},
        {'name':'Winners brackets', 'id':'winners_bracket'},
        {'name':'Losers brackets', 'id':'losers_bracket'},
        {'name':'Champion', 'id':'champion'},
        {'name':'Losers bracket Champion', 'id':'losers_bracket_champion'}
    ]

    standings_table_data = []
    for u in users:
        standings_table_data.append({'manager':u.person, 'seasons': 0, 'total_points':0, 'record':[0,0]})
        if rs:
            standings_table_data[-1]['total_points'] += u.total_points_rs
            standings_table_data[-1]['record'][0] += u.total_wins_rs
            standings_table_data[-1]['record'][1] += u.total_losses_rs
        if po:
            standings_table_data[-1]['total_points'] += u.total_points_po
            standings_table_data[-1]['record'][0] += u.total_wins_po
            standings_table_data[-1]['record'][1] += u.total_losses_po

        standings_table_data[-1]['highest_scorer'] = u.highest_scorer
        standings_table_data[-1]['lowest_scorer'] = u.lowest_scorer
        standings_table_data[-1]['highest_score'] = f'{u.highest_score:.2f}'
        standings_table_data[-1]['lowest_score'] = f'{u.lowest_score:.2f}'
        standings_table_data[-1]['luck_factor'] = u.luck_factor
        standings_table_data[-1]['winners_bracket'] = u.winners_bracket
        standings_table_data[-1]['losers_bracket'] = u.losers_bracket
        standings_table_data[-1]['champion'] = u.champion
        standings_table_data[-1]['losers_bracket_champion'] = u.losers_bracket_champion


    for i,row in enumerate(standings_table_data):
        standings_table_data[i]['total_points'] = f'{standings_table_data[i]["total_points"]:.2f}'
        standings_table_data[i]['record'] = f'{standings_table_data[i]["record"][0]} - {standings_table_data[i]["record"][1]}'


    for s in seasons:
        for u in s.user_set.all():
            for i,row in enumerate(standings_table_data):
                if row['manager'] == u.person:
                    standings_table_data[i]['seasons'] += 1
                    break



    return record_table_cols, record_table_data, standings_table_cols, standings_table_data
