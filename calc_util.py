#
# Contains functions that are helpful for calculating DPS stuff.
#
class CalcUtil(object):


    #
    # Partitions gear into each slot.
    #
    # Transform map from being name --> piece to be
    # slot --> (name --> piece).
    #
    @staticmethod
    def slotifyAllGear(nameToPiece):
        ret = {}

        for name in nameToPiece:
            piece = nameToPiece[name]
            slot = piece['Slot']
            if (slot not in ret):
                ret[slot] = {}
            ret[slot][name] = piece

        return ret


    #
    # Maps logical slots like 'Ring_1' or 'Ring_2'
    # to just 'Ring'
    #
    @staticmethod
    def removeUnderscore(string):
        idx = string.find('_')
        if (idx >= 0):
            return string[0 : idx]
        else:
            return string


    #
    # Return the dot product of the piece's stats and the stat DPS values
    #
    @staticmethod
    def calcStatDPS(piece, statDPS):
        stats = list(statDPS.keys())

        # Zero out null values (just in case)
        for stat in stats:
            if (piece[stat] is None):
                piece[stat] = 0

        return sum([piece[stat] * statDPS[stat] for stat in stats])


    #
    # Calculates the DPS-add due to gems for a given piece.
    #
    # For now, just adds 40 DPS per gem slot.
    #
    @staticmethod
    def calcGemDPS(piece):
        dpsPerGem = 40
        totalDPS = 0

        for slotName in ['Gem 1', 'Gem 2', 'Gem 3', 'Gem 4']:
            if (piece[slotName] != None and piece[slotName] != ''):
                totalDPS += dpsPerGem

        return totalDPS


    @staticmethod
    def calcDPSDiff(piece1, piece2, statDPS):
        # Calculate the DPS delta due to the stats
        statDelta = CalcUtil.calcStatDPS(piece2, statDPS) - CalcUtil.calcStatDPS(piece1, statDPS)

        # Calculate the DPS delta due to the gems
        gemDelta = CalcUtil.calcGemDPS(piece2) - CalcUtil.calcGemDPS(piece1)

        return (statDelta + gemDelta)
