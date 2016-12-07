# -*- coding: utf-8 -*-
import requests
# import pickle
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.cm


def color(i, n):
    # cmap = matplotlib.cm.get_cmap('Paired')
    if n <= 6:
        n_reduced = 6
    elif n <= 12:
        n_reduced = 12
    else:
        n_reduced = n
    colors = [
        plt.cm.Paired(float(c) / (n_reduced - 1))
        for c in range(0, n_reduced)]
    color = colors[i]
    return color

# API info found here:
# http://www.fiso.co.uk/forum
# /viewtopic.php?f=18&t=121295&p=2911180#p2911180

# Enter your team id manually to get results from all your leagues.
# Alternatively, manually enter league_ids below.
my_team_id = 70189
# https://fantasy.premierleague.com/drf/entry/70189/history
my_team_url = (
    'https://fantasy.premierleague.com/drf/entry/'
    '{}/history').format(my_team_id)
my_team_data = requests.get(my_team_url).json()
my_league_ids = [
    s['id'] for s in my_team_data['leagues']['classic']
    if s['league_type'] == 'x']
current_gw = my_team_data['entry']['current_event']

# Comment out one of these two lines
league_ids = my_league_ids
league_ids.remove(29394)  # too many teams
# https://fantasy.premierleague.com/drf
# /leagues-classic-standings/74045?phase=1&le-page=1&ls-page=1
# league_ids = [74045]

# Loop through the given fpl leagues.
for league_id in league_ids:
    league_url = (
        'https://fantasy.premierleague.com/drf/leagues-classic-standings/'
        '{}?phase=1&le-page=1&ls-page=1').format(league_id)
    league_data = requests.get(league_url).json()
    # for use in file names (æøå looks ugly, but works)
    league_name_f = league_data['league'][
        'name'].replace(' ', '-').encode('utf8')
    # Find teams in each league.
    team_ids = [s['entry'] for s in league_data['standings']['results']]
    overall_points = np.ones((len(team_ids), current_gw)) * np.nan
    points = np.ones((len(team_ids), current_gw)) * np.nan
    players = []
    for i, team_id in enumerate(team_ids):
        team_url = (
            'https://fantasy.premierleague.com/drf/entry/'
            '{}/history').format(team_id)
        team_data = requests.get(team_url).json()
        first_gw = team_data['entry']['started_event']
        gws = np.arange(
            first_gw,
            current_gw + 1)
        overall_points[
            i,
            gws -
            1] = [
            team_data['history'][
                gw -
                first_gw]['total_points'] for gw in gws]
        points[
            i,
            gws -
            1] = [
            team_data['history'][
                gw -
                first_gw]['points'] for gw in gws]
        player = '{} {}'.format(
            team_data['entry']['player_first_name'].encode('utf8'),
            team_data['entry']['player_last_name'].encode('utf8'))
        players.append(player)

    # Check that teams are sorted in api.
    # I think they always are, but am not sure.
    if not (overall_points[:, -1] ==
            sorted(overall_points[:, -1], reverse=True)).all():
        print 'Teams does not come in sorted order, you need to rewrite the code!'
        raise

#### #### Plot league rank vs gw - line plot #### ####
    # Set ranks to nan for gws before team joined.
    league_ranks = np.array(
        len(team_ids) - np.argsort(np.argsort(overall_points, axis=0), axis=0),
        dtype=float)
    league_ranks[np.isnan(overall_points)] = np.nan
    plt.figure(figsize=(16, 6))
    # Loop through leagues
    for i, league_rank in enumerate(league_ranks):
        # # Reduced linewidth for bottom half of league table
        # if len(league_ranks)<5:
        #     linewidth = 10
        # else:
        #     if i<len(league_ranks)/2:
        #         linewidth=10
        #     else:
        #         linewidth=1
        linewidth = 10
        plt.plot(
            range(1, current_gw + 1),
            league_rank,
            '-',
            linewidth=linewidth,
            markersize=linewidth,
            color=color(i, len(team_ids)))
        plt.text(
            current_gw + 0.3,
            i + 1,
            players[i].decode('utf8'),
            verticalalignment='center')
    plt.ylim(0, len(team_ids) + 1)
    plt.yticks(range(1, len(team_ids) + 1))
    plt.xlim(0.7, current_gw * 1.25)  # can this be done better?
    plt.xticks(range(1, current_gw + 1))
    plt.tick_params(
        axis='y',
        which='both',
        right='off')
    plt.xlabel('Gameweek')
    plt.ylabel('League Rank')
    plt.gca().invert_yaxis()
    plt.title(
        'Fantasy Premier League 2016/2017\n' +
        league_data['league']['name'])
    plt.savefig('league_rank_{}.png'.format(
        league_name_f), bbox_inches='tight')
    plt.close()

#### #### Plot league GW rank - boxplot #### ####
    league_ranks_gw = np.array(
        len(team_ids) - np.argsort(np.argsort(points, axis=0), axis=0),
        dtype=float)
    plt.figure(figsize=(12, 8))
    # Boxplot does not handle nans.
    # This is a hack, couldn't be bottered to to it properly.
    league_ranks_gw[np.isnan(points)] = len(team_ids) / 2

    boxplot = plt.boxplot(
        np.transpose(league_ranks_gw),
        whis='range',
        showmeans=False,  # mean not shown, only median (it became too messy)
        patch_artist=True,  # filled boxes
        widths=0.8)  # default is 0.5, I think
    plt.setp(boxplot['boxes'], color='#33a02c', linewidth=0)
    plt.setp(boxplot['whiskers'], color='k', linestyle='-')
    plt.setp(boxplot['caps'], color='k')
    plt.setp(boxplot['medians'], color='w', linewidth=4)
    plt.setp(
        boxplot['means'],
        markerfacecolor='w',
        markeredgecolor='none',
        markersize=10)
    plt.ylim(0, len(team_ids) + 1)
    plt.yticks(range(1, len(team_ids) + 1))
    plt.xticks(
        range(1, len(team_ids) + 1),
        [p.decode('utf8') for p in players],
        rotation='vertical')
    plt.ylabel('League GW Rank')
    plt.gca().invert_yaxis()
    plt.title(
        'Fantasy Premier League 2016/2017\n' +
        league_data['league']['name'])
    plt.savefig('league_gw_rank_{}.png'.format(
        league_name_f), bbox_inches='tight')

# league rank vs team value. kanskje med "hale" som viser utvikling?
# hvor mye poeng skiller. bedre løsning enn søyleplot?
