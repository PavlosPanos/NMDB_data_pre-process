import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import sys 

def boolean_conversion(string):
    if (string=="True"): return(True)
    elif (string=="False"): return(False)
    else :
        print("ERROR - A boolean answer was expected ")
        sys.exit()



# OPTION TO GET YEAR,MONTH,DAY,HOUR,MIN,SEC IN SEPERATE COLUMNS ---> i will include a readmy.txt that says how to manipulate the date library in python  --- FOR THE USER ---
option=boolean_conversion(input("Type 'True' if you want to add a seperate column for the year/month etc. or 'False' if not :"))
replace_null_with_zero=True
cut_null_lines=False


#------------------------------- NOT FOR THE USER
has_null=False
has_negative=False



#opening the .txt file and reading it's lines (putting them into a list with theindex being each line)
with open("NMDB_Data.txt") as f:
    contents_list = f.readlines()
#print(contents_list[0])# <--- bebbug comment
#print(type(contents_list[0])) <--- bebbug comment

#-------------------------------

# creating the time index of the data frame (two types so the user can decide)
year_series=[]
month_series=[]
day_series=[]
hour_series=[]
min_series=[]
second_series=[]
time_series=[]
for i in range(1,len(contents_list)):
    time_row=contents_list[i].split(" ")
    #print(time_row) <--- bebbug comment
    time_row_date=time_row[0].split("-")
    time_row_time=time_row[1].split(":")
    year=int(time_row_date[0])
    month=int(time_row_date[1])
    day=int(time_row_date[2])
    hour=int(time_row_time[0])
    min=int(time_row_time[1])
    dummy=time_row_time[2].split(";")
    sec=int(dummy[0])
    if (option==True):
        year_series.append(year)
        month_series.append(month)
        day_series.append(day)
        hour_series.append(hour)
        min_series.append(min)
        second_series.append(sec)
    date=datetime.datetime(year,month,day,hour,min,sec)
    time_series.append(date)

#-------------------------------    

#creating the mane data frame (just tha dates)
multiple_stations_data=pd.DataFrame({"Date":time_series})
#if option add the extra columns
if (option==True):
    multiple_stations_data["Year"]=year_series
    multiple_stations_data["Month"]=month_series
    multiple_stations_data["Day"]=day_series
    multiple_stations_data["Hour"]=hour_series
    multiple_stations_data["Minute"]=min_series
    multiple_stations_data["Second"]=second_series
    
#-------------------------------    

# creating a list with all the stations names
Station_Names=["AATA","BKSN","DOMC","INVK","JUNG","LMKS","MWSN","NEWK","PTFM","SOPB","TXBY","AATB","CALG","DRBS","IRK2","JUNG1",
"MCRL","MXCO","NRLK","PWNK","SOPO","YKTK","APTY","CALM","ESOI","IRK3","KERG","MGDN","NAIN","NVBK","ROME","TERA","ARNM","DJON",
"FSMT","IRKT","KIEL","MOSC","NANM","OULU","SANB","THUL","ATHN","DOMB","HRMS","JBGO","KIEL2","MRNY","NEU3","PSNM","SNAE","TSMB"]
Station_R =[5.9,5.7,0.01,0.3,4.49,3.84,0.22,2.4,6.98,0.1,0.48,5.9,1.08,3.18,3.64,4.49,
2.46,8.28,0.63,0.3,0.1,1.65,0.65,6.95,10.75,3.64,1.14,2.1,0.3,2.91,6.27,0.01,7.1,11.2,
0.3,3.64,2.36,2.34,7.1,0.81,0.73,0.3,8.53,0.01,4.58,0.3,2.36,0.03,0.1,16.8,0.73,9.15]
Station_Alt =[897,1700,3233,21,3570,2634,30,50,1351,2820,0,3340,1123,225,2000,3475,
200,2274,0,53,2820,105,181,708,2055,3000,33,220,46,163,0,32,3200,200,
180,435,54,200,2000,15,52,26,260,3233,26,29,54,30,40,2565,856,1240]


