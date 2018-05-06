#!/usr/bin/env python

import Adafruit_BluefruitLE
from MicroBit import MicroBit
from Client import Client
from iothub_client import IoTHubTwinUpdateState
from iothub_client import IoTHubMessageDispositionResult
import os
import time
import json

PollingInterval = -1
DeviceIdList = []

def find_device(devices, id):
  for device in devices:
    if device.id == id:
      return device
  return None

def device_twin_callback(update_state, payload, user_context):
  print('\nTwin callback called with:')
  print('  updateStatus = {}'.format(update_state))
  print('  payload = {}\n'.format(payload))

  global PollingInterval
  global DeviceIdList
  j = json.loads(payload)
  if update_state == IoTHubTwinUpdateState.COMPLETE:
    PollingInterval = j['desired']['PollingInterval']
    DeviceIdList = json.loads(j['desired']['DeviceIdList'])
  elif update_state == IoTHubTwinUpdateState.PARTIAL:
    PollingInterval = j['PollingInterval']

def receive_message_callback(message, user_context):
  message_buffer = message.get_bytearray()
  size = len(message_buffer)
  print('Received Message <<<{}>>> & Size={}'.format(message_buffer[:size].decmde('utf-8'), size))
  return IoTHubMessageDispositionResult.ACCEPTED

def send_confirmation_callback(message, result, user_context):
    print('Confirmation[{}] received for message with result = {}'.format(user_context, result))

def main():

  print('Connect IoT Edge.')
  connection_string = os.environ.get('EdgeHubConnectionString')
  cert_file = os.environ.get('EdgeModuleCACertificateFile')
  client = Client()
  client.connect(connection_string)
  client.set_certificates(cert_file)

  client.set_device_twin_callback(device_twin_callback, None)
  client.set_receive_message_callback('input1', receive_message_callback, None)

  print('Wait for module twin.')
  while PollingInterval < 0:
    time.sleep(1)

  print('Turn on bluetooth adapter.')
  adapter = provider.get_default_adapter()
  adapter.power_on()

  print('Get device list.')
  all_devices = provider.list_devices()

  print('Connect devices.')
  mb_devices = []
  for device_id in DeviceIdList:
    print '[{}] Find device...'.format(device_id),
    device = find_device(all_devices, device_id)
    if device is None:
      print('Not found.')
      continue
    print('Found.')

    mb_device = MicroBit(device)
    try:
      print('[{}] Connect device.'.format(mb_device.id))
      mb_device.connect()
    except:
      print('ERROR: Connecton failed.')
      continue

    mb_devices.append(mb_device)

  print('Check number of connect.')
  if len(mb_devices) != len(DeviceIdList):
    return

  message_counter = 0
  while True:
    for mb_device in mb_devices:
      xyz = mb_device.read_accel_value()
      message = '{{"id":"{}","x":{},"y":{},"z":{}}}'.format(mb_device.id, xyz[0], xyz[1], xyz[2])
      print(message)
      client.send_message_async(str(mb_device.id), message, send_confirmation_callback, message_counter)
    message_counter += 1
    time.sleep(PollingInterval)

  print('Disconnect devices.')
  for mb_device in mb_devices:
    print('[{}] Disconnect device.'.format(mb_device.id))
    mb_device.disconnect()

if __name__ == '__main__':
  provider = Adafruit_BluefruitLE.get_provider()
  provider.initialize()
  provider.run_mainloop_with(main)
