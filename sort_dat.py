import glob
import os
import xml.etree.ElementTree as ET

listOfGames = {}
def addGame(mainGame, cloneGame):
    if mainGame not in listOfGames:
        listOfGames[mainGame] = []
    if mainGame != cloneGame:
        listOfGames[mainGame].append(cloneGame)

def printFile(outputFile):
    with open(outputFile, 'w') as output:
        for gameName, gameClones in listOfGames.items():
            output.write(f'{gameName}\n')
            for cloneName in gameClones:
                output.write(f'\t{cloneName}\n')

def processDAT(datFile):
    listOfGames.clear()
    tree = ET.parse(datFile)
    datName = tree.find('header').find('name').text.replace(' (Parent-Clone)', '')
    print(f'Processing now: {datName}')
    games = tree.findall('game')
    for game in games:
        gameName = game.attrib['name']
        if 'cloneof' in game.attrib:
            addGame(game.attrib['cloneof'], gameName)
        else:
            addGame(gameName, gameName)
    outputFile = os.path.join('sorted_dats', datName + '.txt');
    printFile(outputFile)

datFiles = glob.glob(os.path.join('dats', '*.dat'))
for datFile in datFiles:
    processDAT(datFile)
    
print("END")