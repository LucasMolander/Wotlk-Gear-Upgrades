import copy

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
                # if (added > 0):
                #     print('%s gives %.2f %s' % (piece['Name'], added, stat))


            # print('\n%.2f total %s\n\n' % (allStats[stat], stat))

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
    def calcStatDPS(piece, charInfo):
        stats = list(charInfo['Stat DPS'].keys())

        # Zero out null values (just in case)
        for stat in stats:
            if (stat not in piece or piece[stat] is None):
                piece[stat] = 0

        return sum([piece[stat] * charInfo['Stat DPS'][stat] for stat in stats])


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
    def calcTrinketDPS(trinket, charInfo):
        # statDPS, charInfo

        # Always calculate flat stats
        flatStatDPS = CalcUtil.calcStatDPS(trinket['Flat Stats'], charInfo)

        # Chance on hit to proc (Stats, Damage, Stacks, or DBW)
        if ('On Hit' in trinket):
            onHit = trinket['On Hit']

            if (onHit['Type'] == 'Stats'):
                # Just add stats, multiplying by the ratio of time they exist
                uptimePct = float(onHit['Duration']) / float(onHit['ICD'])
                moreStats = onHit['Stats']
                moreDPS   = CalcUtil.calcStatDPS(moreStats, charInfo)
                extraDPS  = uptimePct * moreDPS
            elif (onHit['Type'] == 'Damage'):
                # Ignore crit for now because these trinkets are ass anyway
                extraDPS = float(onHit['Damage']) / float(onHit['ICD'])
            elif (onHit['Type'] == 'Stacks'):
                stacks = onHit['Stacks']
                n = stacks['N']
                moreStats = copy.deepcopy(stacks['Stats'])

                # Assume max stacks
                for ms in moreStats:
                    moreStats[ms] *= n

                # Multiply by ~0.975 to account for ramp up
                fightLength = 300.0
                stacksPerSecond = 4.0 / 3.0
                tToMaxStacks = float(n) / stacksPerSecond
                ratioNotMax = tToMaxStacks / fightLength
                multiplier = 1.0 - (ratioNotMax / 2.0)

                moreDPS = CalcUtil.calcStatDPS(moreStats, charInfo)
                extraDPS = multiplier * moreDPS
            elif (onHit['Type'] == 'DBW'):
                uptimePct = float(onHit['Duration']) / float(onHit['ICD'])

                classStats = onHit['Class Stats']
                moreStats = classStats[charInfo['Class']]
                moreDPS = CalcUtil.calcStatDPS(moreStats, charInfo)

                extraDPS = (moreDPS * uptimePct) / 3.0
            else:
                extraDPS = 0
        else:
            extraDPS = 0


        return flatStatDPS + extraDPS


    #
    # Calculates the DPS of a piece.
    #
    @staticmethod
    def calcDPS(piece, charInfo):
        if (piece['Slot'] == 'Trinket'):
            return CalcUtil.calcTrinketDPS(piece, charInfo)
        else:
            statDPS = CalcUtil.calcStatDPS(piece, charInfo)
            gemDPS  = CalcUtil.calcGemDPS(piece)
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