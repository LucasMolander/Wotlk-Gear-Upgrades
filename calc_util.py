#
# Contains functions that are helpful for calculating DPS stuff.
#
class CalcUtil(object):

    #
    # asdf
    #
    @staticmethod
    def getTotalStats(nameToPiece, statsToGet):
        allStats = {}
        for stat in statsToGet:
            # allStats[stat] = sum([nameToPiece[name][stat] for name in nameToPiece])

            allStats[stat] = 0
            for name in nameToPiece:
                piece = nameToPiece[name]

                if (piece['Slot'] == 'Trinket'):
                    flatStats = piece['Flat Stats']
                    added = flatStats[stat] if stat in flatStats else 0
                else:
                    added = piece[stat]

                allStats[stat] += added
                if (added > 0):
                    print('%s gives %.2f %s' % (piece['Name'], added, stat))


            print('\n%.2f total %s\n\n' % (allStats[stat], stat))

        return allStats


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


    #
    # Calculates the DPS of a piece.
    #
    @staticmethod
    def calcDPS(piece, statDPS):
        if (piece['Slot'] == 'Trinket'):
            return 0
        else:
            statDPS = CalcUtil.calcStatDPS(piece, statDPS)
            gemDPS = CalcUtil.calcGemDPS(piece)
            return statDPS + gemDPS


    # @staticmethod
    # def calcDPSDiff(piece1, piece2, statDPS):
    #     if (piece1['slot'] == 'Trinket'):
    #         pass
    #     else:
    #         # Calculate the DPS delta due to the stats
    #         statDelta = CalcUtil.calcStatDPS(piece2, statDPS) - CalcUtil.calcStatDPS(piece1, statDPS)

    #         # Calculate the DPS delta due to the gems
    #         gemDelta = CalcUtil.calcGemDPS(piece2) - CalcUtil.calcGemDPS(piece1)

    #         return (statDelta + gemDelta)


    @staticmethod
    def calcTrinketUtil(trinket):
        pass




# Ret DPS calc

# # NORM PROCS
# (
#     (
#         # Number of critical-hit norm procs
#         (CritTotal% * 'DPS Calc'!D79)
#         *
#         (
#             # Half of crit damage
#             (0.5 * 'DPS Calc'!F14)
#             +

#             # SoV crit
#             IF(SealSelection="SoV",'DPS Calc'!J30,0)
#             +

#             # SoC crit
#             IF(SealSelection="SoC",'DPS Calc'!J11,0)
#             +

#             # SoR crit
#             IF(SealSelection="SoR",'DPS Calc'!J18,0)
#         )
#     )
#     +
#     (
#         # Number of regular-hit norm procs
#         ((1 - CritTotal%) * 'DPS Calc'!D79)
#         *
#         (
#             # Same shit as above
#             (0.5 * 'DPS Calc'!F13)
#             +
#             IF(SealSelection="SoV",'DPS Calc'!J29,0)
#             +
#             IF(SealSelection="SoC",'DPS Calc'!J10,0)
#             +
#             IF(SealSelection="SoR",'DPS Calc'!J18,0)
#         )
#     )


# AW PROCS
#     +
#     (
#         (CritTotal% * 'DPS Calc'!D80)
#         *
#         (
#             (0.5 * 'DPS Calc'!G14)
#             +
#             IF(SealSelection="SoV",'DPS Calc'!K30,0)
#             + 
#             IF(SealSelection="SoC",'DPS Calc'!K11,0)
#             +
#             IF(SealSelection="SoR",'DPS Calc'!K18,0)
#         )
#     )
#     +
#     (
#         ((1 - CritTotal%) * 'DPS Calc'!D80)
#         *
#         (
#             (0.5 * 'DPS Calc'!G13)
#             +
#             IF(SealSelection="SoV",'DPS Calc'!K29,0)
#             +
#             IF(SealSelection="SoC",'DPS Calc'!K10,0)
#             +
#             IF(SealSelection="SoR",'DPS Calc'!K18,0)
#         )
#     )
# )
# /
# Length