from data_util import DataUtil
from file_util import FileUtil
from calc_util import CalcUtil

import argparse

from tabulate import tabulate
from pprint import pprint


class Globals(object):

    def __init__(self, epPath):
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
        self.statDPS     = FileUtil.getJSONContents(epPath)

        allGearList  = FileUtil.getJSONContents(paths['allGear'])
        self.allGear = DataUtil.toMap(allGearList, 'Name')


def calculateDiffs(globs):
    # Assign stats to the current gear and print it out
    currentGear = CalcUtil.statifyCurrentGear(globs.currentGear, globs.allGear)
    print('Current gear:')
    CalcUtil.printCurrentGear(currentGear)
    print('')

    # Break up all gear by slot
    allGear = CalcUtil.slotifyAllGear(globs.allGear)

    # Return a new object
    # Because mutation is wonky
    out = {}

    # For each current slot
    for slot in currentGear:
        out[slot] = {}

        curPiece = currentGear[slot]
        print('Current %s: %s' % (slot, curPiece['Name']))

        actualSlotString = CalcUtil.removeUnderscore(slot)
        otherPieces = allGear[actualSlotString]
        for name in otherPieces:
            otherPiece = otherPieces[name]
            otherPiece['DPSDiff'] = CalcUtil.calcDPSDiff(curPiece, otherPiece, globs.statDPS)

            out[slot][name] = otherPiece

    return out


def printUpgrades(allGear):
    print('')
    for slot in sorted(list(allGear.keys())):
        print('\n\n%s' % slot.upper())

        slotPieces = allGear[slot]
        sortedPieces = sorted(slotPieces.values(), lambda p1, p2: int(p2['DPSDiff'] - p1['DPSDiff']))

        headers = [
            'DPSDiff',
            'Name',
            'ilvl',
            'Location',
            'Boss'
        ]
        valuesLists = []
        for piece in sortedPieces:
            if (piece['DPSDiff'] > 0):
                values = [
                    piece[h]
                    for h in headers
                ]
                valuesLists.append(values)

        print('')
        print(tabulate(valuesLists, headers=headers))
        print('')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ep', type=str, required=True, help='EP values file location')
    args = parser.parse_args()

    globs = Globals(args.ep)

    print('\nStat DPS:')
    pprint(globs.statDPS)
    print('')

    allGear = calculateDiffs(globs)
    printUpgrades(allGear)


if __name__ == '__main__':
    main()

