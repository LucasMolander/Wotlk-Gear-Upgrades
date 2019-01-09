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
    # Returns the tabulated (table) representation of the given list of data items.
    #
    # gzFilters is the list of columns (keys) that must be > 0 to appear.
    # This is useful when you only want to print DPS increases, etc.
    # Might factor this out into a generic filtering class later.
    #
    @staticmethod
    def getTabulated(items, headers, gzFilters=[]):
        # Each element represents a row of values. 2D list.
        valuesLists = []

        for item in items:
            # If any item has a gzFilter field <= 0,
            # do not add it to the output
            toAdd = True
            for gzf in gzFilters:
                if (item[gzf] <= 0):
                    toAdd = False

            if (toAdd):
                # If we add the item to the output, append the list of its values
                values = [
                    item[h]
                    for h in headers
                ]
                valuesLists.append(values)

        return tabulate(valuesLists, headers=headers)
