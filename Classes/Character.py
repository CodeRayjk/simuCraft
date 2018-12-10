import yaml
from database.itemReader import *


class Character:
    def __init__(self,name="",cClass="", level="-1",race = ""):
        self.name = name
        self.cClass = cClass
        self.level = level
        self.race = race
        self.items = []
        self.spells = []
        self.oReader = ObjectReader()

    def addItem(self,item):

        self.items.append(self.oReader.getItem(item))

    def getStats(self):

        stats = []


        return stats

    def printSelf(self):
        print('Name:%s' % self.name)
        print('Class:%s' % self.cClass)
        print('Level:%s' % self.level)
        print('Race:%s' % self.race)
        for item in self.items:
            print('------------')
            item.printAll()



class CreateCharacter:
    def __init__(self,file):

        with open(file, 'r') as stream:
            data_loaded = yaml.load(stream)

        print(data_loaded)
        self.__cCreate(data_loaded)

    def __cCreate(self,data):

        munchkin = Character(name=data['Character']['Name'],
                             cClass=data['Character']['Class'],
                             level=data['Character']['Level'],
                             race=data['Character']['Race'])

        for item in data['Character']['Item']:
            if not data['Character']['Item'][item] == 'pass':
                munchkin.addItem(data['Character']['Item'][item])

        munchkin.printSelf()



        return munchkin








if __name__ == '__main__':


    CreateCharacter('C:\\Users\Rayjk\PycharmProjects\simuCraft\demo.yml')