
import csv
import sys,os
import logging
my_path = os.path.abspath(os.path.dirname(__file__))
''''
"2825","2","2","Bow of Searing Arrows","20552","4","0","1","73609","14721","15","-1","-1","42","37","0","0","0","0","0","0","0","0","1","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","47","88","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","2700","2","100","29624","1","0","0","-1","0","-1","0","0","0","0","-1","0","-1","0","0","0","0","-1","0","-1","0","0","0","0","-1","0","-1","0","0","0","0","0","0","-1","2","","0","0","0","0","0","2","0","0","0","0","90","0","0","0","","61","0","0","0","0","0"
"22465","4","3","Earthshatter Legguards","35754","4","0","1","763444","152688","7","64","255","88","60","0","0","0","0","0","0","0","0","1","0","7","28","5","30","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","484","0","0","0","0","0","0","0","0","0","18038","1","0","0","-1","0","-1","21365","1","0","0","-1","0","-1","0","0","0","0","-1","0","-1","0","0","0","0","-1","0","-1","0","0","0","0","0","0","0","1","","0","0","0","0","0","5","0","0","0","527","105","0","0","0","","65","0","0","0","0","0"

"entry",\
"class",
"subclass",
"name",
"displayid",
"Quality",
"Flags",
"BuyCount",
"BuyPrice",
"SellPrice",
"InventoryType",
"AllowableClass",
"AllowableRace",
"ItemLevel",
"RequiredLevel",
"RequiredSkill",
"RequiredSkillRank",
"requiredspell",
"requiredhonorrank",
"RequiredCityRank",
"RequiredReputationFaction",
"RequiredReputationRank",
"maxcount",
"stackable",
"ContainerSlots",
stat_types: 1 - X  :  2 - X  : 3 - Agility : 4 - Strength : 5 - Intellect : 6 - Spirit : 7 - Stamina : 8 - X : 

"stat_type1","stat_value1",   
"stat_type2","stat_value2",
"stat_type3","stat_value3",
"stat_type4","stat_value4",
"stat_type5","stat_value5",
"stat_type6","stat_value6",
"stat_type7","stat_value7",
"stat_type8","stat_value8",
"stat_type9","stat_value9",
"stat_type10","stat_value10",
"dmg_min1","dmg_max1","dmg_type1",
"dmg_min2","dmg_max2","dmg_type2",
"dmg_min3","dmg_max3","dmg_type3",
"dmg_min4","dmg_max4","dmg_type4",
"dmg_min5","dmg_max5","dmg_type5",
"armor",
"holy_res","fire_res","nature_res","frost_res","shadow_res","arcane_res",
"delay","ammo_type","RangedModRange",
"spellid_1","spelltrigger_1","spellcharges_1","spellppmRate_1",
"spellcooldown_1","spellcategory_1","spellcategorycooldown_1",
"spellid_2","spelltrigger_2","spellcharges_2","spellppmRate_2",
"spellcooldown_2","spellcategory_2","spellcategorycooldown_2",
"spellid_3","spelltrigger_3","spellcharges_3","spellppmRate_3",
"spellcooldown_3","spellcategory_3","spellcategorycooldown_3",
"spellid_4","spelltrigger_4","spellcharges_4","spellppmRate_4",
"spellcooldown_4","spellcategory_4","spellcategorycooldown_4",
"spellid_5","spelltrigger_5","spellcharges_5","spellppmRate_5",
"spellcooldown_5","spellcategory_5","spellcategorycooldown_5",
"bonding",
"description",
"PageText",
"LanguageID",
"PageMaterial",
"startquest",
"lockid",
"Material",
"sheath",
"RandomProperty",
"block",
"itemset",
"MaxDurability",
"area",
"Map",
"BagFamily",
"ScriptName",
"DisenchantID",
"FoodType",
"minMoneyLoot",
"maxMoneyLoot",
"Duration",
"ExtraFlags"

dmg_type = 0 - Normal dmg : 1 - Holy dmg : 2 - Fire dmg : 3 - Nature dmg : 4 - Frost dmg  : 5 - Shadow dmg : 6 - Arcane dmg


'''
dmgType ={ '0' : 'Normal' , '1' : 'Holy', '2' : 'Fire' , '3' : 'Nature', '4' : 'Frost', '5' : 'Shadow', '6' : 'Arcane'}


attributeConv = {'3': 'Agility' , '4':'Strength', '5' : 'Intellect', '6' : 'Spirit', '7' : 'Stamina'}

# Slots = '1' : 'head' , '2' : 'amulet', '3':'shoulders','5': 'chest','6':'waist', '7':'legs','8':'feet'
# '9': 'wrist','10': 'hands','11:'Rings','12':'trinket','13':'weapon','16': 'cloak','17':'Two-hand',
# '21':'main weapon': '22':'off weapon', '14': 'shield' , '28' : 'idol/lib/totem', '15': 'bow' ,
# '26' : 'gun/crossbow/wand'




