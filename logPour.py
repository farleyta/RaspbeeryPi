import os
import uuid
import psycopg2

DEFAULT_USER_ID = "904ca286-98cb-4db5-a1d7-5f0b1f34f87e"

# TODO: use connection pooling?
def insertQuery(query, values): 
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

    
    #rows = cur.fetchall()
    #print rows
    #for row in rows:
    #    print "  ", row
    
    conn.commit()
    cur.close()
    conn.close()

def logPour(amount, beverage, pour_time_start, pour_time_end):

    # TODO: Alter amount data type from TEXT to INT
    insertQuery( 
            """INSERT INTO pours (
                id, 
                amount, 
                user_id, 
                beverage_id,
                pour_time_start,
                pour_time_end
            ) VALUES (%s, %s, %s, %s, %s, %s);""",
            (
                str(uuid.uuid4()), 
                amount,
                DEFAULT_USER_ID,
                beverage,
                pour_time_start,
                pour_time_end
            ))

    print("Someone poured ", amount, " of ", beverage, " starting at ",
            pour_time_start, " and ending at ", pour_time_end, ".")
