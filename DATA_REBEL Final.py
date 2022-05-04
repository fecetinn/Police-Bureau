# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 19:44:32 2021

@author: Fatih Çetin
"""
# Note: You should install PySimpleGUI first by entering  pip install pysimplegui  in the console

import sqlite3
import PySimpleGUI as sg
from datetime import datetime

con = sqlite3.connect('Example.db')
cur = con.cursor()

login_user_id = -1
login_user_name = -1
login_user_type = -1
crimescenes = []

def window_login():
    
    layout = [[sg.Text('Welcome to the Detective Bureau Management System. Please enter your information.')],
              [sg.Text('SSN:',size=(10,1)), sg.Input(size=(10,1), key='id')],
              [sg.Text('Password:',size=(10,1)), sg.Input(size=(10,1), key='password')],
              [sg.Button('Login')]]

    return sg.Window('Login Window', layout)


def window_fieldofficer():
    
    layout = [[sg.Text('Welcome ' + login_user_name +'!')],
              [sg.Button('Crime Scenes')],
              [sg.Button('Equipments')],
              [sg.Button('Logout')]]

    return sg.Window('Field Officer Window', layout)

def window_Investigator():
    
    layout = [[sg.Text('Welcome ' + login_user_name +'!')],
              [sg.Button('All Crime Scenes')],
              [sg.Button('All Field Officers')],
              [sg.Button('Suspects')],
              [sg.Button('Logout')]]

    return sg.Window('Investigator Window', layout)

def window_Prosecutor():
    
    layout = [[sg.Text('Welcome ' + login_user_name +'!')],
              [sg.Button('Indictments')],
              [sg.Button('Create Indictment')],
              [sg.Button('Executions')],
              [sg.Button('Logout')]]

    return sg.Window('Prosecutor Window', layout)

# button functions
def button_login(values):
    
    global login_user_id
    global login_user_name
    global login_user_type
    global window
    
    uid = values['id']
    upass = values['password']
    if uid == '':
        sg.popup('SSN cannot be empty')
    elif upass == '':
        sg.popup('Password cannot be empty')
    else:
        
        cur.execute('SELECT SSN, Name FROM Field_Officers WHERE SSN = ? AND Password = ? Union SELECT SSN, Name FROM Investigators WHERE SSN = ? AND Password = ? Union SELECT SSN, Name FROM Prosecutors WHERE SSN = ? AND Password = ?', (uid,upass,uid,upass,uid,upass))
        row = cur.fetchone()
        
        if row is None:
            sg.popup('SSN, Title or password is wrong!')
        else:
            
            login_user_id = row[0]
            
            
            login_user_name = row[1]
            
            
            cur.execute('SELECT SSN FROM Field_Officers WHERE SSN = ?', (uid,))
            row_student = cur.fetchone()
            
            if row_student is None:
                
                cur.execute('SELECT SSN FROM Investigators WHERE SSN = ?', (uid,))
                row_teacher = cur.fetchone()
                if row_teacher is None:
                    
                    login_user_type = 'Prosecutors'
                    sg.popup('Welcome, ' + login_user_name + ' (Prosecutor)')
                    window.close()
                    window = window_Prosecutor()
                else:
                    
                    login_user_type = 'Investigators'
                    sg.popup('Welcome, ' + login_user_name + ' (Investigator)')
                    window.close()
                    window = window_Investigator()
            else:
                
                    login_user_type = 'Field_Officers'
                    sg.popup('Welcome, ' + login_user_name + ' (Field Officer)')
                    window.close()
                    window = window_fieldofficer()
   
def window_crimescenes():
    
    global crimescenes
    
    
    crimescenes = []
    for row in cur.execute('''SELECT SceneNo, Date
                              FROM Assign
                              WHERE OSSN = ?''', (login_user_id,)):
        crimescenes.append(row)
    
    layout = [[sg.Text('Your Crime Scenes:'), sg.Combo(crimescenes, size=(25,7), key='crimescene'), sg.Button('Evidences')],
              [sg.Button('New Evidence')],
              [sg.Button('Return To Main')]]
    
    return sg.Window('Crime Scenes', layout)  


def window_allcrimescenes():
    
    global allcrimescenes
    
    allcrimescenes = []
    
    for row in cur.execute('''SELECT *
                              FROM Crime_Scene
                              '''):
        allcrimescenes.append(row)
    
    layout = [[sg.Text('All Crime Scenes:')],
              [sg.Listbox(allcrimescenes, size=(50,10), key='allcrimescenes')],
              [sg.Button('Return To Main')]]

    return sg.Window('All Crime Scenes', layout)



def window_allfieldofficers():
    
    allfieldofficers = []
    
    
    for row in cur.execute('''SELECT *
                              FROM Field_Officers
                              '''):
        allfieldofficers.append(row)
    
    layout = [[sg.Text('All Field Officers:')],
              [sg.Listbox(allfieldofficers, size=(55,10), key='allfieldofficers'),  sg.Button('Assign')],
              [sg.Button('List By Location')],
              [sg.Button('Return To Main')]]
    
    return sg.Window('All Field Officers', layout)



def window_listedallfieldofficers():
    
    global locationofallfieldofficers
    
    listedallfieldofficers = []
    for row in cur.execute('''SELECT SSN, Name, Surname, Location
                              FROM Field_Officers
                              ORDER BY Location'''):
        listedallfieldofficers.append(row)
    
    
    locationofallfieldofficers = []
    for row in cur.execute('''SELECT distinct Location
                              FROM Field_Officers
                              ORDER BY Location'''):
        locationofallfieldofficers.append(row)
    
    layout = [[sg.Text('Listed all Field Officers accoeding to Location order:')],
              [sg.Listbox(listedallfieldofficers, size=(50,10), key='listedallfieldofficers')],
              [sg.Combo(locationofallfieldofficers, size=(50,10), key='thelocationofallfieldofficers'), sg.Button('Filter Field Officers')],
              [sg.Button('All Field Officers'), sg.Button('Return To Main')]]

    return sg.Window('List By Location', layout)

def window_filteredallfieldofficers():
    
    theloc = values['thelocationofallfieldofficers']

    locatiofilteredofallfieldofficers = []
    for row in cur.execute('''SELECT *
                              FROM Field_Officers
                              WHERE Location = ?''', (theloc[0],)):
        locatiofilteredofallfieldofficers.append(row)
        
    

    layout = [[sg.Text('Filtered Field Officers belongs to Location of ' + str(theloc[0]) + ':')],
              [sg.Listbox(locatiofilteredofallfieldofficers, size=(60,10), key='locatiofilteredofallfieldofficers')],
              [sg.Button('List By Location'), sg.Button('All Field Officers'),sg.Button('Return To Main')]]

    return sg.Window('Filter Field Officers', layout)


def window_newassign():
    
    #All Assignment List
    newassign = []
    for row in cur.execute('''SELECT *
                              FROM Assign
                              '''):
        newassign.append(row)
    
    #Field Officers
    allfieldofficers = []
    for row in cur.execute('''SELECT SSN
                              FROM Field_Officers
                              '''):
        allfieldofficers.append(row)
    
    
    crimescene = []
    for row in cur.execute('''SELECT SceneNo
                              FROM Crime_Scene
                              '''):
        crimescene.append(row)
        
    
    layout = [[sg.Text('Already Assigned Crime Scenes to Officers:')],
              [sg.Listbox(newassign, size=(50,10), key='newassign')],
              [sg.Text('Crime Scenes:')],
              [sg.Combo(crimescene, size=(50,10), key='crimescene')],
              [sg.Text('Field Officers:')],
              [sg.Combo(allfieldofficers, size=(50,10), key='fieldofficer')],
              [sg.Button('New Assign')], 
              [sg.Button('All Field Officers'), sg.Button('Return To Main')]]

    return sg.Window('Assign', layout)


def button_assign(values):
    
    OfficerSSN = values['fieldofficer']
    Scene_no = values['crimescene']
    date = datetime.today().strftime('%Y-%m-%d')
    
    
    if Scene_no == '':
        sg.popup('Choose a Crime Scene!')
    elif OfficerSSN == '':
        sg.popup('Choose an Officer!')
            
    
    else: 
        theOfficerSSN = OfficerSSN[0]
        theScene_no = Scene_no[0]
            
        cur.execute('INSERT INTO Assign VALUES (?,?,?,?)',(theOfficerSSN,login_user_id,theScene_no,date))
                    
        sg.popup('Officer successfully assigned')
                    
                    
        window.Element('fieldofficer').Update(value='')
        window.Element('crimescene').Update(value='')
        

def window_evidences():
    
    
    evidences = []
    thecrime = values['crimescene']
    
    if thecrime == '':
        layout = [[sg.Text('Choose a Crime Scene!',size=(40,1))],
                  [sg.Button('Crime Scenes'),sg.Button('Return To Main')]]
        
    else:
        thecrime = thecrime[0]
    
    
        for row in cur.execute('''SELECT *
                                  FROM Evidence
                                  WHERE EvidenceNo in (SELECT EvidenceNO FROM InCrimeScene Where SceneNO = ? )''', (thecrime,)):
                                      evidences.append(row)
        
        layout = [[sg.Text('Evidences that are found in ' + str(thecrime) + ' enumareted Crime Scene:')],
                  [sg.Listbox(evidences, size=(40,10), key='evidence')],
                  [sg.Button('Crime Scenes'),sg.Button('Return To Main')]]
    
    return sg.Window('Evidence Window', layout)


def window_new_evidence():
    
    thecrime = values['crimescene']
    
    if thecrime == '':
        layout = [[sg.Text('Choose a Crime Scene!',size=(40,1))],
                  [sg.Button('Crime Scenes'),sg.Button('Return To Main')]]
        
    else:
        thecrime = [thecrime[0]]
        
    
        layout = [[sg.Text('The Crime Scene:',size=(20,1)), sg.Combo(thecrime, size=(10,10), key='thecrime')],
              [sg.Text('Address:',size=(20,1)), sg.Input(key='address',size=(10,1))],
              [sg.Text('Description:',size=(20,1)), sg.Input(key='description',size=(10,1))],
              [sg.Text('Object Name:',size=(20,1)), sg.Input(key='object name',size=(10,1))],
              [sg.Button('Insert')],
              [sg.Button('Crime Scenes'), sg.Button('Return To Main')]]

    return sg.Window('New Evidence Window', layout)      

def button_insert(values):
    
    the_crime = values['thecrime']
    adres = values['address']
    desc = values['description']
    obnname = values['object name']
    date = datetime.today().strftime('%Y-%m-%d')
    
    if adres == '':
        sg.popup('Address cannot be empty!')
    elif desc == '':
        sg.popup('Description cannot be empty!')
    elif obnname == '':
        sg.popup('Object Name cannot be empty!')
           
    else:
        cur.execute('SELECT MAX(EvidenceNo) FROM Evidence')
        row = cur.fetchone()
        if row is None:
      
            new_id = 1
        else:
            new_id = row[0] + 1

            
        cur.execute('INSERT INTO Evidence VALUES (?,?,?,?,?)',(new_id,adres,desc,obnname,date))
        cur.execute('INSERT INTO Find VALUES (?,?)',(login_user_id,new_id))
        cur.execute('INSERT INTO InCrimeScene VALUES (?,?)',(new_id,the_crime))
        sg.popup('Successfully inserted with Evidence No: ' + str(new_id) )
            
         
        window.Element('address').Update(value='')
        window.Element('description').Update(value='')
        window.Element('object name').Update(value='')


def window_suspects():
    
    global suspects
    
    suspects = []
    for row in cur.execute('''SELECT *
                              FROM Suspect
                              '''):
        suspects.append(row)

    layout = [[sg.Text('All Suspects at the below:')], 
              [sg.Text('Choose a Suspect:'), sg.Combo(suspects, size=(40,10), key='suspect'), sg.Button('Reports')],
              [sg.Button('New Suspect')],
              [sg.Button('Return To Main')]]

    return sg.Window('Suspects Window', layout)

def window_reports():
    
    
    reports = []

    thesuspect = values['suspect']
    for row in cur.execute('''SELECT *
                              FROM Report
                              WHERE PhoneNo = ? ''', (thesuspect[0],)):
        reports.append(row)
        
    thesuspectnmbr = []
    for row in cur.execute('''SELECT *
                              FROM Suspect
                              WHERE PhoneNo = ? ''', (thesuspect[0],)):
        thesuspectnmbr.append(row)

    layout = [[sg.Text('Interrogation Reports of Suspect named ' + str(thesuspect[4] + ' ' + str(thesuspect[3]) + ' :' ))],
              [sg.Listbox(reports, size=(80,5), key='reports')],
              [sg.Text('The Suspect: ',size=(20,1))],
              [sg.Combo(thesuspectnmbr, size=(50,5), key='thesuspectnmbr')],
              [sg.Text('Report Content:',size=(15,1)), sg.Input(key='reportcontent',size=(35,2))],
              [sg.Button('Insert Report')], 
              [sg.Button('Suspects') ,sg.Button('Return To Main')]]
    
    return sg.Window('Reports', layout)

def button_insertreport(values):
    
    thephonenumber = values['thesuspectnmbr']
    report_content = values['reportcontent']

    if report_content == '':
        sg.popup('Report Content cannot be empty!')
            
    else:
        cur.execute('SELECT MAX(ReportNo) FROM Report')
        row = cur.fetchone()
        if row is None:
            new_id = 1
        else:
            new_id = row[0] + 1
           
        cur.execute('INSERT INTO Report VALUES (?,?,?,?)',(new_id,thephonenumber[0],login_user_id,report_content))
        sg.popup('Successfully inserted with Report No: ' + str(new_id))
            
        window.Element('reportcontent').Update(value= '')
        


def window_newsuspect():
    
    layout = [[sg.Text('Phone Number:',size=(15,1)), sg.Input(key='phnumber',size=(10,1))],
              [sg.Text('Name:',size=(15,1)), sg.Input(key='name',size=(10,1))],
              [sg.Text('Surname:',size=(15,1)), sg.Input(key='surname',size=(10,1))],
              [sg.Text('Gender:',size=(15,1)), sg.Input(key='gender',size=(10,1))],
              [sg.Text('Age:',size=(15,1)), sg.Input(key='age',size=(10,1))],
              [sg.Button('Insert Suspect')],
              [sg.Button('Suspects'),sg.Button('Return To Main')]]

    return sg.Window('New Suspect Window', layout)

def button_insertsuspect(values):
    
    phone_number = values['phnumber']
    the_name = values['name']
    the_surname = values['surname']
    the_gender = values['gender']
    the_age = values['age']

    
    if phone_number == '':
        sg.popup('Phone Number cannot be empty!')
    elif the_name == '':
        sg.popup('Name cannot be empty!')
    elif the_surname == '':
        sg.popup('Surname Name cannot be empty!')
    elif the_gender == '':
        sg.popup('Gender cannot be empty!')
    elif the_age == '':
        sg.popup('Age Name cannot be empty!')
           
    else:
        
            
        cur.execute('INSERT INTO Suspect VALUES (?,?,?,?,?)',(phone_number,the_gender,the_age,the_surname,the_name))
            
        sg.popup('Suspect ' + str(the_name) + ' ' + str(the_surname) + ' successfully inserted with Phone Number: ' + str(phone_number) )
            
            
        window.Element('phnumber').Update(value='')
        window.Element('name').Update(value='')
        window.Element('surname').Update(value='')
        window.Element('gender').Update(value='')
        window.Element('age').Update(value='')



def window_equipments():
    
    equipments = []
    
    for row in cur.execute('''SELECT *
                              FROM HaveEquipment
                              WHERE SSN = ?''', (login_user_id,)):
        equipments.append(row)
    
    layout = [[sg.Text('Equipments of: ' + str(login_user_name) )],
              [sg.Listbox(equipments, size=(40,10), key='equipments')],
              [sg.Button('New Equipment'), sg.Button('Return To Main')]]

    return sg.Window('Equipments Window', layout)

def window_new_equipment():
    
    layout = [[sg.Text('Equipment Name:',size=(20,1)), sg.Input(key='equipment name',size=(10,1))],
              [sg.Text('Weight:',size=(20,1)), sg.Input(key='weight',size=(10,1))],
              [sg.Button('Insert Equipment')], 
              [sg.Button('Equipments'), sg.Button('Return To Main')]]

    return sg.Window('New Equipment Window', layout)      

def button_inserteq(values):
    
    eqname = values['equipment name']
    weight = values['weight']
    date = datetime.today().strftime('%Y-%m-%d')
    
    if eqname == '':
        sg.popup('Equipment Name cannot be empty!')
    elif weight == '':
        sg.popup('Equipments are not weightless!')
    else:

        cur.execute('INSERT INTO HaveEquipment VALUES (?,?,?,?)',(eqname,login_user_id,weight,date))
            
        sg.popup('The Equipment successfully inserted' )
            
            
        window.Element('equipment name').Update(value='')
        window.Element('weight').Update(value='')

def window_indictments():
    
    
    
    indictments = []
    
    for row in cur.execute('''SELECT *
                              FROM Indictment
                              WHERE SSN = ?''', (login_user_id,)):
        indictments.append(row)
    
    Status = ['OnGoing', 'Guilty', 'Innocent']
    
    layout = [[sg.Text('Indictments of:'), sg.Text(login_user_name)],
              [sg.Listbox(indictments, size=(80,10), key='indictments')],
              [sg.Text('Choose an Indictment from above and update an Indictment Status:')],
              [sg.Combo(Status, size=(80,10), key='status'), sg.Button('Update')],
              [sg.Button('Return To Main')]]

    return sg.Window('Indictments', layout)

def button_update(values):
    
    Indictment = values['indictments']
    Status = values['status']
    
    
    if Status == '':
        sg.popup('Choose a Status!')
            
    
    else: 
            
            
        cur.execute('UPDATE Indictment SET Status = ? WHERE FileNo = ?',(Status,Indictment[0][0]))
        
        sg.popup('Indictment succesfully updated!')
                    
                    
        window.Element('status').Update(value= '')

def window_createindictment():
    
    global createindictment
    
    createindictment = []
    
    for row in cur.execute('''SELECT *
                              FROM Indictment
                               '''):
        createindictment.append(row)
    
    suspects = []
    for row in cur.execute('''SELECT *
                              FROM Suspect
                              '''):
        suspects.append(row)
    
    Status = ['OnGoing', 'Guilty', 'Innocent']
    
    layout = [[sg.Text('Existing Indictments:')],
              [sg.Listbox(createindictment, size=(70,10), key='createindictment')],
              [sg.Text('',size=(25,2)), sg.Text('Create an Indictment:',size=(20,2))],
              [sg.Text('Choose a Suspect:',size=(20,1))],
              [sg.Combo(suspects, size=(30,10), key='suspects')],
              [sg.Text('Choose a Status:',size=(20,1))],
              [sg.Combo(Status, size=(30,10), key='status')],
              [sg.Text('Crime Description:',size=(20,1))], 
              [sg.Input(key='crimedesc',size=(30,2))],
              [sg.Text('Punishment Description:',size=(20,1))], 
              [sg.Input(key='punismentdesc',size=(30,2))],
              [sg.Button('Insert Indictment'), sg.Button('Return To Main')]]

    return sg.Window('Create Indictment', layout)

def button_insertindictment(values):
    
    Thesuspect = values['suspects']
    Status = values['status']
    CrimeDescription = values['crimedesc']
    PunishmentDescription = values['punismentdesc']
    
    if Thesuspect == '':
        sg.popup('Choose a suspect!')
    elif Status == '':
        sg.popup('Status cannot be empty!')
    elif CrimeDescription == '':
        sg.popup('Crime Description cannot be empty!')
    elif PunishmentDescription == '':
        sg.popup('Punishment Description cannot be empty!')
            
    else:
        The_suspect = Thesuspect[0]
        
        cur.execute('SELECT MAX(FileNo) FROM Indictment')
        row = cur.fetchone()
        if row is None:
        
            new_id = 1
        else:
            new_id = row[0] + 1

            
        cur.execute('INSERT INTO Indictment VALUES (?,?,?,?,?,?)',(new_id,The_suspect,login_user_id,Status,CrimeDescription,PunishmentDescription))
            
        
        sg.popup('Successfully inserted with File No: ' + str(new_id) )
            
            
        window.Element('suspects').Update(value='')
        window.Element('status').Update(value='')
        window.Element('crimedesc').Update(value='')
        window.Element('punismentdesc').Update(value='')

def window_executions():
    
    global thecrimescenes
    
    thecrimescenes = []
    for row in cur.execute('''SELECT *
                              FROM Crime_Scene
                              '''):
        thecrimescenes.append(row)
    
    layout = [[sg.Text('Choose Crime Scene:')],
              [sg.Combo(thecrimescenes, size=(40,10), key='thecrimescenes')],
              [sg.Button('List Associated Evidences')],
              [sg.Button('Relate Evidence')],
              [sg.Button('Return To Main')]]

    return sg.Window('Executions Window', layout)

def window_listofevidences():
    
    evidences = []
    thecrimescenes = values['thecrimescenes']
    for row in cur.execute('''SELECT *
                              FROM Evidence
                              WHERE EvidenceNo in (SELECT EvidenceNo FROM InCrimeScene Where SceneNO = ? )''', (str(thecrimescenes[0]),)):
        evidences.append(row)
        

    layout = [[sg.Text('List of Evidences belong to: ' + str(thecrimescenes[0]) + ' enumerated Crime Scene')],
              [sg.Listbox(evidences, size=(60,10), key='evidences')],
              [sg.Button('Executions'), sg.Button('Return To Main')]]

    return sg.Window('List of Evidence Window', layout)

def window_relateevidence():
    
    
    evidence = []
    for row in cur.execute('''SELECT *
                              FROM Evidence
                              '''):
        evidence.append(row)
    
    indictment = []
    for row in cur.execute('''SELECT *
                              FROM Indictment
                              '''):
        indictment.append(row)
        
    relatedto = []
    for row in cur.execute('''SELECT *
                              FROM RelatedTo
                              '''):
        relatedto.append(row)
        
    layout = [[sg.Text('Indictment that are already Related with Evidence:')],
              [sg.Listbox(relatedto, size=(50,10), key='relatedto')],
              [sg.Text('Already Relate an Evidence with Indictment:')],
              [sg.Text('Choose a piece of Evidence:')],
              [sg.Combo(evidence, size=(50,10), key='evidence')],
              [sg.Text('Choose an Indictment:')],
              [sg.Combo(indictment, size=(50,10), key='indictment')],
              [sg.Text('Role:',size=(10,1))], 
              [sg.Input(key='role',size=(50,2))],
              [sg.Button('Relate')],
              [sg.Button('Executions'), sg.Button('Return To Main')]]

    return sg.Window('Relate Evidence', layout)

def button_relate(values):
    
    Evidence = values['evidence']
    Indictment = values['indictment']
    Therole = values['role']
    
    
    if Evidence == '':
        sg.popup('Choose an Evidence!')
    elif Indictment == '':
        sg.popup('Choose an Indictment!')
    elif Therole == '':
        sg.popup('Role cannot be empty!')
            
    
    else: 
            
            
        cur.execute('INSERT INTO RelatedTo VALUES (?,?,?)',(Indictment[0],Evidence[0],Therole))
                    
        sg.popup('Evidence succesfully related!')
                    
                    
        window.Element('evidence').Update(value='')
        window.Element('indictment').Update(value='')
        window.Element('role').Update(value='')



window = window_login()

while True:
    event, values = window.read()
    if event == 'Login':
        button_login(values)
        
    elif event == 'Crime Scenes':
        window.close()
        window = window_crimescenes()
        
    elif event == 'All Crime Scenes':
        window.close()
        window = window_allcrimescenes()
        
    elif event == 'All Field Officers':
        window.close()
        window = window_allfieldofficers()
        
    elif event == 'List By Location':
        window.close()
        window = window_listedallfieldofficers()
    
    elif event == 'Filter Field Officers':
        window.close()
        window = window_filteredallfieldofficers()
     
    elif event == 'Assign':
        window.close()
        window = window_newassign()
        
    elif event == 'Evidences':
        window.close()
        window = window_evidences()
        
    elif event == 'Suspects':
        window.close()
        window = window_suspects()
        
    elif event == 'New Suspect':
        window.close()
        window = window_newsuspect()
        
    elif event == 'New Evidence':
        window.close()
        window = window_new_evidence()
        
    elif event == 'Equipments':
        window.close()
        window = window_equipments()
        
    elif event == 'New Equipment':
        window.close()
        window = window_new_equipment()
        
    elif event == 'Reports':
        window.close()
        window = window_reports()
        
    elif event == 'Indictments':
        window.close()
        window = window_indictments()
        
    elif event == 'Create Indictment':
        window.close()
        window = window_createindictment()
        
    elif event == 'Executions':
        window.close()
        window = window_executions()
        
    elif event == 'List Associated Evidences':
        window.close()
        window = window_listofevidences()
        
    elif event == 'Relate Evidence':
        window.close()
        window = window_relateevidence()
        
    elif event == 'Insert Equipment':
        button_inserteq(values)
        
    elif event == 'Insert':
        button_insert(values)
        
    elif event == 'Insert Suspect':
        button_insertsuspect(values)
        
    elif event == 'New Assign':
        button_assign(values)
    
    elif event == 'Insert Report':
        button_insertreport(values)
    
    elif event == 'Insert Indictment':
        button_insertindictment(values)
    
    elif event == 'Relate':
        button_relate(values)
        
    elif event == 'Update':
        button_update(values)
        
    elif event == 'Return To Main':
        if login_user_type == 'Prosecutors':
            window.close()
            window = window_Prosecutor()
        elif login_user_type == 'Field_Officers':
            window.close()
            window = window_fieldofficer()
        elif login_user_type == 'Investigators':
            window.close()
            window = window_Investigator()
        else:
            
            window.close()
            window = window_login()
    elif event == 'Logout':
      
        login_user_id = -1
        login_user_name = -1
        login_user_type = -1
        window.close()
        window = window_login()
    elif event == sg.WIN_CLOSED:
        break

window.close()
#con.commit()
con.close()