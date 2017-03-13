import time
import serial
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import GPS_ellipse as gps
class MyHandler(PatternMatchingEventHandler):

    patterns=["*.jpg"]
    powr=[90,80,70,60,50,40]
    way=[1,2,3,4,1,2]
    i=0
    ser = serial.Serial()
    ser.port='/dev/ttyUSB0'
    ser.baudrate=19200
    ser.timeout=1
    ser.open()

    def __init__(self):
        self.spoof = gps.spoof_gps()
        self.spoof.generate()

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """

        c_lat = self.spoof.curr_lat
        c_long = self.spoof.curr_long
        st_lt=str(c_lat)+'\n'
        st_lon=str(c_long)+'\n'
        st_powr=str(self.powr[self.i])+'\n'
        st_way=str(self.way[self.i])+'\n'
        self.ser.write(st_lt.encode('utf-8'))
        self.ser.write(st_lon.encode('utf-8'))
        self.ser.write(st_powr.encode('utf-8'))
        self.ser.write(st_way.encode('utf-8'))
        with open(event.src_path, 'rb') as f:
            self.ser.write(f.read())
        self.i += 1
        self.spoof.generate()
        if (self.i > 5):
            self.i = 0

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    observer = Observer()
    observer.schedule(MyHandler(), path='.',recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(3)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
