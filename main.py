from data_util import DataUtil
from file_util import FileUtil
from calc_util import CalcUtil

import argparse
import copy

from pprint import pprint


class Globals(object):

    allStats = ['AP', 'Str', 'Agi', 'Crit', 'Hit', 'WE', 'Haste', 'Arpen']

    def __init__(self, charInfoPath):
        """
        Slots (currently - adding weapons and trinkets later):
        'Back', 'Belt', 'Bracer', 'Chest', 'Feet',
        'Gloves', 'Head', 'Legs', 'Neck', 'Ring', 'Shoulder'
        """

        paths = {
            'allGear':     'AllGear.json',
            'trinkets':    'Trinkets.json'
        }

        self.charInfo = FileUtil.getJSONContents(charInfoPath)

        allGearList     = FileUtil.getJSONContents(paths['allGear'])
        allTrinketsList = FileUtil.getJSONContents(paths['trinkets'])

        # They don't exlicitly say that they're trinkets
        for trink in allTrinketsList:
            trink['Slot'] = 'Trinket'

        # Combine all gear into one list
        self.allGear = []
        self.allGear.extend(allGearList)
        self.allGear.extend(allTrinketsList)

        # Then turn that list into a map from name to the piece of gear
        self.allGear = DataUtil.toMap(self.allGear, 'Name')

        # Load the current gear into memory
        self.currentGear = DataUtil.statifyNamedGear(self.charInfo['Current Gear'], self.allGear)



        # TODO
        # SEE IF THIS DOESN'T BREAK THINGS LATER ON IN EXECUTION
        # (Might not be kosher if slotified this early)
        self.allGear = CalcUtil.slotifyAllGear(self.allGear)



        # Calculate each piece's DPS
        for name in self.currentGear:
            piece = self.currentGear[name]
            piece['DPS'] = CalcUtil.calcDPS(piece, self.charInfo)

        # Get some basic overall stats about the current gear
        self.totalStats = CalcUtil.getTotalStats(self.currentGear, Globals.allStats)


def calculateDiffs(globs):
    # Assign stats to the current gear and print it out
    currentGear = copy.deepcopy(globs.currentGear)

    # Print current gear
    items   = [currentGear[slot] for slot in sorted(list(currentGear.keys()))]
    headers = ['Slot', 'Name', 'ilvl', 'Location', 'Boss', 'DPS']

    print('\nCurrent gear (%s %s):\n' % (globs.charInfo['Spec'], globs.charInfo['Class']))
    print(DataUtil.getTabulated(items, headers))

    # Print stat DPS
    print('\n\n\nStat DPS:\n')
    for stat in globs.charInfo['Stat DPS']:
        value = globs.charInfo['Stat DPS'][stat]
        print('%s:\t%.4f' % (stat, value))
    print('')



    # TODO
    # Factored this out into the Globals constructor.
    # Might want to get rid of this for sure later.
    # # Partition all gear into slots
    # allGear = CalcUtil.slotifyAllGear(globs.allGear)



    # Return a new object
    # Because mutation is wonky
    out = {}

    for slot in list(globs.allGear.keys()):
        out[slot] = {}

        # curPiece = currentGear[slot]

        actualSlotString = CalcUtil.removeUnderscore(slot)
        otherPieces = globs.allGear[actualSlotString]
        for name in otherPieces:
            # Making a deep copy gets rid of issues with having 2 ring slots.
            # The second DPSDiff calculation would clobber the original DPSDiff calculation.
            otherPiece = copy.deepcopy(otherPieces[name])
            # otherPiece['DPSDiff'] = CalcUtil.calcDPSDiff(curPiece, otherPiece, globs.statDPS)
            otherPiece['DPS'] = CalcUtil.calcDPS(otherPiece, globs.charInfo)

            out[slot][name] = otherPiece

    return out


def printAllGear(allGear):
    headerString = 'ALL GEAR'
    print('\n\n\n%s\n%s\n' % (headerString, '-' * len(headerString)))

    for slot in sorted(list(allGear.keys())):
        print('\n\n%s' % slot.upper())

        slotPieces = allGear[slot]

        sortedPieces = sorted(slotPieces.values(), lambda p1, p2: int(p2['DPS'] - p1['DPS']))
        headers      = ['DPS', 'Name', 'ilvl', 'Location', 'Boss']

        print('')
        print(DataUtil.getTabulated(sortedPieces, headers))
        print('')


def printUpgrades(currentGear, allGear):
    headerString = 'UPGRADES'
    print('\n\n\n%s\n%s\n' % (headerString, '-' * len(headerString)))

    headers = ['DPS Diff', 'Name', 'ilvl', 'Location', 'Boss']

    for slot in sorted(list(currentGear.keys())):
        piece = currentGear[slot]
        print('\n\n\n%s (%s, %.2f DPS)' % (slot, piece['Name'], piece['DPS']))

        actualSlotString = CalcUtil.removeUnderscore(slot)

        outputItems = []

        for otherName in allGear[actualSlotString]:
            otherPiece = copy.deepcopy(allGear[actualSlotString][otherName])
            otherPiece['DPS Diff'] = otherPiece['DPS'] - piece['DPS']

            if (otherPiece['DPS Diff'] > 0):
                outputItems.append(otherPiece)

        outputItems.sort(lambda p1, p2: int(p2['DPS'] - p1['DPS']))

        print('')
        print(DataUtil.getTabulated(outputItems, headers))
        print('')


    # for slot in allGear:
    #     slotItems = allGear[slot]
    #     print(slot)
    #     for otherName in slotItems:
    #         otherPiece = slotItems[otherName]
    #         print('\t%s (%.2f)' % (otherName, otherPiece['DPS']))


    # print('')
    # for slot in sorted(list(allGear.keys())):
    #     print('\n\n%s' % slot.upper())

    #     slotPieces = allGear[slot]

    #     sortedPieces = sorted(slotPieces.values(), lambda p1, p2: int(p2['DPSDiff'] - p1['DPSDiff']))
    #     headers      = ['DPSDiff', 'Name', 'ilvl', 'Location', 'Boss']
    #     gzFilters    = ['DPSDiff']

    #     print('')
    #     print(DataUtil.getTabulated(sortedPieces, headers, gzFilters=gzFilters))
    #     print('')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--charInfo', type=str, required=True, help='Character into file')
    parser.add_argument('--allGear', default=False, action='store_true', help='Show DPS for all gear')
    args = parser.parse_args()

    globs = Globals(args.charInfo)

    allGear = calculateDiffs(globs)

    if (args.allGear):
        printAllGear(allGear)
    else:
        printUpgrades(globs.currentGear, allGear)


if __name__ == '__main__':
    main()

