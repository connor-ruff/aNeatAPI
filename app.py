from flask import Flask
from flask_cors import CORS
import pyodbc


app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route('/')
def home():
    try:
        conn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:ruffserver.database.windows.net,1433;Database=funData;Uid=connorruff;Pwd=Charlotte99!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

        cursor = conn.cursor()
        cursor.execute('SELECT * from dbo.YearList2021 where BIRD_ID = 1')

        row = cursor.fetchone()
        output = str(row)
    except Exception as e:
        output = 'FAILURE' + str(e)
    return output


if __name__ == '__main__':
    app.run()