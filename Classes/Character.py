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

    def addSpell(self,spell,rank,condition = 0):

        self.spells.append(self.oReader.getSpell(spell,rank))


    def getStats(self):

        stats = []


        return stats

    def attribute(self,attr):

        for item in self.items:
                tmp = item.getAttribute(attr)
                if tmp:
                    print( tmp )





    def printSelf(self):
        print('Name:%s' % self.name)
        print('Class:%s' % self.cClass)
        print('Level:%s' % self.level)
        print('Race:%s' % self.race)
        for item in self.items:
            print('------------')
            item.printAll()

        for spell in self.spells:
            print('-----------')
            spell.printAll()


class CreateCharacter:
    def __init__(self,file):

        with open(file, 'r') as stream:
            self.data_loaded = yaml.load(stream)


        #print(data_loaded)
        #self.cCreate(data_loaded)

    def cCreate(self, datain = 0):
        if datain == 0:
            data = self.data_loaded
        else:
            data = datain

        munchkin = Character(name=data['Character']['Name'],
                             cClass=data['Character']['Class'],
                             level=data['Character']['Level'],
                             race=data['Character']['Race'])

        for item in data['Character']['Item']:
            if not data['Character']['Item'][item] == 'pass':
                munchkin.addItem(data['Character']['Item'][item])


        for spell in data['Character']['Spells']:
            munchkin.addSpell(data['Character']['Spells'][spell]['Name'],data['Character']['Spells'][spell]['Rank'])



        #munchkin.printSelf()



        return munchkin








if __name__ == '__main__':


    cc = CreateCharacter('C:\\Users\Rayjk\PycharmProjects\simuCraft\demoLock.yml')

    rayjk = cc.cCreate()
    rayjk.attribute('Intellect')
