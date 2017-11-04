import json
import os
import uuid
import psycopg2
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

DEFAULT_USER_ID = "904ca286-98cb-4db5-a1d7-5f0b1f34f87e"

token_url = os.environ.get('TOKEN_URL')
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
audience = os.environ.get('TOKEN_AUDIENCE')

client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

def getToken():
    return oauth.fetch_token(token_url=token_url, client_id=client_id,
        client_secret=client_secret, audience=audience)

# grab initial token
token = getToken()

# TODO: use connection pooling?
def insertPour(query, values): 
    host = os.environ.get('DB_HOST')
    dbname = os.environ.get('DB_DATABASE')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    
    try:
        conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host)
        print "connection successful"
    except:
        print "ERR - unable to connect to database."

    cur = conn.cursor()
    try:
        cur.execute(query, values)

    except Exception as e:
        print "ERR - unable to insert"
        print e

    conn.commit()
    cur.close()
    conn.close()

def emitPour(pourJSON):

    try:
        r = requests.post(
            'http://beer.timfarley.com/topics/pours',
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token.get('access_token')
            },
            data = pourJSON
        )
        print(r.text)
    
    except TokenExpiredError as e:
        getToken()
        emitPour(pourJSON)

def logPour(amount, amount_formatted, beverage, pour_time_start, pour_time_end):

    # Log to DB
    insertPour( 
            """INSERT INTO pours (
                id, 
                amount,
                amount_formatted,
                user_id, 
                beverage_id,
                pour_time_start,
                pour_time_end
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);""",
            (
                str(uuid.uuid4()), 
                amount,
                amount_formatted,
                DEFAULT_USER_ID,
                beverage,
                pour_time_start,
                pour_time_end
            ))

    # Emit to Kafka Stream
    data = {
        'amount': amount,
        'amountFormatted': amount_formatted,
        'userId': DEFAULT_USER_ID,
        'beverageId': beverage,
        'pourTimeStart': pour_time_start.__str__(),
        'pourTimeEnd': pour_time_end.__str__()
    }

    emitPour(json.dumps(data))

    print("Someone poured ", amount_formatted, " of ", beverage, " starting at ",
            pour_time_start, " and ending at ", pour_time_end, ".")
