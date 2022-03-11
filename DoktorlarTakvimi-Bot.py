from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import pymssql
from datetime import datetime
from pymssql import _mssql
from pymssql import _pymssql
import uuid
import decimal
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW

mydb = pymssql.connect(
        server="...!Private",
        user="kayitentu",
        password = "...!Private",
        database = "kayitentu"
    )
cursor =mydb.cursor()
cursor.execute("select TUserName from [kayitentu].[dbo].[Panel]")
TUserName = cursor.fetchall()
cursor.execute("select TPassword from [kayitentu].[dbo].[Panel]")
TPassword = cursor.fetchall()
cursor.execute("select DosyaYolu from [kayitentu].[dbo].[Panel]")
dosyaYolu=cursor.fetchall()

def splitmaker(deneme):
    deneme=str(deneme[0])  
    deneme= deneme.split(",")  
    deneme = deneme[0].split("(")
    deneme = deneme[1]
    deneme = deneme[1:len(deneme)-1]
    return(deneme)
   
def openWeb(UserName,Password):           
    browser.get("https://docplanner.doktortakvimi.com/#/calendar/week")
    browser.implicitly_wait(20)
    userLabel = browser.find_element_by_xpath('//*[@id="username"]')
    userLabel.send_keys(UserName)
    browser.implicitly_wait(20)
    passwordLabel = browser.find_element_by_xpath('//*[@id="password"]')
    passwordLabel.send_keys(Password)
    browser.implicitly_wait(20)
    loginButton = browser.find_element_by_xpath('/html/body/main/div/section/div[2]/form/div[3]/button')
    loginButton.click()
    time.sleep(8)
    browser.implicitly_wait(20)
    # nextweek = browser.find_element_by_xpath('//*[@id="calendar-base-layout"]/div/div[2]/div/div[1]/div/div/div[1]/div/button[2]')
    # nextweek.click()
    dates=browser.find_elements_by_class_name("day-name")
    datesArray=[]
    for p in dates:
        datesArray.append(p.text)
    dateToday = browser.find_element_by_class_name("is-today")
    dateToday=(dateToday.text)
    print(datesArray)
    global indexToday
    global endindex
    indexToday=datesArray.index(dateToday)
    indexToday= indexToday+2
    endindex = indexToday+2
    
    
