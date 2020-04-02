import serial

import logger


class DynonSerialReader(object):

    def __init__(
        self,
        serial_port: str
    ):
        super().__init__()

        self.serial_port = serial_port
        self.serial_reader = None

        self.open_serial_connection()

    def open_serial_connection(
        self
    ):
        try:
            if self.serial_reader is None or not self.serial_reader.is_open():
                logger.log(
                    f'ATTEMPTING to open connection to {self.serial_port}')

                self.serial_reader = serial.Serial(
                    self.serial_port,
                    baudrate=115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=10)

                self.serial_reader.flushInput()

                logger.log(f'OPENED serial connection to {self.serial_port}')
        except:
            self.serial_reader = None
            logger.log(
                f'FAILED attempt to open serial connection to {self.serial_port}')

    def read(
        self
    ):
        try:
            if self.serial_reader is not None and self.serial_reader.is_open():
                serial_bytes = self.serial_reader.readline()

                if serial_bytes != None and len(serial_bytes) > 0:
                    raw_read = str(serial_bytes, encoding='ascii')
                    logger.log(raw_read)
                    return raw_read
            else:
                self.open_serial_connection()

            return ""
        except:
            try:
                self.serial_reader.close()
            finally:
                self.serial_reader = None