slots ={ '1' : 'head' , '2' : 'amulet', '3':'shoulders','5': 'chest','6':'waist', '7':'legs','8':'feet',
 '9': 'wrist','10': 'hands','11':'Rings','12':'trinket','13':'One-hand','16': 'cloak', '17':'Two-hand',
 '21':'Main hand', '22':'Off hand', '14': 'Shield' , '28' : 'idol/lib/totem', '15': 'Ranged' , '24': 'Ammo',
 '26' : 'Ranged','20':'Robe'}



class Item():
    def __init__(self, **kwargs):
        self.info = kwargs

    def addAttribute(self,**kwargs):
        self.info.update(kwargs)

    def printAll(self):
        for key,item in self.info.items():
            print('%s:%s' %(key,item))

    def getAttribute(self,attr):

        for key,item in self.info.items():
            if attr in key:
                return item

        return None



class Spell():
    def __init__(self, **kwargs):
        self.info = kwargs

    def addAttribute(self,**kwargs):
        #print('INSIDE ADD')
        #print (kwargs)
        self.info.update(kwargs)
        #print(self.info)

    def getAttribute(self,attr):
        for key,item in self.info.items():
            if attr in key:
                return item

        return None

    def printAll(self):
        for key,item in self.info.items():
            print('%s:%s' %(key,item))




