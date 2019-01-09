#
# This class houses temporary tests to figure things out / debug stuff.
# Its functions might be useful later, so they live here.
#

from data_util import DataUtil
from file_util import FileUtil

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


def main():
    # globs = Globals('EP_Assassination.json')
    # TempTests.printSlots(globs.allGear)

    TempTests.ensureUniqueGearNames()


if __name__ == '__main__':
    main()