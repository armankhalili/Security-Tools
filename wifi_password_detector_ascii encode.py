# 👇import libraries
import subprocess   #👈 to run CMD command
from prettytable import PrettyTable # 👈to create table for store data
from datetime import datetime   # 👈to create uniqe filename

# CMD command to get name of ssid
temp_name = str(subprocess.check_output("netsh wlan show profile").decode("ascii")).split("\n") 

ssid = []  # 👈to store list SSID 
data=[]    # 👈to store all attribute of certain access piont
num = 1    # 👈to count number of the table row

# store date and time to generate file name ↩️
# 👇and covert formate from "2021-11-05 03:42:16.500038.txt" to "2021-11-05_03-42-16.500038.txt"
now = str(datetime.now()).replace(" ","_").replace(":","-") 

filename = str(now) + ".txt" #Generate file name 

# 👇Create and open file 
myfile= open(filename,"w+")

# 👇Create out table to store data
mytable = PrettyTable(['#','SSID','Key','Authentication'])

# 👇Generate list of SSIDs and store in ssid variable
for a in temp_name :
    if "All User Profile" in a :
        ssid.append(a.strip())

# 👇Generate clear list of SSIDs and restore "ssid"
for index in range(len(ssid)) :
    temp = ssid[index]
    ssid[index] = temp[23:]

for name in ssid :

    # 👇Create number of index columns
    data.append(num)
    num += 1

    # 👇Write SSID 
    data.append(name)
    command = "netsh wlan show profile \"{}\" key=clear".format(name)

    # 👇Get Data About Certain SSID
    case = str(subprocess.check_output("netsh wlan show profile \"{}\" key=clear".format(name)).decode("ascii")).split("\n")
    
    # 👇Write Key Content

    # 👇detect all authentication and seprate password and store in password variable
    if len((case[32].split(":"))) > 1 :
        password = (case[32].split(":"))[1]
        data.append(password[:-2])

    # anything else be open  authentication which is have no password so our list have less than 2 index ↩️
    # 👇To handling open authentication which is password variable equal to "" (replace "" by "NULL")
    else :
            data.append("NULL")

    # 👇Write Authentication Type
    authentication = (case[29].split(":"))[1]
    # To handling open authentication (replace "absent" by "No authentication (open)")
    if len(authentication[:-2]) == 6 :
        data.append("No authentication (open)")
    else :
        data.append(authentication[:-2])

    # 👇Insert list of Data in one tables row
    mytable.add_row(data)
    data.clear()

myfile.write(str(mytable))  # 👈store table to txt file
myfile.close    # 👈close file

