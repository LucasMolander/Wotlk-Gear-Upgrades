from data_util import DataUtil
from file_util import FileUtil
from calc_util import CalcUtil

import argparse
import copy

from pprint import pprint


class Globals(object):

    def __init__(self, sdPath):
        """
        Slots (currently - adding weapons and trinkets later):
        'Back', 'Belt', 'Bracer', 'Chest', 'Feet',
        'Gloves', 'Head', 'Legs', 'Neck', 'Ring', 'Shoulder'
        """

        paths = {
            'allGear':     'AllGear.json',
            'currentGear': 'CurrentGear.json',
        }

        self.currentGear = FileUtil.getJSONContents(paths['currentGear'])
        self.statDPS     = FileUtil.getJSONContents(sdPath)

        allGearList  = FileUtil.getJSONContents(paths['allGear'])
        self.allGear = DataUtil.toMap(allGearList, 'Name')


def calculateDiffs(globs):
    # Assign stats to the current gear and print it out
    currentGear = DataUtil.statifyCurrentGear(globs.currentGear, globs.allGear)

    # Print current gear
    items     = [currentGear[slot] for slot in sorted(list(currentGear.keys()))]
    headers   = ['Slot', 'Name', 'ilvl', 'Location', 'Boss']

    print('\nCurrent gear:\n')
    print(DataUtil.getTabulated(items, headers))

    # Print stat DPS
    print('\n\n\nStat DPS:\n')
    for stat in globs.statDPS:
        print('%s:\t%.4f' % (stat, globs.statDPS[stat]))
    print('')

    # Partition all gear into slots
    allGear = CalcUtil.slotifyAllGear(globs.allGear)

    # Return a new object
    # Because mutation is wonky
    out = {}

    # For each current slot

    # print(list(currentGear.keys()))
    # exit(0)

    for slot in currentGear:
        out[slot] = {}

        curPiece = currentGear[slot]

        actualSlotString = CalcUtil.removeUnderscore(slot)
        otherPieces = allGear[actualSlotString]
        for name in otherPieces:
            # Making a deep copy gets rid of issues with having 2 ring slots.
            # The second DPSDiff calculation would clobber the original DPSDiff calculation.
            otherPiece = copy.deepcopy(otherPieces[name])
            otherPiece['DPSDiff'] = CalcUtil.calcDPSDiff(curPiece, otherPiece, globs.statDPS)

            out[slot][name] = otherPiece

    return out


def printUpgrades(allGear):
    print('')
    for slot in sorted(list(allGear.keys())):
        print('\n\n%s' % slot.upper())

        slotPieces = allGear[slot]

        sortedPieces = sorted(slotPieces.values(), lambda p1, p2: int(p2['DPSDiff'] - p1['DPSDiff']))
        headers      = ['DPSDiff', 'Name', 'ilvl', 'Location', 'Boss']
        gzFilters    = ['DPSDiff']

        print('')
        print(DataUtil.getTabulated(sortedPieces, headers, gzFilters=gzFilters))
        print('')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sd', type=str, required=True, help='Stat DPS values file location')
    args = parser.parse_args()

    globs = Globals(args.sd)

    allGear = calculateDiffs(globs)
    printUpgrades(allGear)


if __name__ == '__main__':
    main()

