import config
from AvailabilityFile import AvailabilityFile
from GroupPriorityFile import GroupPriorityFile
from ComboHolder import ComboHolder
from SetFinder import SetFinder
from EasyAvailability import EasyAvailability
from ErrorChecker import ErrorChecker
from Performance import Performance

import pandas as pd

def main():
    prf_obj = Performance() ##keep this at the beginning
    prf_obj.start()

    e_check = ErrorChecker()

    # get availability file info
    avail_obj = AvailabilityFile(config.csv_availability_filename)
    e_check.checkAvail(avail_obj)
    # get priority file info
    pri_obj = GroupPriorityFile(config.csv_priority_filename)
    e_check.checkGroupPri(pri_obj)


    prf_obj.startCombo()
    # next generate a list of every possible combination and set of combos in the combo object
    combo_obj = ComboHolder(config.team_size,config.number_of_teams,pri_obj.group1,pri_obj.group2,pri_obj.group3,True)
    combo_obj.createCombos()
    combo_obj.createSets()
    prf_obj.endCombo()

    easyAvail_obj = EasyAvailability(avail_obj)
    easyAvail_obj.generateDictionary()


    prf_obj.startSetFinder()
    prf_obj.startSFInit()
    setFinder_obj = SetFinder(combo_obj,easyAvail_obj)
    prf_obj.endSFInit()
    prf_obj.startSFCMOD()
    setFinder_obj.createMinuteOverlapDic(config.minHoursOverlap,config.minDaysOverlap)
    prf_obj.endSFCMOD()
    prf_obj.startSFCSD()
    setFinder_obj.createSortedDic()
    prf_obj.endSFCSD()
    prf_obj.startSFCCD()
    setFinder_obj.createCompressedDic()
    prf_obj.endSFCCD()
    prf_obj.startSFDGS()
    setFinder_obj.drawGoodSets()
    prf_obj.endSFDGS()
    prf_obj.endSetFinder()




    #keep this at the end - for performance measuring purposes
    prf_obj.end()
    prf_obj.drawPerformance()