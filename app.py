from flask import Flask
from flask import request, Response

from flask_sqlalchemy import SQLAlchemy
import shlex
import subprocess
import os
import json
import time
from datetime import date
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

command1 = "python3 /app/python1.py"
command2 = "python3 /app/python2.py"
command3 = "/app/hello"

DB_URI = os.environ.get('DB_URI', '')

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
db = SQLAlchemy(app)

class resultTable(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    requestId = db.Column(db.Integer)
    output1 = db.Column(db.String(64))
    output2 = db.Column(db.String(64))
    output3 = db.Column(db.String(64))
    dateAdded = db.Column(db.DateTime)

def getJson(output):
    jsonArray = []
    dataArray = output.splitlines()
    #print(dataArray)
    headerArray = dataArray[0].replace("#", "").split()
    #print(headerArray)
    for row in range(1, len(dataArray)):
      #print(dataArray[row])
      jsonData = {}
      rowArray = dataArray[row].split()
      #print(rowArray)
      for index, col in enumerate(headerArray):
          jsonData[col] = rowArray[index]
      jsonArray.append(jsonData)
    return jsonArray

def saveDb(requestId, result1, result2, result3):
    row = resultTable(requestId=requestId, output1=result1, output2=result2, output3=result3, date_joined=date.today())
    db.session.add(row)
    db.session.commit()

def run(command):
    try:
        p = subprocess.run(shlex.split(command), capture_output=True, text=True, timeout=10, encoding="utf-8", check=False)
        if p.returncode == 0:
                print("success:{}".format(p))
                print(p.stdout+"\n")
                return p.returncode, p.stdout.rstrip()
        else:
                print("error:{}".format(p))
                print(p.stderr+"\n")
                return p.returncode, p.stderr.rstrip()
    except subprocess.TimeoutExpired as e:
        print("TimeoutExpired")
        return -1, "TimeoutExpired"

@app.route("/ping", methods=['GET'])
def hello():
    return Response("{'return_msg':'pong'}", status=200, mimetype='application/json')

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    try:
        db.session.query("1").from_statement("SELECT 1").all()
        return Response("{'return_msg':'200OK'}", status=200, mimetype='application/json')
    except:
        return Response("{'return_msg':'DB Error'}", status=500, mimetype='application/json')

@app.route('/exec', methods=['GET'])
def execute():
    if 'id' in request.args:
        command1_with_args = command1 + " " + request.args['id']
        ret1 = run(command1_with_args)
        print(ret1)
        if ret1[0] != 0:  
           return Response("{'return_msg':'" + ret1[1] + "'}", status=500, mimetype='application/json')
        else:
           command2_with_args = command2 + " " + ret1[1]
           ret2 = run(command2_with_args)
           print(ret2)
           if ret2[0] != 0:
                return Response("{'return_msg':'" + ret2[1] + "'}", status=500, mimetype='application/json')
           else:
                command3_with_args = command3 + " " + ret2[1] + " FixedArgumentFile.txt"
                ret3 = run(command3_with_args)
                print(ret3)
                if ret3[0] != 0:
                    return Response("{'return_msg':'" + ret3[1] + "'}", status=500, mimetype='application/json')
                else:
                    time.sleep(5)
                    jsonData = json.dumps(getJson(ret3[1]))
                    if len(DB_URI) > 0:
                        saveDb(request.args['id'], ret1[1], ret2[1], jsonData)
                    return Response("{'return_msg':" + jsonData + "}", status=200, mimetype='application/json')
    else:
        return Response("{'return_msg':'Bad request'}", status=400, mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


