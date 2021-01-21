from flask import Flask
from flask_cors import CORS
import pyodbc


app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route('/')
def home():
    conn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=ruffserver.database.windows.net;Database=funData;Uid=connorruff;Pwd=Charlotte99!')

    cursor = conn.cursor()
    cursor.execute('SELECT * from dbo.YearList2021 where BIRD_ID = 1')

    row = cursor.fetchone()
    output = str(row)
    return output


if __name__ == '__main__':
    app.run()