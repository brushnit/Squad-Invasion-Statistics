import json 
import csv
import shutil
import pandas as pd
#configure input JSON file name for json_file_path, and output CSV file name for csv_file_path
json_file_path = 'DBLog_Games_2023_10_08.json'#match log JSON
csv_file_path  = 'levelstatistics.csv' #new csv file

#set int v5FirstMatchId and int v6FirstMatchId to the match IDs of the first live game of each update in json_file_path
v5FirstMatchId = 933
v6FirstMatchId = 4710

original_csv_file = 'invasionlevels.csv'
filter_file_path = 'invasionlayers.csv'
shutil.copy(original_csv_file, csv_file_path)

invasionLayers = []#array of all invasion layer display names
team2Layers = []#array of all invasion layer display names in which team 2 attacks
with open(filter_file_path, newline='') as incsv:
    invasionLayersReader = csv.reader(incsv)
    next(invasionLayersReader)
    for row in invasionLayersReader:
        if row == 'Fool': #workaround for the single quote in Fool`s Road Invasion v1 breaking filter, may break Squad Enhanced analysis
            invasionLayers.append('Fool\'s Road Invasion v1')
        else:
            invasionLayers.append(row[0])
        if row[2] != '1':
            team2Layers.append(row[0])
            
class Game:
    def __init__(self, game):
        self.id = game['id'] #required if using game version filter
        self.time = game['time']
        self.winnerTeam = game['winnerTeam'] #required
        self.winnerFaction = game['winnerFaction']
        self.winnerTickets = game['winnerTickets'] #required for afk filter
        self.loserTeam = game['loserTeam'] #required
        self.loserFaction = game['loserFaction']
        self.loserTickets = game['loserTickets'] #required for afk filter
        self.layer = game['layer'] #required
        self.level = game['level'] #required
        
        #custom filters
        self.team1Win = game['winnerTeam'] == "1"
        self.isInvasionMatch = game['layer'] in invasionLayers #filter for invasion layer display names
        self.isTeamsInvert = game['layer'] in team2Layers #filter for layers which team 2 attacks
        self.isLiveMatch = not (game['winnerTickets'] == 900 and game['loserTickets'] == 200) or (game['winnerTickets'] == 800 and game['loserTickets'] == 200) #filter for live matches, assuming no tickets are ever lost in afk matches
        self.preV5 = game['id'] < v5FirstMatchId #filter for all matches before v5 update
        self.V5 = v5FirstMatchId <= game['id'] < v6FirstMatchId #filter for all matches in v5
        self.postV6 = game['id'] >= v6FirstMatchId #filter for all matches after v6 update
        
def main():
    df = pd.read_csv(csv_file_path) #creates dataframe of new csv file
    
    #if adding new fields to output, configure fields in newFields array - make sure update list matchStats below
    newFields = ['attackWin', 'defendWin', 'perAttackWin', 'perDefendWin', 'numMatches'] #fields to be added to csv/columds to be added to dataframe
    for field in newFields:
        df[field] = '' #creates columns in df based on newFields, sets all values of each column to ''
    
    with open(json_file_path, 'r') as json_file:
        matches = json.load(json_file)
        gameList = []
        
        for index, row in df.iterrows():
            attackWin = 0
            defendWin = 0
            numInvasionMatches = 0
            perAttackWin = 0
            perDefendWin = 0
            
            for match in matches['DBLog_Games']:
                game = Game(match)
                gameList.append(match)
                
                #filter block
                if game.level == row['level'] and game.isLiveMatch and game.isInvasionMatch: #add more filters using 'and' statements, i.e: and (game.V5 or game.preV5):
                    numInvasionMatches += 1
                    if game.isTeamsInvert:
                        if game.team1Win:
                            defendWin += 1
                        else :
                            attackWin += 1
                    else:
                        if game.team1Win:
                            attackWin += 1
                        else:
                            defendWin += 1
            
            #add any calculations of variables below           
            if(numInvasionMatches > 0):
                        perAttackWin = f'{round(100 *(attackWin / numInvasionMatches), 1)}%'
                        perDefendWin = f'{round(100 *(defendWin / numInvasionMatches), 1)}%' 
            else:
                        perAttackWin = 'No Data'
                        perDefendWin = 'No Data'
                        
            #if adding new fields to output, add variables in matchStats to be written to fields added in newFields            
            matchStats = [f'{attackWin}',f'{defendWin}', perAttackWin, perDefendWin,f'{numInvasionMatches}']
            
            df.loc[index, newFields] = matchStats #writes matchStats to newFields in the row defined by index
    
    df.to_csv(csv_file_path) #saves dataframe to file
        
if __name__ == '__main__':
    main()