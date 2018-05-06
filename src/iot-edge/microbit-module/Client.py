#!/usr/bin/env python

from iothub_client import IoTHubClient
from iothub_client import IoTHubTransportProvider
from iothub_client import IoTHubMessage

class Client:

  __PROTOCOL = IoTHubTransportProvider.MQTT
  __MESSAGE_TIMEOUT = 10000

  def connect(self, connection_string):
    self.__client = IoTHubClient(connection_string, self.__PROTOCOL)
    self.__client.set_option('messageTimeout', self.__MESSAGE_TIMEOUT)

  def set_certificates(self, cert_file):
    file = open(cert_file)
    self.__client.set_option('TrustedCerts', file.read())
    file.close()

  def send_message_async(self, output_name, payload, message_callback, user_context):
    message = IoTHubMessage(payload)
    self.__client.send_event_async(output_name, message, message_callback, user_context)

  def set_receive_message_callback(self, input_name, message_callback, user_context):
    self.__client.set_message_callback(input_name, message_callback, user_context)

  def set_device_twin_callback(self, callback, user_context):
    self.__client.set_device_twin_callback(callback, user_context)
