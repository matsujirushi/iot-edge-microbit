#!/usr/bin/env python

import Adafruit_BluefruitLE
import uuid
import struct

class MicroBit:

  __SERVICE_ACCEL = uuid.UUID('e95d0753-251d-470a-a062-fa1922dfa9a8')   # MicroBit Accelerometer Service
  __CHAR_ACCEL_DATA = uuid.UUID('e95dca4b-251d-470a-a062-fa1922dfa9a8') # Accelerometer Data

  def __init__(self, device):
    self.__device = device

  @property
  def id(self):
    return self.__device.id

  def connect(self):
    if not self.__device.is_connected:
      self.__device.connect()
    self.__device.discover([self.__SERVICE_ACCEL], [self.__CHAR_ACCEL_DATA])
    service = self.__device.find_service(self.__SERVICE_ACCEL)
    self.__char_accel_data = service.find_characteristic(self.__CHAR_ACCEL_DATA)

  def disconnect(self):
    if self.__device.is_connected:
      self.__device.disconnect()

  def read_accel_value(self):
    data = self.__char_accel_data.read_value()
    x = struct.unpack('<h', bytearray((data[0], data[1])))[0]
    y = struct.unpack('<h', bytearray((data[2], data[3])))[0]
    z = struct.unpack('<h', bytearray((data[4], data[5])))[0]
    return (x, y, z)