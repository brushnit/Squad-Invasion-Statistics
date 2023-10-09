# Squad Invasion Statistics
Scripts for analyzing Invasion balancing by layer or level. Requires JSON match log with winner/loser team #. 

Example of visualized data: https://bit.ly/invasion-stats-all-time

## How It's Made:
**Tech Used:** Python, JSON, CSV

Requires pandas library

Simply configure match log JSON file path at top and run.
Creates duplicate of invasionlayerss.csv, invasionlevels.csv, or invasionlayersSE.csv with appended fields for # attack wins, # defense wins, attack win %, defend win %, and # of matches.
LayerScript.py duplicates invasionlayers.csv, LevelScript.py duplicates invasionlevels.csv
LevelScript requires BOTH invasionlayers.csv and invasionlevels.csv to function. LayerScript requires only invasionlayers.csv

LayerScript.py can also be used to analyze Squad Enhanced layer statistics, by simply configuring original_file_path to invasionlayersSE.csv

Filters in the Game class can be used in the filter block to filter for specific matches. Preset filters include afk/empty server and version (preV5, V5, or postV6)
preV5, V5, and postV6 filters need to be configured once on a server by server basis for which match ID marked the first game of the update V5 and V6

## Optimizations/Future Plans
-add interopability with default SquadJS match logs
  -would allow for average match time
-add terminal args for configuring input JSON name/file path and output CSV's name/file path, filters, and fields

#Lessons Learned
