

from flask import Flask

# Initialize the Flask app
app = Flask(__name__)

# Import your routes
from routes import *

if __name__ == '__main__':
    app.run(debug=True)


