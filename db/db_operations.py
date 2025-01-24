from db.db_connection import DBConnection  #database connection 
from adb.app_usage_utils import get_app_usage # apps
from adb.battery_utils import get_battery_status #battery




#Class to establish  a connection with database
def get_connection():
    db = DBConnection(user="hr", password="hr", dsn="localhost:1521/XEPDB1")
    return db.get_connection()



def insert_raw_data():
    """
    Catches app and battery usage data
    """
    connection = None
    try:
        app_usage_data = get_app_usage()  # app_usage
        battery_data = get_battery_status()  # battery

        connection = get_connection()
        cursor = connection.cursor()

        # 3. Insert data into `landing_raw_app_usage`
        query_app_usage = """
        INSERT INTO landing_raw_app_usage (raw_data, ingestion_time)
        VALUES (:raw_data, SYSDATE)
        """
        cursor.execute(query_app_usage, {"raw_data": str(app_usage_data) })

        # 4. Insert data into `landing_battery_status`
        query_battery_status = """
        INSERT INTO landing_raw_battery_status (raw_data, ingestion_time)
        VALUES (:raw_data, SYSDATE)
        """
        cursor.execute(query_battery_status, {"raw_data": str(battery_data)})

        # 5. Transactions commit
        connection.commit()

        print("Data inserted into raw layer - sucess")
    except Exception as e:
        print(f"Error in insert into raw layer: {e}")
    finally:
        if connection:
            connection.close()






