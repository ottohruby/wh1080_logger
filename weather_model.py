from base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.inspection import inspect

class Weather(Base):
   __tablename__ = 'weather'
   id = Column(Integer, primary_key=True)
   replicated = Column(Boolean, default=False)
   #server_datetime = Column(DateTime(timezone=True), server_default=func.now())
   server_datetime = Column(String(length=20), nullable=True)
   server_timestamp = Column(String(length=16), nullable=True)

   stationame = Column(String(length=20), nullable=True) 
   station_datetime_rf = Column(String(length=20), nullable=True)
   station_timezone_rf = Column(String(length=10), nullable=True)
   read_period = Column(String(length=10), nullable=True)
   read_datetime = Column(String(length=20), nullable=True)
   read_pos = Column(String(length=10), nullable=True)

   delay = Column(String(length=10), nullable=True)
   abs_pressure = Column(String(length=10), nullable=True)
   rel_pressure = Column(String(length=10), nullable=True)
   hum_in = Column(String(length=10), nullable=True)
   hum_out = Column(String(length=10), nullable=True)
   rain = Column(String(length=10), nullable=True)
   temp_in = Column(String(length=10), nullable=True)
   temp_out = Column(String(length=10), nullable=True)
   wind_ave = Column(String(length=10), nullable=True)
   wind_dir = Column(String(length=10), nullable=True) 
   wind_gust = Column(String(length=10), nullable=True)
   status_lost_connection = Column(String(length=5), nullable=True)
   status_rain_overflow = Column(String(length=5), nullable=True)

   # abs_pressure_unit = Column(String(length=10), nullable=True)
   # rel_pressure_unit = Column(String(length=10), nullable=True)
   # rain_unit = Column(String(length=10), nullable=True)
   # temp_in_unit = Column(String(length=10), nullable=True)
   # temp_out_unit = Column(String(length=10), nullable=True)
   # wind_unit = Column(String(length=10), nullable=True)

def addWeather(session, rows):
   table = inspect(Weather)
   for row in rows:
      filtered_row = dict()
      for col in row:
         if col in table.c:   
            filtered_row[col] = str(row[col])

      newWeather = Weather(**filtered_row)
      session.add(newWeather)
      
   session.commit()
   
