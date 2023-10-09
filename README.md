# Squad Invasion Statistics
Scripts for analyzing Invasion balancing by layer or level. Requires custom JSON match log with objects containing winner & loser team # (1/2), level, and layer (in display form).

Example of visualized data: https://bit.ly/invasion-stats-all-time

Special thanks to @midwaey for providing match logs, and @ChristianBrinkley for consulation!

## Prerequisites

### Required Software:
[Python 3.12](https://www.python.org/downloads/release/python-3120/)

### Required Libraries:
[pandas](https://pypi.org/project/pandas/)

## Installation and Use:

Download all source files and place all into a folder accesible to preffered editor.

Open up LayerScriot.py or LevelScript.py in editor. Configure file path of match log JSON and run.

## Notes:

Creates duplicate of invasionlayers.csv, invasionlevels.csv, or invasionlayersSE.csv with appended fields for # attack wins, # defense wins, attack win %, defend win %, and # of matches.

LayerScript.py duplicates invasionlayers.csv, LevelScript.py duplicates invasionlevels.csv

LevelScript requires BOTH invasionlayers.csv and invasionlevels.csv to function. LayerScript requires only invasionlayers.csv

LayerScript.py can also be used to analyze Squad Enhanced layer statistics, by simply configuring original_file_path to invasionlayersSE.csv

Filters in the Game class can be used in the filter block to filter for specific matches. Premade filters include afk/empty server and game version(preV5, V5, or postV6).

preV5, V5, and postV6 filters need to be configured once on a match log by match log basis for which match ID marks the first game of the updates V5 and V6.

## Optimizations/Future Plans
-complete invasionlayers.csv and invasionlayersSE.csv for attack/defend faction and attack/defend ticket accuracy

-create filters for faction (i.e. filter all layers for faction United States Army on team 1)

-add terminal args for configuring input JSON name/file path and output CSV's name/file path, filters, and fields

-add interopability with default squadJS match logs

-squadJS match logs would allow for average match time analysis 
