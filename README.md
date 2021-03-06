# Fantasy premier league plotting

Misc plots of fantasy premier league stats for your own fantasy leagues. 

## Usage
Edit `config.yaml` and then run
`python fpl_scrape_and_plot.py`.

## Description
Raw data is read from the fantasy premier league API, for example:

* https://fantasy.premierleague.com/drf/entry/70189/history

* https://fantasy.premierleague.com/drf/leagues-classic-standings/74045?phase=1&le-page=1&ls-page=1

Although not currently used, a third resource is:

* https://fantasy.premierleague.com/drf/bootstrap-static

Based on info found 
[here](http://www.fiso.co.uk/forum/viewtopic.php?f=18&t=121295&p=2911180#p2911180 "fiso.co.uk").

## Method
Written in python. Data scraped using requests and plotted using matplotlib.

## Example output
![League rank](plots/league_rank_LR-Consulting-Norway.png "League rank")

![GW rank](plots/league_gw_rank_LR-Consulting-Norway.png "GW rank")

![GW rank](plots/league_value_and_rank_LR-Consulting-Norway.png "League value and rank")