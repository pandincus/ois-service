from flask import Flask
from flask_apscheduler import APScheduler
from apscheduler.util import obj_to_ref

from .connection import Connection

app = Flask(__name__)
connection = Connection()

@app.route("/")
def get_status():
    status = connection.getData()

    s = ""

    for key, request in status.items():
        s += "{}:{}<br />".format(request.fieldName, request.value)

    return s

class DataJobConfig(object):
    JOBS = [
        {
            "id": "dataJob",
            "func": "ois.data_job:run",
            "kwargs": { "connection": connection },
            "trigger": "interval",
            "seconds": 2,
            "timezone": "America/Los_Angeles"
        }
    ]

    SCHEDULER_API_ENABLED = True

app.config.from_object(DataJobConfig())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

