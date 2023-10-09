import json 
import csv
import shutil
import pandas as pd
#block creates duplicate of invasionlayers.csv for statistics to append to, sets file path names
json_file_path = 'DBLog_Games_202310011917.json'
original_csv_file = 'invasionlevels.csv'
team2_file_path = 'invasionlayers.csv'
csv_file_path  = 'levelstatisticsseptember.csv' #new csv file
shutil.copy(original_csv_file, csv_file_path)

#creates array of invasion layers and layers in which team 2 is the attackers
invasionLayers = []
team2Layers = []
with open(team2_file_path, newline='') as incsv:
    invasionLayersReader = csv.reader(incsv)
    next(invasionLayersReader)
    for row in invasionLayersReader:
        if row == 'Fool':
            invasionLayers.append('Fool\'s Road Invasion v1')
        else:
            invasionLayers.append(row[0])
        if row[2] != '1':
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
        self.team1Win = game['winnerTeam'] == "1"
        self.isInvasionMatch = game['layer'] in invasionLayers
        self.isTeamsInvert = game['layer'] in team2Layers
        self.isLiveMatch = not (game['winnerTickets'] == 900 and game['loserTickets'] == 200) or (game['winnerTickets'] == 800 and game['loserTickets'] == 200) #make isLiveMatch be tied to int in field 5 and 8 of invasionlayers.csv
        self.postV6 = game['id'] >= 4710 #only useful for sept data set, or combined data set

def main():
    df = pd.read_csv(csv_file_path) #creates dataframe of csv file
    
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
                    
                if game.level == row['level'] and game.isLiveMatch and game.isInvasionMatch:
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
                        
            if(numInvasionMatches > 0):
                        perAttackWin = f'{round(100 *(attackWin / numInvasionMatches), 1)}%'
                        perDefendWin = f'{round(100 *(defendWin / numInvasionMatches), 1)}%' 
            else:
                        perAttackWin = 'No Data'
                        perDefendWin = 'No Data'
                            
            matchStats = [f'{attackWin}',f'{defendWin}', perAttackWin, perDefendWin,f'{numInvasionMatches}']
            
            df.loc[index, newFields] = matchStats #writes matchStats to newFields in the row defined by index
    
    df.to_csv(csv_file_path) #saves dataframe to file
        
if __name__ == '__main__':
    main()