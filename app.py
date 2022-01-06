from flask import Flask
from flask_cors import CORS
import pyodbc
import json
from flask import request 
import re
import sys


app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route('/')
def home():
    try:
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:ruffserver.database.windows.net,1433;Database=funData;Uid=connorruff;Pwd=Charlotte99!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

        cursor = conn.cursor()
        cursor.execute('SELECT * from dbo.YearList2021 where BIRD_ID = 1')

        row = cursor.fetchone()
        output = str(row)
    except Exception as e:
        output = 'FAILURE' + str(e)

    return output

@app.route('/list2021')
def list2021():
    output = {}
    try:
        output['Result'] = 'Success'
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:ruffserver.database.windows.net,1433;Database=funData;Uid=connorruff;Pwd=Charlotte99!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        cursor = conn.cursor()
        cursor.execute('SELECT * from dbo.YearList2021')

        output['Data'] = []

        for row in cursor.fetchall():
            birdObj = {}
            birdObj["ID"] = row[0]
            birdObj["Species"] =row[1]
            birdObj["Category"] = row[2]
            birdObj["CategoryAlt"] = row[3]
            birdObj["FirstSightCity"] = row[4]
            birdObj["FirstSightState"] = row[5]
            birdObj["FirstSightDetails"] = row[6]
            birdObj["FirstSightDate"] = str(row[7])
            birdObj["WasLifeBird"] = row[8]
            output['Data'].append(birdObj)

    except Exception as e:
        output['Result'] = 'Failure'
        output['Message'] = str(e)

    return json.dumps(output)     

@app.route('/list2022')
def list2022():
    output = {}
    try:
        output['Result'] = 'Success'
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:ruffserver.database.windows.net,1433;Database=funData;Uid=connorruff;Pwd=Charlotte99!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        cursor = conn.cursor()
        cursor.execute('SELECT * from FACT.YearList2022')

        output['Data'] = []

        for row in cursor.fetchall():
            birdObj = {}
            birdObj["Species_Code"] = row[0]
            birdObj["Species"] =row[1]
            birdObj["FirstSightDate"] = str(row[2])
            birdObj["FirstSightCity"] = row[3]
            birdObj["FirstSightState"] = row[4]
            birdObj["FirstSightDetails"] = row[5]
            birdObj["WasLifeBird"] = row[6]
            output['Data'].append(birdObj)

    except Exception as e:
        output['Result'] = 'Failure'
        output['Message'] = str(e)

    return json.dumps(output)      

@app.route('/lifelist')
def listList():
    output = {}

    try:
        output['Result'] = 'Success'
        

        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:ruffserver.database.windows.net,1433;Database=funData;Uid=connorruff;Pwd=Charlotte99!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        cursor = conn.cursor()
        cursor.execute('SELECT * from dbo.LifeList')

        output['Data'] = []

        for row in cursor.fetchall():
            birdObj = {}
            birdObj["ID"] = row[0]
            birdObj['Species'] = row[1]
            birdObj['Category'] = row[2]
            birdObj['CategoryAlt'] = row[3]
            birdObj['FirstSightCity'] = row[4]
            birdObj['FirstSightState'] = row[5]
            birdObj['FirstSightDetails'] = row[6]
            birdObj['FirstSightDate'] = str(row[7])

            output['Data'].append(birdObj)

    except Exception as e:
        output['Result'] = 'Failure'
        output['Message'] = str(e)

    return json.dumps(output)

@app.route('/lifelistobj')
def lifeListObj():

    output = {}

    try:
        output['Result'] = 'Success'
        

        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:ruffserver.database.windows.net,1433;Database=funData;Uid=connorruff;Pwd=Charlotte99!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        cursor = conn.cursor()
        cursor.execute('SELECT * from dbo.LifeList')

        output['Data'] = {}

        for row in cursor.fetchall():
            birdObj = {}
            birdObj['Species'] = row[1]
            birdObj['Category'] = row[2]
            birdObj['CategoryAlt'] = row[3]
            birdObj['FirstSightCity'] = row[4]
            birdObj['FirstSightState'] = row[5]
            birdObj['FirstSightDetails'] = row[6]
            birdObj['FirstSightDate'] = str(row[7])

            output['Data'][row[0]] = birdObj

    except Exception as e:
        output['Result'] = 'Failure'
        output['Message'] = str(e)

    return json.dumps(output)

@app.route('/getbird', methods=['POST'])
def getbird():
    # Get the user input
    output = {}
  

    try:
        output['Result'] = 'Success'
        output['Data'] = {}
        userData = request.form
        birdToFind = userData['bird']
        # Search Databases
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:ruffserver.database.windows.net,1433;Database=funData;Uid=connorruff;Pwd=Charlotte99!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * from dbo.LifeList WHERE species = ''?'' ', birdToFind)
        lifeListRet = cursor.fetchall()
        output['Data']['Life'] = {}
        if (len(lifeListRet) > 0):
            output['Data']['Life']['Found'] = 'True'
            output['Data']['Life']['Entry'] = {}
            birdObj = {}
            birdObj['Species'] = lifeListRet[1]
            birdObj['Category'] = lifeListRet[2]
            birdObj['CategoryAlt'] = lifeListRet[3]
            birdObj['FirstSightCity'] = lifeListRet[4]
            birdObj['FirstSightState'] = lifeListRet[5]
            birdObj['FirstSightDetails'] = lifeListRet[6]
            birdObj['FirstSightDate'] = str(lifeListRet[7])

        else:
            output['Data']['Life']['Found'] = 'False'

        cursor.execute(f'SELECT * from dbo.YearList2021 WHERE species = ''?'' ', birdToFind)
        lifeListRet = cursor.fetchall()
        output['Data']['Year'] = {}
        if (len(lifeListRet) > 0):
            output['Data']['Year']['Found'] = 'True'
            output['Data']['Year']['Entry'] = str(lifeListRet[0])
        else:
            output['Data']['Year']['Found'] = 'False'


    except Exception as e:
        output['Result'] = 'Failure'
        output['Message'] = str(e)
        output['Usage'] = usageString


    return json.dumps(output)

    # return an object 

