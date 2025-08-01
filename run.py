
import sys
import os
import mysql.connector

from app import create_app

app = create_app()
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)),debug=True)
