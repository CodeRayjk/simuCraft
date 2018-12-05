
import csv
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

class Item():
    def __init__(self, **kwargs):
        self.info = kwargs

    def addAttribute(self,**kwargs):
        self.info.update(kwargs)

    def print(self):
        for key,item in self.info.items():
            print('%s:%s' %(key,item))



class ObjectReader():
    def __init__(self):
        readItem = csv.reader(open('C:\\Users\\Rayjk\PycharmProjects\simuCraft\database\item_template.csv'),delimiter = ',')
        self.allItem = []
        for line in readItem:
            self.indexItem = line
            break
        for line in readItem:
            self.allItem.append(line)

    def getItem(self,itemName):
        theItem = None
        for row in self.allItem:
            if itemName == row[self.indexItem.index('name')]:
                theItem = Item(Name = row[self.indexItem.index('name')])

                print(row)

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


        return theItem

    def getSpell(self):
        pass


oReader = ObjectReader()

edward = oReader.getItem('Wand of Eternal Light')
ragnaros = oReader.getItem('Finkle\'s Lava Dredger')

edward.print()
ragnaros.print()

"""""



AllItem = csv.reader(open('C:\\Users\\Rayjk\PycharmProjects\simuCraft\database\item_template.csv'),delimiter = ',')
first = True
firstRow = None
for row in AllItem:
    for item in row:
        if 'Might of' in item:
            #print(row)
            print(row[firstRow.index('name')])
            if row[firstRow.index('armor')] is not '0':
                print( 'Armor : %s' % row[firstRow.index('armor')])

            for i in range(1,6):
                if row[firstRow.index('stat_type%d' % i)] is not '0':
                    print('%s : %s' % (attributeConv[row[firstRow.index('stat_type%d' % i)]], row[firstRow.index('stat_value%d' % i)]))

            print('---------------------')

            #print( '%s : %s' % (attributeConv[row[firstRow.index('stat_type1')]],row[firstRow.index('stat_value1')]))
            #print('%s : %s' % (attributeConv[row[firstRow.index('stat_type2')]], row[firstRow.index('stat_value2')]))
            #print('%s : %s' % (attributeConv[row[firstRow.index('stat_type3')]], row[firstRow.index('stat_value3')]))


"""

