from AvailabilityFile import AvailabilityFile

import pandas as pd
import datetime as dtime


def drawDictionary(dic):
    for k,v in dic.items():
        print(f"key: {k}, val: {v}\n")




"""Purpose of this object will be to make doing comparisons between people and their availabilities easier, the object will accomplish this
by creating a dictionary, where the key is the name of the person, and the value is going to be two arrays(Parallel) having start and end times
error checking: if start times not equal to end times"""
class EasyAvailability:
    keyName_valStartTimeEndTimeParallelArrs = dict()
    keyName_valAvailableMinutes = dict()
    availFile_obj = AvailabilityFile

    def __init__(self,availFile_obj) -> None:
        self.availFile_obj = availFile_obj

    def generateDictionary(self):
        for innerArr in self.availFile_obj.name_avail_matrix:
            parallel_arr_start_end = list()
            tmp_start = list()
            tmp_end = list()
            #get rid of the NaT's so that we can do error checking, otherwise check will not work
            for val in innerArr[1::2]:
                if pd.isnull(val):
                    continue
                tmp_start.append(val)
            for val in innerArr[2::2]:
                if pd.isnull(val):
                    continue
                tmp_end.append(val)

            assert(len(tmp_start) == len(tmp_end)), "your start and end times arent lining up, make sure that you have the same # start and end times, thanks :)"#then diff num start and end times
            parallel_arr_start_end.append(tmp_start.copy())
            parallel_arr_start_end.append(tmp_end.copy())

            self.keyName_valStartTimeEndTimeParallelArrs[innerArr[0]] = parallel_arr_start_end
        
        for name,start_end_parallelArrs in self.keyName_valStartTimeEndTimeParallelArrs.items():
            tmp_for_starts = start_end_parallelArrs[0]
            i = -1
            tmp_to_copy = list()
            for start_time in tmp_for_starts:
                i += 1
                """NOTE: Right here i am converting the DateTimeIndex object that pandas creates, and swapping it to just a normal array by using the .values at the end
                of the line of code below, only thing is that the values look a tiny bit different when i do that, so if later on i have some issue reading the times
                and comparing them or something, then come back here and alter this, but it shouldn't matter for my code as i just wanna make minutes arrays for every
                member and check whether they share the same exact time, which should remain the same whether it looks a little different than in the datetimeindex format
                should not matter for my code"""
                tmp = pd.date_range(start=start_time,end=start_end_parallelArrs[1][i] - pd.DateOffset(minutes=1),freq='T').values
                for ugly_formatted_date in tmp:#this loop is to greatly compress the 16 chars into just the day of the week,time in hours, time in minutes
                    tmp_datetime = pd.to_datetime(ugly_formatted_date)
                    str_datetime = tmp_datetime.strftime("%a%H:%M")
                    tmp_to_copy.append(str_datetime)
                #(format="%Y-%m-%d %H:%M")
            self.keyName_valAvailableMinutes[name]  = tmp_to_copy.copy()
        # drawDictionary(self.keyName_valAvailableMinutes) # verified dictionary has every name and their corresponding available minutes
        