import pywws.weatherstation
import datetime
from time import time 
from uuid import getnode as get_mac
MAC_ADDRESS = ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class MyWeatherstation():
    def __init__(self):
        self._ws = pywws.weatherstation.WeatherStation()
        self._data = []
    
    def set_fixed_data(self):
        if self._data:
            self._ws.write_data(self._data)
        self._data = []
    
    def prepare_set_data_count(self, val=0):
        ptr = self._ws.fixed_format['data_count'][0]
        self._data.append((ptr, val))

    def prepare_set_current_pos(self, val=0):
        ptr = self._ws.fixed_format['current_pos'][0]
        self._data.append((ptr, val))

    def prepare_set_read_period(self, val=5):
        ptr = self._ws.fixed_format['read_period'][0]
        self._data.append((ptr, val))
    
    def measure(self):
        measurements = []
        date = datetime.datetime.now().replace(second=0, microsecond=0)
        date_fixed = date.strftime(DATE_FORMAT)
        timestamp = int(time())

        fixed_block = self._ws.get_fixed_block()
        ptr = fixed_block.get('current_pos')
        read_timezone = fixed_block.get('timezone')
        read_period = fixed_block.get('read_period')
        read_datetime = fixed_block.get('date_time')
        for i in range(fixed_block.get('data_count', 0)):
            data = self._ws.get_data(ptr, True)
            data['server_timestamp'] = timestamp
            data['server_datetime'] = date_fixed
            data['station_timezone_rf'] = read_timezone
            data['station_datetime_rf'] = read_datetime
            data['stationame'] = MAC_ADDRESS
            if data.get('delay'):
                date = date - datetime.timedelta(minutes=data.get('delay'))
                data['read_datetime'] = date.strftime(DATE_FORMAT)
            data['read_period'] = read_period
            data['read_pos'] = ptr
            data['status_lost_connection'] = data.get('status', {}).get('lost_connection')
            data['status_rain_overflow'] = data.get('status', {}).get('rain_overflow')
            measurements.append(data)

            ptr = self._ws.dec_ptr(ptr)
        
        print(fixed_block)
        print(measurements)

        if len(measurements):
            if(fixed_block.get('read_period', 0) != 5):
                self.prepare_set_read_period()
            self.prepare_set_data_count(0)
            self.set_fixed_data()

        return measurements

if __name__ == "__main__":
    ws = MyWeatherstation()
    ws.measure()