import json 
import csv
import argparse
#insert JSON file name
json_file_path = 'DBLog_Games_202310011917.json'

#example Python terminal input:
#py .\InvasionScript.py -lv "Al Basrah"
#returns all invasion matches on Al Basrah, regardless of layer

#initialize parser
parser = argparse.ArgumentParser()

#adding optional argument
parser.add_argument("-la", "--Layer", help = "Filter by layer")
parser.add_argument("-lv", "--Level", help = "Filter by level")
parser.add_argument("-f", "--Faction", help = "Filter by faction")
parser.add_argument("-id", "--Ids", help = "Filter by ids")
parser.add_argument("-t", "--Time", help = "Filter by time")

#read arguments from command line
args = parser.parse_args()

layerFilter = None
levelFilter = None
factionFilter = None
idFilter = None
timeFilter = None

#need to add ids and times
if args.Layer:
    print(f"Selected layer is {args.Layer}")
    layerFilter = args.Layer
if args.Level:
    print(f"Selected level is {args.Level}")
    levelFilter = args.Level
if args.Faction:
    print(f"Selected faction is {args.Faction}")
    factionFilter = args.Faction 

#array of invasion layers
invasionLayers = []
with open('invasionlayers.csv', newline='') as csvfile:
    invasionLayersCsv = csv.reader(csvfile)
    for row in invasionLayersCsv:
        invasionLayers.append(row[0])

#array of layers team 2 attacks on
team2Layers = []
with open('team2layers.csv', newline='') as csvfile:
    team2layersCsv = csv.reader(csvfile)
    for row in team2layersCsv:
        team2Layers.append(row[0])
        
class Game:
    def __init__(self, game):
        self.id = game['id']
        self.time = game['time']
        self.winnerTeam = game['winnerTeam']
        self.winnerFaction = game['winnerFaction']
        self.winnerTickets = game['winnerTickets']
        self.loserTeam = game['loserTeam']
        self.loserFaction = game['loserFaction']
        self.loserTickets = game['loserTickets']
        self.layer = game['layer']
        self.level = game['level']
        self.team1win = game['winnerTeam'] == "1"
        self.isInvasionMatch = game['layer'] in invasionLayers
        self.isTeamsInvert = game['layer'] in team2Layers
        self.isLiveMatch = not (game['winnerTickets'] == 900 and game['loserTickets'] == 200) or (game['winnerTickets'] == 800 and game['loserTickets'] == 200)
        self.postV6 = game['id'] >= 4710
        #need to add ids and time
        self.matchesFilter = layerFilter is None or game['layer'] == layerFilter 
        self.matchesFilter = self.matchesFilter and (levelFilter is None or game['level'] == levelFilter)
        self.matchesFilter = self.matchesFilter and (factionFilter is None or game['winnerFaction'] == factionFilter or game['loserfaction'] == factionFilter)
            
def main():
    
    attackWin = 0
    defendWin = 0
    numInvasionMatches = 0
    perAttackWin = 0
    perDefendWin = 0
    
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            gameList = []
            for row in data['DBLog_Games']:
                game = Game(row)
                gameList.append(row)
                if game.isInvasionMatch and game.isLiveMatch and game.matchesFilter:
                    numInvasionMatches += 1
                    if game.isTeamsInvert:
                        if game.team1win:
                            defendWin += 1
                        else :
                            attackWin += 1
                    else:
                        if game.team1win:
                            attackWin += 1
                        else:
                            defendWin += 1
            
        perAttackWin = attackWin / numInvasionMatches
        perDefendWin = defendWin / numInvasionMatches    
        
        print(f"Number of invasion matches: {numInvasionMatches}")
        print(f"Number of defense wins: {defendWin}")
        print(f"Defense win percent: {perDefendWin}")
        print(f"Number of attack wins: {attackWin}")
        print(f"Attack win percent: {perAttackWin}")
        
        if(numInvasionMatches == 0):
            raise Exception("Number of matches is 0")

    except FileNotFoundError:
        print(f"File '(json_file_path)' not found.")
    except json.JSONDecodeError:
        print(f"Invalid JSON format in '(json_file_path)'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
if __name__ == '__main__':
    main()