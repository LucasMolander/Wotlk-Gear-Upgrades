#
# This file is for just running quick tests to develop proofs of concept.
#
# This file is NOT for keeping around potentially re-usable tests.
#
# IMPORTANT
# Remember to remove un-used packages from requirements.txt!
#


#
# TODO
# Remove koala2 from requirements.txt if I don't end up using it!
#

from koala.ExcelCompiler import ExcelCompiler

# c = ExcelCompiler('Combat - Current - Copy.xls')
# All sheets: Equipment, Cycles, Races, Gear, Gems, Settings, Calcs
c = ExcelCompiler('Combat.xlsx', ignore_sheets=['Gems', 'Settings', 'Cycles', 'Races', 'Gear', 'Equpiment'])
sp = c.gen_graph()



# #
# # TODO
# # Remove xlrd from requirements.txt if I don't end up using it!
# #
# import xlrd

# myBook = xlrd.open_workbook('Combat - Current - Copy.xls')
# print(myBook)

# print(myBook.complex)

# theSheet = myBook.sheet_by_name('Calcs')
# print(theSheet)

# aCol = theSheet.col(1)

# for cell in aCol:
# 	print(dir(cell))
# 	print(cell.dump)
# 	exit()



# #
# # TODO
# # Remove pycel-x from requirements.txt if I don't end up using it!
# #

# from pycel import ExcelCompiler

# # print(ExcelCompiler)


# import pycel
# from pycel import *

# from pprint import pprint

# pprint(vars(pycel))

# for bi in pycel.__builtins__:
# 	print(bi)

# pprint(pycel.excelfile)
