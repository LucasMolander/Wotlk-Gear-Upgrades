#
# This class houses temporary tests to figure things out / debug stuff.
# Its functions might be useful later, so they live here.
#

from data_util import DataUtil
from file_util import FileUtil
from calc_util import CalcUtil

from main import Globals

from pprint import pprint

class TempTests(object):

    #
    # Gets the names of all the slots.
    #
    @staticmethod
    def printSlots(allGear):
        slots = set()
        for name in allGear:
            piece = allGear[name]
            slots.add(piece['Slot'])

        pprint(slots)


    #
    # Makes sure the name of all items is unique.
    #
    @staticmethod
    def ensureUniqueGearNames():
        allGearList  = FileUtil.getJSONContents('AllGear.json')
        allGear      = DataUtil.toMap(allGearList, 'Name')

        print('%d items in list' % len(allGearList))
        print('%d items in map' % len(list(allGear.keys())))

        nRings = 0
        for name in allGear:
            piece = allGear[name]
            if (piece['Slot'] == 'Ring'):
                nRings += 1

        print('%d rings' % nRings)


    #
    # Prints out all gear of a given slot
    #
    @staticmethod
    def printAllGear(slot, globs):
        nameToPiece = globs.allGear[slot]

        for name in nameToPiece:
            piece = nameToPiece[name]
            piece['DPS'] = CalcUtil.calcDPS(piece, globs.statDPS, globs.charInfo)

        items = sorted(list(nameToPiece.values()), lambda p1, p2: int(p2['DPS'] - p1['DPS']) )
        headers = ['Name', 'ilvl', 'DPS', 'Location', 'Boss']

        print(DataUtil.getTabulated(items, headers))

        # for t in trinkets:
        #     print(t['Name'])


def main():
    # globs = Globals('SD_Assassination.json')
    # TempTests.printSlots(globs.allGear)
    # TempTests.ensureUniqueGearNames()

    globs = Globals('SD_Combat.json')
    TempTests.printAllGear('Trinket', globs)


if __name__ == '__main__':
    main()