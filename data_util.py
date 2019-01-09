#
# This class is mostly just for nice-to-have data structure manipulations.
#


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
