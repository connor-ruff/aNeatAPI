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
        cursor.execute('SELECT TOP 1 * from FACT.LifeList')

        row = cursor.fetchone()
        output = str(row)
    except Exception as e:
        output = 'FAILURE' + str(e)

    return output

  

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
        cursor.execute('SELECT * from FACT.LifeList')

        output['Data'] = []

        for row in cursor.fetchall():
            birdObj = {}
            birdObj["Species_Code"] = row[0]
            birdObj["Species"] =row[1]
            birdObj["FirstSightDate"] = str(row[2])
            birdObj["FirstSightCity"] = row[3]
            birdObj["FirstSightState"] = row[4]
            birdObj["FirstSightDetails"] = row[5]
            output['Data'].append(birdObj)

          

    except Exception as e:
        output['Result'] = 'Failure'
        output['Message'] = str(e)

    return json.dumps(output)




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