from db.db_connection import DBConnection
from processing.battery_processing import parse_battery_status
from processing.app_processing import process_app_usage
import cx_Oracle
from datetime import datetime

def process_battery_raw_to_silver():
    """
    Landing --> silver
    """
    db = DBConnection(user="hr", password="hr", dsn="localhost:1521/XEPDB1")
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        query_raw = "SELECT raw_data FROM landing_raw_battery_status"
        cursor.execute(query_raw)
        raw_data = cursor.fetchall()

        column_mapping = {
            "timestamp": "timestamp",
            "AC powered": "\"AC_powered\"",
            "USB powered": "\"USB_powered\"",
            "Wireless powered": "\"Wireless_powered\"",
            "Dock powered": "\"Dock_powered\"",
            "Max charging current": "\"Max_charging_current\"",
            "Max charging voltage": "\"Max_charging_voltage\"",
            "voltage": "\"voltage\"",
            "Charge counter": "\"Charge_counter\"",
            "status": "\"status\"",
            "health": "\"health\"",
            "present": "\"present\"",
            "level": "\"level\"",
            "scale": "\"scale\"",
            "temperature": "\"temperature\"",
            "technology": "\"technology\"",
            "batteryMiscEvent": "\"batteryMiscEvent\"",
            "batteryCurrentEvent": "\"batteryCurrentEvent\"",
            "mSecPlugTypeSummary": "\"mSecPlugTypeSummary\"",
            "LED Charging": "\"LED_Charging\"",
            "LED Low Battery": "\"LED_Low_Battery\"",
            "current now": "\"current_now\"",
            "Adaptive Fast Charging Settings": "\"Adaptive_Fast_Charging_Settings\"",
            "Super Fast Charging Settings": "\"Super_Fast_Charging_Settings\"",
            "FEATURE_WIRELESS_FAST_CHARGER_CONTROL": "\"FEATURE_WIRELESS_FAST_CHARGER_CONTROL\"",
            "mWasUsedWirelessFastChargerPreviously": "\"mWasUsedWirelessFastChargerPreviously\"",
            "mWirelessFastChargingSettingsEnable": "\"mWirelessFastChargingSettingsEnable\"",
        }

        silver_rows = [
            {**{
                column_mapping[key]: value
                for key, value in parse_battery_status(
                    row[0].read() if isinstance(row[0], cx_Oracle.LOB) else row[0]
                ).items()
                if key in column_mapping
            }, 'timestamp': datetime.strptime(parse_battery_status(row[0].read() if isinstance(row[0], cx_Oracle.LOB) else row[0])["timestamp"], "%Y-%m-%d %H:%M:%S")}
            for row in raw_data
        ]

        for mapped_data in silver_rows:
            column_names = ", ".join(mapped_data.keys())
            placeholders = ", ".join([f":{key}" for key in mapped_data.keys()])

            insert_query = f"""
            INSERT INTO silver_processed_battery_status (
                {column_names}
            ) VALUES (
                {placeholders}
            )
            """
            cursor.execute(insert_query, mapped_data)

        connection.commit()
    except Exception as e:
        print(f"Error to process the data in process_battery_raw_to_silver: {e}")
    finally:
        db.close()

def process_app_raw_to_silver():
    """
    landing --> Silver.
    """
    db = DBConnection(user="hr", password="hr", dsn="localhost:1521/XEPDB1")
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        query_raw = "SELECT raw_data FROM landing_raw_app_usage"
        cursor.execute(query_raw)
        raw_data = cursor.fetchall()

        silver_data = []
        for row in raw_data:
            raw_lob = row[0] 

            # LOB TO STRING
            raw_output = raw_lob.read() if isinstance(raw_lob, cx_Oracle.LOB) else raw_lob

            # FUNCTION FROM DATA_PROCESSING
            processed_events = process_app_usage(raw_output)
            silver_data.extend(processed_events)
        # INSERTING INTO SILVER TABLE
        insert_query = """
        INSERT INTO silver_processed_app_usage (datetime, timestamp, event_type, package_name)
        VALUES (TO_TIMESTAMP(:1, 'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:2, 'YYYY-MM-DD'), :3, :4)
        """
        silver_rows = [
            (event["datetime"], event["timestamp"], event["event_type"], event["package_name"])
            for event in silver_data
        ]
        cursor.executemany(insert_query, silver_rows)
        connection.commit()
        print("App data usage processed: Raw ---> Silver")
    
    except Exception as e:
        print(f"Error to process the data in process_app_raw_to_silver: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing process in Silver layer")
    process_battery_raw_to_silver()
    #print("Starting apps processes")
    #process_app_raw_to_silver()
    print("Process in silver layer is concluded!")