# --------------- getting the first row to check with stations we have
for i in range(len(contents_list[0])):
    first_row=contents_list[0]
names_row=first_row.split(" ")
  

# -------------- creating a list with the stations that have been called (and their stations_names indexes)
Stations_called=[]
Stations_called_index=[]
for i in range(len(Station_Names)):
    if Station_Names[i]  in names_row:
        Stations_called.append(Station_Names[i])
        Stations_called_index.append(i)
    if Station_Names[i]+"\n"  in names_row:
        Stations_called.append(Station_Names[i])
        Stations_called_index.append(i)

# ----------- Shorting the stations by magnetic rigidity (its the way NMDB puts them)

def SortingBubble(list,index_list):
    loop = len(list)
    swapped = False
    for i in range(loop-1):
        for j in range(0, loop-i-1):
            if list[j] < list[j + 1]:
                swapped = True
                list[j], list[j + 1] = list[j + 1], list[j]
                index_list[j], index_list[j + 1] = index_list[j + 1], index_list[j]
        if not swapped:
            return list,index_list
    return list,index_list

Stations_called_R=[]
for i in range(len(Stations_called)):
    Stations_called_R.append(Station_R[Stations_called_index[i]])

Sorted_R,Sorted_index = SortingBubble(Stations_called_R,Stations_called_index)
#-----------------------print(Sorted_index,Sorted_R)

# --------------- Making correction only for the Stations with the same R value

# ------------- Function that finds the Stations with the same R
def Same_R_Stations(Sorted_index,Sorted_R):
    Same_R_list=[]
    for i in range(len(Sorted_index)):
        dummy_R=Sorted_R[i]
        flag=0
        flag_R=0
        for j in range(len(Sorted_index)):
            if(dummy_R==Sorted_R[j] and j !=i):
                if (flag==0):
                    for k in range(len(Same_R_list)):
                        if (Same_R_list[k]==Sorted_R[i]):
                            flag_R+=1
                    if (flag_R==0):
                        Same_R_list.append(" ")
                        Same_R_list.append(Sorted_R[i])
                    flag+=1
                Same_R_list.append(Station_Names[Sorted_index[j]])
    return(Same_R_list)

# ----------- determining which column of the data corresponed to which station index
station_first_row_index_list=[]
station_index_list=[]
for j in range(len(Station_Names)):
    name=Station_Names[j]
    a=names_row
    empty_counter=0
    ATHN_location=0
    for i in range(len(a)):
        if (a[i]=="" and ATHN_location==0):
            #print("hi")
            empty_counter+=1
        if name in a[i]:
            #print(name , i )
            ATHN_location = i
    station_first_row_index=1+ATHN_location-empty_counter
    if(station_first_row_index>0):
        station_first_row_index_list.append(station_first_row_index)
        station_index_list.append(j)
        #print(name,station_first_row_index)
#print(station_first_row_index_list)
#print(station_index_list)        

# -------- null checker and replacing with zero ??? (I CAN JUST CUT THESE LINES AND NOT INCLUDE THEM --- OR I CAN GIVE A VALUE OF -100 AND THEN CUT THEM)
def null_with_zero(i):
    if (i=="   null" or i=="   null\n"):
        return (0)
    else: return(i)
def negative_with_zero(i):
    if (float(i)<0): return(0)
    else : return(i)

def all_data_corrections_with_zero(i):
    return(negative_with_zero(null_with_zero(i)))
# ------------------ Creating the dataframe with the givven stations        
        
for i in range(len(station_first_row_index_list)):
    data_list=[]
    for j in range(1,len(contents_list)):
        a=contents_list[j].split(";")
        data_list.append(float(all_data_corrections_with_zero(a[station_first_row_index_list[i]])))
    #print(data_list)
    multiple_stations_data[Station_Names[station_index_list[i]]]=data_list   
        
print(multiple_stations_data)   
multiple_stations_data.to_excel("multiple_stations_data.xlsx")