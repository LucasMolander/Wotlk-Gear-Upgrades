#
# This class is mostly just for nice-to-have data structure manipulations.
#

from tabulate import tabulate


class DataUtil(object):

    #
    # Converts a list of objects (each of which has the key field)
    # into a map from that key to the object itself.
    #
    @staticmethod
    def toMap(objs, key):
        return {
            o[key]: o
            for o in objs
        }


    #
    # Because slotToPiece is just names.
    # Use the allGear map to get stats.
    #
    @staticmethod
    def statifyCurrentGear(slotToPiece, allGear):
        return {
            slot: allGear[slotToPiece[slot]]
            for slot in slotToPiece
        }


    #
    # Just prints the current gear and where it's from.
    # Where did you come from, Cotton Eye Joe?
    #
    @staticmethod
    def printCurrentGear(slotToPiece):
        for slot in slotToPiece:
            piece = slotToPiece[slot]
            print('%s: %s (ilvl %d from %s)' % (slot, piece['Name'], piece['ilvl'], piece['Location']))


    @staticmethod
    def getTabulated(items, headers, gzFilters):
        valuesLists = []
        for item in items:
            toAdd = True
            for gzf in gzFilters:
                if (item[gzf] <= 0):
                    toAdd = False

            if (toAdd):
                values = [
                    item[h]
                    for h in headers
                ]
                valuesLists.append(values)

        return tabulate(valuesLists, headers=headers)
