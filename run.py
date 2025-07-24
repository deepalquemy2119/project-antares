
import sys
import os

from app import create_app



app = create_app()
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
if __name__ == "__main__":
    app.run(debug=True)
