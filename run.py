import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

sys.path.append(os.path.join(BASE_DIR, 'app'))
sys.path.append(os.path.join(BASE_DIR, 'sync'))
sys.path.append(os.path.join(BASE_DIR, 'ddbb'))



from multiprocessing import Process
from app import create_app

from celery_worker import listen_sync_queue 

app = create_app()

p = Process(target=listen_sync_queue)
p.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
