from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
from dash import dash_table, no_update  # , Dash
import dash_daq as daq
import inspect
from colour import Color
from stats.models import League, Season, User, Matchup
from django.shortcuts import get_object_or_404


green = Color("green")
red = Color("red")

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def debug():
    '''
    This is just for debuggin purposes.
    It prints the function in which it is called,
    and the line at which it is called.
    '''

    print(
        '{} fired. Line {}.'.format(
            inspect.stack()[1][3],
            inspect.stack()[1][2]))


# , external_stylesheets=external_stylesheets)
app = DjangoDash('fantasy_table')
# app = Dash(__name__)

app.css.append_css({"external_url": "/static/css/sb-admin-2.min.css"})

tabs_container_styles = {"width": "49%", "display": "inline-block"}

# html.Img(src='/static/img/record.svg'),

app.layout = html.Div([
    dcc.Store(id='league', data=[]),
    html.Div(
        dcc.Tabs(
            [
                dcc.Tab(
                    dash_table.DataTable(
                        id='records_table',
                        cell_selectable=False,
                        style_header={
                            'backgroundColor': '#2B3140',
                            'color': '#fff',
                            'border': 'none'
                        },
                        style_cell={
                            'border': 'none',
                            'minWidth': '80px',
                            'width': '80px',
                            'maxWidth': '80px',
                            'textAlign': 'center'
                        }
                    ),
                    className='tab-element tab-records',
                    label="RECORDS"
                ),

                dcc.Tab(
                    children=dash_table.DataTable(
                        id='standings_table',
                        sort_action="native",
                        sort_mode="multi",
                        cell_selectable=False,
                        style_header={
                            'backgroundColor': '#2B3140',
                            'color': '#fff',
                            'border': 'none'
                        },
                        style_cell={
                            'border': 'none',
                            'minWidth': '80px',
                            'width': '80px',
                            'maxWidth': '80px',
                            'textAlign': 'center',
                            'color': '#acbfe8',
                            'backgroundColor': '#2e3544'
                        },
                        tooltip_delay=0,
                        tooltip_duration=None
                    ),
                    className='tab-element tab-standings',
                    label='STANDINGS'
                )
            ]
        ),
        className='tabs-div-container',
        style={"width": '49%', "display": "inline-block"},
    ),
    html.Div([
        daq.BooleanSwitch(
            id='rs_switch',
            on=True,
            color='#00ceb8',
            label="Regular season",
            labelPosition="right",
        ),
        daq.BooleanSwitch(
            id='po_switch',
            on=True,
            color='#00ceb8',
            label="Playoffs",
            labelPosition="right"
        )
    ],
        className='switches'
    )
],
    className='div-dash')


def markdown_link(person, league):
    return f'[{person}](/{league}/{person})'


