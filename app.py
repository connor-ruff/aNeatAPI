from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route('/')
def home():
    return 'First Output'


if __name__ == '__main__':
    app.run()