class ObjectReader():



    def __init__(self):
        filePathItem = os.path.join(my_path, "item_template.csv")
        readItem = csv.reader(open(filePathItem),delimiter = ',')

        filePathSpell = os.path.join(my_path, "spell_template.csv")
        readSpell = csv.reader(open(filePathSpell), delimiter=',')

        filePathCast = os.path.join(my_path, "SpellCastTimes.csv")
        readSpellCast = csv.reader(open(filePathCast), delimiter=',')


        filePathDuration = os.path.join(my_path, "SpellDuration.csv")
        readSpellDur =  csv.reader(open(filePathDuration), delimiter=',')


        self.allItem = []
        self.indexItem = self._fReader(readItem,self.allItem)

        self.allSpells = []
        self.indexSpell = self._fReader(readSpell,self.allSpells)

        self.allCastTimes = []
        self.indexCastSpeed = self._fReader(readSpellCast,self.allCastTimes)

        self.allCastDurations = []
        self.indexCastDuration = self._fReader(readSpellDur,self.allCastDurations)



        readItem = None
        readSpell = None
        readSpellCast = None
        readSpellDur = None

    def _fReader(self,obj,list):
        index = None

        for line in obj:
            index = line
            break
        for line in obj:
            list.append(line)

        return index


    def __getSpellDuration(self,id):

        for row in self.allCastDurations:
            if row[self.indexCastDuration.index('ID')] == id:
                return row[self.indexCastDuration.index('Duration')]

    def __getCastSpeed(self,id):

        for row in self.allCastTimes:
            if row[self.indexCastSpeed.index('ID')] == id:
                return row[self.indexCastSpeed.index('Base')]


    def getItem(self,itemName):

        #DELAY
        theItem = None
        for row in self.allItem:
            if itemName.lower() == row[self.indexItem.index('name')].lower():
                theItem = Item(Name = row[self.indexItem.index('name')])
                logging.debug(row)
                #print(row[self.indexItem.index('delay')])

                if row[self.indexItem.index('armor')] is not '0':
                    theItem.addAttribute(Armor = row[self.indexItem.index('armor')])
                    #print('Armor : %s' % row[self.indexItem.index('armor')])

                for i in range(1, 6):
                    if row[self.indexItem.index('stat_type%d' % i)] is not '0':
                        if row[self.indexItem.index('stat_type%d' % i)] == '3':
                            theItem.addAttribute(Agility = row[self.indexItem.index('stat_value%d' % i)])
                        elif row[self.indexItem.index('stat_type%d' % i)] == '4':
                            theItem.addAttribute(Strength=row[self.indexItem.index('stat_value%d' % i)])
                        elif row[self.indexItem.index('stat_type%d' % i)] == '5':
                            theItem.addAttribute(Intellect=row[self.indexItem.index('stat_value%d' % i)])
                        elif row[self.indexItem.index('stat_type%d' % i)] == '6':
                            theItem.addAttribute(Spirit=row[self.indexItem.index('stat_value%d' % i)])
                        elif row[self.indexItem.index('stat_type%d' % i)] == '7':
                            theItem.addAttribute(Stamina=row[self.indexItem.index('stat_value%d' % i)])

                for i in range(1, 6):
                    if row[self.indexItem.index('dmg_min%d' % i)] is not '0':
                        theItem.addAttribute(dmg_min = row[self.indexItem.index('dmg_min%d' % i)])
                        theItem.addAttribute(dmg_max = row[self.indexItem.index('dmg_max%d' % i)])
                        theItem.addAttribute(dmg_type=dmgType[row[self.indexItem.index('dmg_type%d' % i)]])


                if row[self.indexItem.index('holy_res')] is not '0':
                    theItem.addAttribute(holy_res=row[self.indexItem.index('holy_res')])
                if row[self.indexItem.index('fire_res')] is not '0':
                    theItem.addAttribute(fire_res=row[self.indexItem.index('fire_res')])
                if row[self.indexItem.index('nature_res')] is not '0':
                    theItem.addAttribute(nature_res=row[self.indexItem.index('nature_res')])
                if row[self.indexItem.index('frost_res')] is not '0':
                    theItem.addAttribute(frost_res=row[self.indexItem.index('frost_res')])
                if row[self.indexItem.index('shadow_res')] is not '0':
                    theItem.addAttribute(shadow_res=row[self.indexItem.index('shadow_res')])
                if row[self.indexItem.index('arcane_res')] is not '0':
                    theItem.addAttribute(arcane_res=row[self.indexItem.index('arcane_res')])


                if row[self.indexItem.index('delay')] is not '0':
                    theItem.addAttribute(AttackSpeed=row[self.indexItem.index('delay')])


                if row[self.indexItem.index('InventoryType')] is not '0':
                    theItem.addAttribute(InventoryType=slots[row[self.indexItem.index('InventoryType')]])


        return theItem

    def getSpell(self,spellName,rank = '0'):

        """
        SpellName : done
        SpellRank : done
        EffectBasePoints1: done
        EffectDieSides1: done
        EffectBaseDice1: done
        ManaCost: done
        ProcChance: done
        School : done
        CastingTimeIndex: done
        CategoryRecoveryTime: done
        DurationIndex:
        EffectAmplitude1:
        """
        theSpell = None
        for row in self.allSpells:
            if spellName.lower() == row[self.indexSpell.index('SpellName')].lower() and \
                    rank.lower() == row[self.indexSpell.index('Rank')].lower():

                #print(row)
                #print(row[self.indexSpell.index('EffectBasePoints1')])
                if row[self.indexSpell.index('BaseLevel')] is not '0':
                    theSpell = Spell(SpellName=spellName, Rank=rank)

                    for i in range(1,3):
                        if row[self.indexSpell.index('Effect%s' % str(i))] is not '0':
                            minDmg = int(row[self.indexSpell.index('EffectBasePoints%s'% str(i))]) + \
                                     int(row[self.indexSpell.index('EffectBaseDice%s'% str(i))])

                            maxDmg = int(row[self.indexSpell.index('EffectBasePoints%s'% str(i))]) + \
                                     (int(row[self.indexSpell.index('EffectDieSides%s'% str(i))]) * \
                                     int(row[self.indexSpell.index('EffectBaseDice%s'% str(i))]) + 1 )


                            if row[self.indexSpell.index('Effect%s'% str(i))] == '2':
                                theSpell.addAttribute(dmg_min = str(minDmg))
                                theSpell.addAttribute(dmg_max = str(maxDmg))
                            elif row[self.indexSpell.index('Effect%s'% str(i))] == '6':
                                theSpell.addAttribute(dmg_dot_min = str(minDmg))
                                theSpell.addAttribute(dmg_dot_max = str(maxDmg))

                                if row[self.indexSpell.index('EffectAmplitude1')] is not '0':
                                    theSpell.addAttribute(DotInterval =
                                                          row[self.indexSpell.index('EffectAmplitude%s'% str(i))])

                    theSpell.addAttribute(dmg_type = dmgType[row[self.indexSpell.index('School')]])

                    theSpell.addAttribute(CastTime =
                                          self.__getCastSpeed(row[self.indexSpell.index('CastingTimeIndex')]))

                    if row[self.indexSpell.index('ManaCost')] is not '0':
                        theSpell.addAttribute(ManaCost = row[self.indexSpell.index('ManaCost')])

                    if row[self.indexSpell.index('ProcChance')] is not '0':
                        theSpell.addAttribute(ProcChance = row[self.indexSpell.index('ProcChance')])

                    if row[self.indexSpell.index('CategoryRecoveryTime')] is not '0':
                        theSpell.addAttribute(Cooldown = row[self.indexSpell.index('CategoryRecoveryTime')])


                    theSpell.addAttribute(Duration =
                                          self.__getSpellDuration(row[self.indexSpell.index('DurationIndex')]))


                    #print(minDmg)
                    #print(maxDmg)
                    #for i,items in enumerate(row):
                    #    print('%s : %s' % (self.indexSpell[i] , items))
                    #print(self.indexSpell[i])
                #theItem = Item(Name = row[self.indexItem.index('name')])


                    #theSpell.printAll()

        return theSpell

    def clean(self):
        self.allItem = []
        self.allCastTimes = []
        self.allSpells = []
        self.allCastDurations = []







if __name__ == '__main__':
    oReader = ObjectReader()

    #edward = oReader.getItem('Blade of Eternal Darkness')
    #ragnaros = oReader.getItem('Draconic Avenger')

    sB =oReader.getSpell('Immolate','Rank 1')

    print('---------------------------')
    #edward.printAll()
    print ( '---------------------------')
    #ragnaros.printAll()
    print('---------------------------')
    sB.printAll()
    print('---------------------------')