@app.callback(
    Output("records_table", 'columns'),
    Output("records_table", 'data'),
    Output("records_table", 'style_data_conditional'),
    Output("standings_table", 'columns'),
    Output("standings_table", 'data'),
    Output("standings_table", 'style_data_conditional'),
    Output("standings_table", 'tooltip_header'),
    Output("rs_switch", 'on'),
    Output("po_switch", 'on'),
    # ---------------------
    Input("rs_switch", 'on'),
    Input("po_switch", 'on'),
    # ---------------------
    State("league", 'data')
)
def at_load2(*args, **kwargs):
    debug()

    rs = args[0]
    po = args[1]
    league = args[2]
    ctx = kwargs['callback_context']

    # Prevent from switching off both switches
    update_rs = no_update
    update_po = no_update
    if len(ctx.triggered) > 0:
        if ctx.triggered[0]['prop_id'] == "rs_switch.on" and not rs and not po:
            update_po = True
            po = True

        elif ctx.triggered[0]['prop_id'] == "po_switch.on" and\
                not rs and not po:
            update_rs = True
            rs = True

    l = get_object_or_404(League, nickname=league)
    seasons = Season.objects.filter(league=l)
    users = User.objects.filter(seasons__in=seasons).distinct()

    people = users.values_list('person', flat=True)

    record = {p1: {p2: [0, 0] for p2 in people} for p1 in people}

    for s in seasons:
        for m in Matchup.objects.filter(season=s):
            if m.week < s.playoff_week_start and rs:
                winner = User.objects.get(
                    user_id=m.winner_id, seasons=s).person
                loser = User.objects.get(user_id=m.loser_id, seasons=s).person
                record[winner][loser][0] += 1
                record[loser][winner][1] += 1
            elif m.week >= s.playoff_week_start and po:
                winner = User.objects.get(
                    user_id=m.winner_id, seasons=s).person
                loser = User.objects.get(user_id=m.loser_id, seasons=s).person
                record[winner][loser][0] += 1
                record[loser][winner][1] += 1

    rc_cols = [
        {'name': '', 'id': 'manager', 'presentation': 'markdown'}]
    rc_cols = rc_cols + \
        [{'name': p, 'id': p} for p in record]

    rc_data = []
    rc_conditional_formatting = []
    for p1, person1 in enumerate(record):
        rc_data.append({'manager': markdown_link(person1, league)})
        rc_conditional_formatting.append(
            {
                'if': {
                    'column_id': 'manager',
                },
                'backgroundColor': '#2B3140',
                'color': '#fff',
                'textAlign': 'right',
                'padding-right': '10px'
            }
        )
        for person2 in record[person1]:
            wins = record[person1][person2][0]
            losses = record[person1][person2][1]
            rc_data[-1][person2] = f'{wins} - {losses}'
            color = str(list(green.range_to(red, wins + losses + 1))[losses])
            if person1 == person2:
                color = '#2B3140'
                rc_data[-1][person2] = ''
            rc_conditional_formatting.append(
                {
                    'if': {
                        'column_id': person2,
                        'row_index': p1,
                    },
                    'backgroundColor': color,
                    'color': '#000'
                }
            )

    st_cols = [
        {'name': 'MAN.', 'id': 'manager', 'presentation': 'markdown'},
        {'name': 'SEA.', 'id': 'seasons'},
        {'name': 'PTS.', 'id': 'total_points'},
        {'name': 'REC.', 'id': 'record'},
        {'name': 'W.H.S.', 'id': 'highest_scorer'},
        {'name': 'W.L.S.', 'id': 'lowest_scorer'},
        {'name': 'H.S.', 'id': 'highest_score'},
        {'name': 'L.S.', 'id': 'lowest_score'},
        {'name': 'LUCK', 'id': 'luck_factor'},
        {'name': 'W.B.R.', 'id': 'winners_bracket'},
        {'name': 'L.B.R.', 'id': 'losers_bracket'},
        {'name': 'CHAM.', 'id': 'champion'},
        {'name': 'L.B.R.C.', 'id': 'losers_bracket_champion'}
    ]

    st_data = []
    st_conditional_formatting = [
        {
            'if': {'row_index': 'even'},
            'backgroundColor': '#212635'
        }
    ]

    tooltip_header = {
        'manager': 'Fantasy manager',
        'seasons': 'Number of seasons',
        'total_points': 'Total points',
        'record': 'Overall record',
        'highest_scorer': 'Number of weekly highest scorer',
        'lowest_scorer': 'Number of weekly lowest scorer',
        'highest_score': 'Overall highest score',
        'lowest_score': 'Overall lowest score',
        'luck_factor': 'Luck factor: +1 for wins below median,\
              -1 for losses above median',
        'winners_bracket': 'Number of winner brackets',
        'losers_bracket': 'Number of looser brackets',
        'champion': 'Number of championships',
        'losers_bracket_champion': 'Number of looser bracket championships'}

    for u in users:
        st_conditional_formatting.append(
            {
                'if': {
                    'column_id': 'manager',
                },
                'color': '#fff',
                'textAlign': 'right',
                'padding-right': '10px'
            }
        )
        st_data.append({
            'manager': markdown_link(u.person, league),
            'seasons': 0,
            'total_points': 0,
            'record': [0, 0]}
            )
        if rs:
            st_data[-1]['total_points'] += u.total_points_rs
            st_data[-1]['record'][0] += u.total_wins_rs
            st_data[-1]['record'][1] += u.total_losses_rs
        if po:
            st_data[-1]['total_points'] += u.total_points_po
            st_data[-1]['record'][0] += u.total_wins_po
            st_data[-1]['record'][1] += u.total_losses_po

        st_data[-1]['highest_scorer'] = u.highest_scorer
        st_data[-1]['lowest_scorer'] = u.lowest_scorer
        st_data[-1]['highest_score'] = f'{u.highest_score:.2f}'
        st_data[-1]['lowest_score'] = f'{u.lowest_score:.2f}'
        st_data[-1]['luck_factor'] = u.luck_factor
        st_data[-1]['winners_bracket'] = u.winners_bracket
        st_data[-1]['losers_bracket'] = u.losers_bracket
        st_data[-1]['champion'] = u.champion
        st_data[-1]['losers_bracket_champion'] = u.losers_bracket_champion

    for i, row in enumerate(st_data):
        st_data[i]['total_points'] = f'{st_data[i]["total_points"]:.2f}'
        st_data[i]['record'] = f'{st_data[i]["record"][0]} '\
            f'- {st_data[i]["record"][1]}'

    for s in seasons:
        for u in s.user_set.all():
            for i, row in enumerate(st_data):
                if row['manager'] == markdown_link(u.person, league):
                    st_data[i]['seasons'] += 1
                    break

    return rc_cols, rc_data, rc_conditional_formatting, \
        st_cols, st_data, st_conditional_formatting, \
        tooltip_header, update_rs, update_po


# if __name__ == '__main__':

#     app.run_server(debug=True)
