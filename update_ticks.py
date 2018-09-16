import json
import pandas as pd
from urllib3 import PoolManager
import mysql.connector
import numpy as np

def get_data():
  security = "EUR_USD"
  granularity = "M1"
  api_token = ""
  url = "https://api-fxpractice.oanda.com/v1/candles"
  payload = {
  "instrument": security,
  #"accountId": self.account_id,
  "candleFormat": "midpoint",
  "granularity": granularity,
  "count": "5000",
  #"start": "2016-01-10T15:00:00.000000Z",
  #"end": "2016-03-01T15:00:00.000000Z"
  #"dailyAlignment": "0",
  #"alignmentTimezone": "America%2FNew_York"
  }

  header = {"Authorization": "Bearer " + api_token}
  manager = PoolManager(10)
  req = manager.request("GET", url, fields=payload, headers=header)
  return req

def load_db():
  response = get_data()
  if response.status == 200:
    response_data = response.data
    decoded_response_data = response_data.decode("utf_8")
    jsonDict = json.loads(decoded_response_data)
    json_df = pd.DataFrame.from_dict(jsonDict).join(pd.DataFrame.from_dict(jsonDict["candles"])).drop("candles", axis=1)


    json_df["time_dt"] = pd.to_datetime(json_df["time"])
    json_df["timestamp"] = json_df["time_dt"].astype(np.int64) // 10 ** 9

    db_tick_time = json_df["time_dt"].apply(str)
    db_timestamp = json_df["timestamp"].values.tolist()
    db_tick_year = json_df["time_dt"].dt.year.tolist()
    db_tick_hour = json_df["time_dt"].dt.hour.tolist()
    db_tick_minute = json_df["time_dt"].dt.minute.tolist()
    db_tick_second = json_df["time_dt"].dt.second.tolist()
    db_tick_dayofweek = json_df["time_dt"].dt.dayofweek.tolist()
    db_tick_dayofmonth = json_df["time_dt"].dt.day.tolist()
    db_tick_dayofyear = json_df["time_dt"].dt.dayofyear.tolist()
    db_tick_instrument = json_df["instrument"].values.tolist()
    db_tick_openMid = json_df["openMid"].values.tolist()
    db_tick_highMid = json_df["highMid"].values.tolist()
    db_tick_lowMid = json_df["lowMid"].values.tolist()
    db_tick_closeMid = json_df["closeMid"].values.tolist()
    db_tick_volume = json_df["volume"].values.tolist()
    db_tick_granularity = json_df["granularity"].values.tolist()
    row_data = []

    for i in range(json_df.shape[0]):
      row_data.append((db_tick_time[i], db_timestamp[i], db_tick_year[i], db_tick_hour[i], db_tick_minute[i], db_tick_second[i], db_tick_dayofweek[i], db_tick_dayofmonth[i], db_tick_dayofyear[i], db_tick_instrument[i], db_tick_openMid[i], db_tick_highMid[i], db_tick_lowMid[i], db_tick_closeMid[i], db_tick_volume[i], db_tick_granularity[i]))

    db_user = ""
    db_password = ""
    db_host = "localhost"
    database_name = ""
    
    #Open database connection)
    db = mysql.connector.connect(user=db_user, password=db_password,
                  host=db_host,
                  database=database_name)


    # prepare a cursor object using cursor() method
    cursor = db.cursor()
      #execute SQL query using execute() method.
    cursor.executemany("""insert into tick (tick_datetime, tick_timestamp, tick_year, tick_hour, tick_minute, tick_second, tick_dayofweek, tick_dayofmonth, tick_dayofyear, tick_security, tick_openMid, tick_highMid, tick_lowMid, tick_closeMid, tick_volume, tick_granularity) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update tick.tick_datetime = IF(VALUES(tick_datetime) < tick.tick_datetime, tick.tick_datetime, VALUES(tick_datetime))""", row_data)

    #disconnect from server
    db.commit()
    cursor.close()
    db.close()

if __name__ == "__main__":
  load_db()
