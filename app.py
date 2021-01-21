from flask import Flask
from flask_cors import CORS
import pyodbc
import json
import re


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

@app.route('/lifelist')
def lifeList():

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


if __name__ == '__main__':
    app.run()