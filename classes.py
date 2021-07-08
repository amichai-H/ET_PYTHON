import threading


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class AccessPoint:
    def __init__(self, bssid, ssid, dbm_signal, channel, crypto):
        self.ssid = ssid
        self.dbm_signal = dbm_signal
        self.channel = channel
        self.crypto = crypto
        self.bssid = bssid
        self.connectDev = []

    def __add__(self, other):
        self.connectDev.append(other)