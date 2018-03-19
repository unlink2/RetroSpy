import serial
from axel import Event

# This class models the connection to an arduino
#
# Constructors:
# callback: callback class
# serial port: port of the arduino (defaults to /dev/ttyACM0)
# baud_rate: set baud rate (defaults to 9600)
# timer_ms: set read timeout (defaults to 30)
#
# The callback class should only have 2 methodes
# onSuccess(self, data)
# onError(self, data)
#
# Implementation Status: Ported


class SerialMonitor:
    def __init__(self, serial_port='/dev/ttyACM0', baud_rate=115200,
                 timer_ms=10):
        self.baud_rate = baud_rate
        self.serial_port = serial_port
        self.timer_ms = timer_ms

        # array of bytes
        self._localBuffer = []

        #  establish connection
        self._datPort = serial.Serial(serial_port, baud_rate, timeout=timer_ms)
        # self._datPort.timeout = timer_ms

        self.packet_recv = Event()
        self.disconnected = Event()
        self.onerror = Event()

    def start(self):
        pass

    def stop(self):
        if not self._datPort.is_open:
            return
        self._datPort.close()

    def serial_read(self, bytes=16):
        if not self._datPort.is_open:
            return None

        s = self._datPort.read(bytes)

        self._localBuffer.extend(s)

        # try and find 2 splitting characters in the local buffer
        # one starts the package, one ends it
        # if they are found they will fire the callback
        # since python has no reverse index, we just enumerate
        lastSplitIndex = None
        secondLastSplitIndex = None
        for i, v in enumerate(self._localBuffer):
            if v == 0x0A:
                secondLastSplitIndex = lastSplitIndex
                lastSplitIndex = i
        if lastSplitIndex is None or secondLastSplitIndex is None:
            return s

        # fire event
        self.packet_recv(self._localBuffer[secondLastSplitIndex + 1:lastSplitIndex])

        del self._localBuffer[0:lastSplitIndex + 1]

        return s

    def set_pin_mode(self, pin_number, mode):
        if not self._datPort.is_open:
            return
        """
        Performs a pinMode() operation on pin_number
        Internally sends b'M{mode}{pin_number} where mode could be:
        - I for INPUT
        - O for OUTPUT
        - P for INPUT_PULLUP MO13
        """
        command = (''.join(('M',mode,str(pin_number)))).encode()
        self._datPort.write(command)

    def serial_write(self, data):
        if not self._datPort.is_open:
            return
        self._datPort.write(data.encode())

    def digital_write(self, pin, value):
        if not self._datPort.is_open:
            return
        """
        Writes the digital_value on pin_number
        Internally sends b'WD{pin_number}:{digital_value}' over the serial
        connection
        """
        command = (''.join(('WD', str(pin), ':',
                   str(value)))).encode()
        self._datPort.write(command)

    # this function performs a read on any pin. This is used for debugging
    def digital_read(self, pin):
        if not self._datPort.is_open:
            return 0
        command = (''.join(('RD', str(pin)))).encode()

        self._datPort.write(command)
        line_received = self._datPort.readline().decode().strip()
        header, value = line_received.split(':')  # e.g. D13:1

        if header == ('D' + str(pin)):
            if pin == 0xFF:
                # returns string of all pins in order
                return value
            return int(value)

    def is_open(self):
        return self._datPort.is_open
