# Simple template for controlling GPS-X from a Python interpreter
# This script is launched from GPS-X
# GPS-X copyright 2020 Hydromantis
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import csv
############################USER INPUTS############################
CommInt = 0.05
StopTime = 60.0
#adding 1 since it is otherwise between 0 and 49.95
bodi = ["BOD1"]
codi = ["COD1"] 
bod = ["BOD31"]
cod = ["COD31"]
bod_c = ["BOD_C"]
cod_c = ["COD_C"]
ts = ["TIME"]
c = ["C"]
###################################################################

#############################FUNCTIONS#############################

# start() function executed once at simulation start
#
def start():
    global CommInt, StopTime
    try:
        gpsx.setTstop(StopTime)
        gpsx.setCint(CommInt)
    except Exception as e:
        print(e)

# cint() function executed at every communication interval
#
def cint():
    global bod,cod,bod_c,cod_c,ts,c,bodi,codi
    try:
        #store the time
        a = round(gpsx.getValue("t"),2)
        ts.append(a)
        #store bod and cod
        bod.append(gpsx.getValue("bod31"))
        cod.append(gpsx.getValue("cod31"))
        bodi.append(gpsx.getValue("bod1"))
        codi.append(gpsx.getValue("cod1"))
        #calculate c value for bod and cod
        bod_c.append(min(50-gpsx.getValue("bod31"), max(25 - gpsx.getValue("bod31"), 0.7*gpsx.getValue("bod1")-gpsx.getValue("bod1")+gpsx.getValue("bod31"))))
        cod_c.append(min(250-gpsx.getValue("cod31"), max(125 - gpsx.getValue("cod31"), 0.75*gpsx.getValue("cod1")-gpsx.getValue("cod1")+gpsx.getValue("cod31"))))
        c.append(min(bod_c[-1],cod_c[-1]))
    except Exception as e:
        print(e)

# eor() function executed once at end of simulation
# finished set True is required to terminate the runSim() function
#
def eor():
    global finished
    finished = True
    try:
        pass
    except Exception as e:
        print(e)

# runSim() call starts simulation in GPS-X
try:
    #reset all the values to the base value
    gpsx.resetAllValues()
    #run the simulation
    runSim()
    #print values of bod and cod
    print(bodi)
    print(codi)
    print(ts)
    print(bod)
    print(cod)
    print(c)
    #calculate min c for bod and cod
    #min_bod_c = min(bod_c)
    #min_cod_c = min(cod_c)
    #print("Min BOD Robustness Value: ", min_bod_c)
    #print("Min COD Robustness Value: ", min_cod_c)
    fields=["TIME","BOD31","COD31","BOD1","COD1","BOD_C","COD_C","C"]
    rows= [ts,bod,cod,bodi,codi,bod_c,cod_c,c]
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        #writer.writerow(fields)
        writer.writerows(rows)
    
    #read csv file as a dataframe
    df = pd.read_csv('data.csv', index_col=0, header=None).T
    
    #create plots and save them to a file
    #print("Make the plots of bod and cod")
    #plt.plot(df.TIME, df.BOD10)
    #plt.xlabel('Time')
    #plt.ylabel('BOD Concentration')
    #plt.title('Robustness')
    #plt.savefig('bod.png')
    #plt.show()
    #plt.plot(df.TIME, df.COD10)
    #plt.xlabel('Time')
    #plt.ylabel('COD Concentration')
    #plt.title('Robustness')
    #plt.savefig('cod.png')
    #plt.show()
except Exception as e:
 print(e)
###################################################################

