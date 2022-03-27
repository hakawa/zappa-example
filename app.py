# app.py

from flask import Flask, Response, json, request
import logging
import os
import pymysql.cursors
app = Flask(__name__)
RDS_HOST = 'aaa.bbb.ap-northeast-1.rds.amazonaws.com'
RDS_PORT = 3306
NAME = 'xxx'
PASSWORD = 'aaa'
DB_NAME = 'aaa'

# we need to instantiate the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# here is how we are handling routing with flask:
@app.route('/')
def index():
    connect()
    return "Hello World!", 200

def connect():
    try:
        cursor = pymysql.cursors.DictCursor
        conn = pymysql.connect(RDS_HOST, user=NAME, passwd=PASSWORD, db=DB_NAME, port=RDS_PORT, cursorclass=cursor, connect_timeout=5)
        logger.info("SUCCESS: connection to RDS successful")
        return(conn)
    except Exception as e:
        logger.exception("Database Connection Error")

def build_db():
    conn = connect()
    query = "create table User (ID varchar(255) NOT NULL, firstName varchar(255) NOT NULL, lastName varchar(255) NOT NULL, email varchar(255) NOT NULL, PRIMARY KEY (ID))"
    try:
        with conn.cursor() as cur:
            # just in case it doesn't work the first time let's drop the table if it exists
            cur.execute("drop table if exists User")
            cur.execute(query)
            conn.commit()
    except Exception as e:
        logger.exception(e)
        response = Response(json.dumps({"status": "error", "message": "could not build table"}), 500)
    finally:
        cur.close()
        conn.close()
    response = Response(json.dumps({"status": "success"}), 200)
    return response

@app.route('/build', methods=["GET"])
def build():
    return build_db()

@app.route('/user', methods=["GET", "POST"])
def user():
    resp_dict = {}
    if request.method == "GET":
        resp_dict = {"first_name": "John", "last_name": "doe"}
    if request.method == "POST":
        data = request.form
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        email = data.get("email", "")
        resp_dict = {"first_name": first_name, "last_name": last_name, "email": email}
    response = Response(json.dumps(resp_dict), 200)
    return response

# include this for local dev

if __name__ == '__main__':
    app.run()