def scan(DoctorID):
    for a in range(indexToday,endindex):    
        try: 
            n=1
            while True:  
                browser.implicitly_wait(20)                   
                event = browser.find_element_by_xpath('//*[@id="calendar-base-layout"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/table/tbody/tr/td/div/div/div/div[2]/table/tbody/tr/td[{}]/div/div[2]/div[{}]/a/div[1]/div/div/div[1]'.format(a,n))                                                                                     
                event.click()
                browser.implicitly_wait(10)       
                namePath = browser.find_element_by_xpath('/html/body/dralia-modal/div/div[2]/div/div/dralia-event-detail-modal/div/div/div[2]/div[2]/div[1]/div/dralia-appointment-summary-patient/div/div/div[1]/div[1]/div[2]/p[1]/strong')                       
                #hourPath = browser.find_element_by_xpath('/html/body/dralia-modal/div/div[2]/div/div/dralia-event-detail-modal/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/p[1]/strong')
                dayPath = browser.find_element_by_xpath('/html/body/dralia-modal/div/div[2]/div/div/dralia-event-detail-modal/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/p/strong/span[3]')     
                #hour=hourPath.text.split(" - ")
                nameFull = namePath.text                
                try:
                    phonePath= browser.find_element_by_xpath('/html/body/dralia-modal/div/div[2]/div/div/dralia-event-detail-modal/div/div/div[2]/div[2]/div[1]/div/dralia-appointment-summary-patient/div/div/div[1]/div[1]/div[2]/p[2]')
                    phone = phonePath.text
                except:
                    phone = ""
               
                hourStart=browser.find_element_by_xpath('/html/body/dralia-modal/div/div[2]/div/div/dralia-event-detail-modal/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/p/strong/span[1]')
                hourEnd = browser.find_element_by_xpath('/html/body/dralia-modal/div/div[2]/div/div/dralia-event-detail-modal/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/p/strong/span[2]')      
                day=dayPath.text.split(", ")
                date=day[1]
                hourStart=hourStart.text
                hourEnd=hourEnd.text
                if "ocak" in date:
                    date=date.replace(" ocak ","-01-")
                if "şubat" in date:
                    date=date.replace(" şubat ","-02-")
                if "mart" in date:
                    date=date.replace(" mart ","-03-")
                if "nisan" in date:
                    date=date.replace(" nisan ","-04-")
                if "mayıs" in date:
                    date=date.replace(" mayıs ","-05-")
                if "haziran" in date:
                    date=date.replace(" haziran ","-06-")
                if "temmuz" in date:
                    date=date.replace(" temmuz ","-07-")
                if "ağustos" in date:
                    date=date.replace(" ağustos ","-08-")
                if "eylül" in date:
                    date=date.replace(" eylül ","-09-")
                if "ekim" in date:
                    date=date.replace(" ekim ","-10-")
                if "kasım" in date:
                    date=date.replace(" kasım ","-11-")
                if "aralık" in date:
                    date=date.replace(" aralık ","-12-")
                        
                if len(date)==9:
                    date = "0"+date
                date=date[6:10]+date[2:5]+"-"+date[0:2]
                hourStart = date+" "+hourStart
                hourEnd = date + " " + hourEnd
                date=datetime.fromisoformat(date)
                hourStart=datetime.fromisoformat(hourStart)
                hourEnd=datetime.fromisoformat(hourEnd)
                print(hourEnd)

                inList = 0
                cursor.execute("SELECT Username  FROM [kayitentu].[dbo].[User]")
                names = cursor.fetchall()
                for m in range(len(names)):
                    if ("{}".format(nameFull)) in names[m]:
                        inList=1
                namePart = nameFull.split(" ")
                if len(namePart)==3:
                    nameFirst=("{} {}".format(namePart[0],namePart[1]))
                    nameLast = namePart[2]
                else:
                    nameFirst=namePart[0]
                    nameLast = namePart[1] 
                
                if inList == 0:
                    metaName2 = str('{'+'"Name": "{}","Surname": "{}","BirthDate": "2001-01-01","Gender": "None","Phone": "{}","Branch": "y","Address": "y"'.format(nameFirst,nameLast,phone)+'}')
                    metaName=str('{'+'"Name": "{}", "Surname": "{}", "Phone": "+905079057424"'.format(nameFirst,nameLast)+ '}')
                    sel=("INSERT INTO [kayitentu].[dbo].[User] (Username, Password, Email, Role, Status, Meta, TCNo) values(%s,%s,%s,%s,%s,%s,%s)")                    
                    value = (nameFull,123,"info@entukbb.com",4,1,metaName2,"12345678910")
                    cursor.execute(sel,value)
                    
                browser.implicitly_wait(5)
                cursor.execute("select ID from [kayitentu].[dbo].[User] where Username LIKE '{}'".format(nameFull))
                patientID=cursor.fetchall()
                patientID=str(patientID[0])  
                patientID= patientID.split(",")  
                patientID = patientID[0].split("(")
                patientID = patientID[1]
        
                cursor.execute("SELECT AppStartDate  FROM [kayitentu].[dbo].[Appointment]")
                saatler = cursor.fetchall()
                saatler2=[]

                outList=0              
                for m in saatler:
                    aha=str(m[0])
                    saatler2.append(aha)

                for t in saatler2:
                    if ("{}".format(hourStart)) in t:
                        outList=1
                many=saatler2.count("{}".format(hourStart))

                cursor.execute("SELECT AppStartDate  FROM [kayitentu].[dbo].[Appointment] WHERE PatientID ={}".format(patientID))
                aka = cursor.fetchall()
                
                inAka=0
                for i in aka:
                    try:
                        if str(hourStart) in (str(i[0])):
                            inAka=1
                    except:
                        inAka=0
                
                if outList == 0:
                    sel2 ="INSERT INTO [kayitentu].[dbo].[Appointment] (Date,DoctorID,Meta,Status,PatientID,AppStartDate,AppEndDate) values (%s,%s,%s,%s,%s,%s,%s)"
                    values2=(date,DoctorID,"{"+"}",1,patientID,hourStart,hourEnd) 
                        
                    cursor.execute(sel2,values2)
                
                elif (outList == 1 and inAka==0):
                    sel2 ="INSERT INTO [kayitentu].[dbo].[Appointment] (Date,DoctorID,Meta,Status,PatientID,AppStartDate,AppEndDate) values (%s,%s,%s,%s,%s,%s,%s)"
                    values2=(date,DoctorID,"{"+"}",1,patientID,hourStart,hourEnd)                           
                    cursor.execute(sel2,values2)            
                print("{}-{}".format(nameFull,patientID))       
                print(hourStart)
                print(hourEnd)
                        
                eventClose=browser.find_element_by_xpath('/html/body/dralia-modal/div/div[2]/div/div/dralia-event-detail-modal/div/div/div[2]/div[1]')               
                browser.implicitly_wait(10)
                eventClose.click()
                browser.implicitly_wait(1)
                n+=1
                mydb.commit()
        except:
            pass
    
args = ["hide_console", ]   
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")
#If you want hide chrome window!
while True:
    try:                  
        browser = webdriver.Chrome(splitmaker(dosyaYolu),service_args=args) 
        browser.maximize_window()       
        openWeb(splitmaker(TUserName),splitmaker(TPassword))
        browser.implicitly_wait(10)
        scan(1)
        browser.implicitly_wait(5)
        browser.close()
        time.sleep(2)       
    except:        
        print("Hata")       
    finally:    
        nowh = datetime.now()
        print("Program Ended at ",nowh)
        time.sleep(3600)    