@app.route('/addToLife', methods=['POST'])
def addToLife():

    usageString = '''
    Data Sent Via POST Should be A JSON Structure With the Following Form:
    {
        'birds': [{'value' : birdCode, 'label': birdSpecies}....],
        'date' : <Date of Sight>,
        'city' : <City of Sight>,
        'state' : <state of sight>,
        'details' : <details of sight> 
    }
    '''
    output = {}
    output['Message'] = {'AddedToLife' : [], 'AlreadyInLife': []}
    output['Usage'] = usageString
    

    try:
        # Establish Connection to SQL Server
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:ruffserver.database.windows.net,1433;Database=funData;Uid=connorruff;Pwd=Charlotte99!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        cursor = conn.cursor()

        speciesToAdd = []

        # grab user data and loop through
        userData = request.json 
        
        for bird in userData['birds']:
            # search for species in list already
            cursor.execute(f'SELECT * FROM FACT.LifeList WHERE Species_Code = ?', bird['value'])
            listRet = cursor.fetchall()
            
            # if species in table already
            if len(listRet) != 0:
                output['Message']['AlreadyInLife'].append(bird['label'])
            # if species is not in table already
            else:
                output['Message']['AddedToLife'].append(bird['label'])
                # Add To Object Containing the Entries
                speciesToAdd.append([bird['value'], bird['label'], userData['date'], userData['city'], userData['state'], userData['details']])
               
        # Insert All Species That Were Not Already In Life List 
        if len(speciesToAdd) > 0:
            query_string = 'INSERT INTO FACT.LifeList (Species_Code, Species, First_Sight_Date, First_Sight_City, First_Sight_State, First_Sight_Details) VALUES (?, ?, ?, ?, ?, ?)'
            cursor.executemany(query_string, speciesToAdd)
            conn.commit()    

        output['Result'] = 'Success'
      
                

    except Exception as e:
        output['Result'] = 'Failure'
        output['Message'] = str(e)
        

    return json.dumps(output)

@app.route('/addToYear2022', methods=['POST'])
def addToYear2022():
    usageString = '''
    Data Sent Via POST Should be A JSON Structure With the Following Form:
    {
        'birds': [{'value' : birdCode, 'label': birdSpecies}....],
        'date' : <Date of Sight>,
        'city' : <City of Sight>,
        'state' : <state of sight>,
        'details' : <details of sight> 
    }
    '''
    output = {}
    output['Message'] = {'AddedToYear' : [], 'AlreadyInYear': []}
    output['Usage'] = usageString
    

    try:
        # Establish Connection to SQL Server
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:ruffserver.database.windows.net,1433;Database=funData;Uid=connorruff;Pwd=Charlotte99!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        cursor = conn.cursor()

        speciesToAdd = []

        # grab user data and loop through
        userData = request.json 
        print(userData)
        for bird in userData['birds']:
            # search for species in list already
            cursor.execute(f'SELECT * FROM FACT.YearList2022 WHERE Species_Code = ?', bird['value'])
            listRet = cursor.fetchall()
            
            
            # if species in table already
            if len(listRet) != 0:
                output['Message']['AlreadyInYear'].append(bird['label'])
            # if species is not in table already
            else:
                output['Message']['AddedToYear'].append(bird['label'])
                # Add To Object Containing the Entries
                cursor.execute('SELECT SPECIES FROM FACT.LifeList WHERE Species_Code = ?', bird['value'])
                if len(cursor.fetchall()) == 0:
                    WasLifeBird = 1
                else:
                    WasLifeBird = 0
               
                speciesToAdd.append([bird['value'], bird['label'], userData['date'], userData['city'], userData['state'], userData['details'], WasLifeBird])

       
        # Insert All Species That Were Not Already In Life List 
        if len(speciesToAdd) > 0:
            query_string = 'INSERT INTO FACT.YearList2022 (Species_Code, Species, First_Sight_Date, First_Sight_City, First_Sight_State, First_Sight_Details, WasLifeBird) VALUES (?, ?, ?, ?, ?, ?, ?)'
            cursor.executemany(query_string, speciesToAdd)
            conn.commit()    

        output['Result'] = 'Success'
      
                

    except Exception as e:
        output['Result'] = 'Failure'
        output['Message'] = str(e)
        

    return json.dumps(output)

@app.route('/getAllBirds', methods=['GET'])
def getAllBirds():
    output = {}
    try:
        output['Result'] = 'Success'
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:ruffserver.database.windows.net,1433;Database=funData;Uid=connorruff;Pwd=Charlotte99!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        cursor = conn.cursor()
        cursor.execute(f'SELECT Species_Code, Species FROM REF.TAXONOMY')
        jsonResp = cursor.fetchall()
        birdObj = []
        key = 0
        for entry in jsonResp:
          #  birdObj.append({'key': key, 'value': entry[0], 'text': entry[1]})
            birdObj.append({'value': entry[0], 'label': entry[1]})
            key+=1
   
        output['Message'] = birdObj

    except Exception as e:
        output['Result'] = 'Failure'
     #   output['Message'] = [{'key': 0, 'value': 'null', 'text': 'Could Not Load Bird'}]
        output['Message'] = [{'value': entry[0], 'label': entry[1]}]

    return json.dumps(output)


if __name__ == '__main__':
    app.run()