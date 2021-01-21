from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route('/')
def home():
    return 'A Test change'


if __name__ == '__main__':
    app.run()