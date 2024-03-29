from model.SocketConnector import SocketConnector 
from MQ135 import MQ135

import time
import machine
import WLAN_connection 
ssid = [84, 111, 116, 97, 108, 112, 108, 97, 121, 45, 54, 53, 65, 53]
password = [54, 53, 65, 53, 50, 56, 56, 52, 77, 89, 72, 66, 84, 121, 87, 120]

def int_to_ascii(list_number: list)-> str:
  string = ''
  for i in range(0, len(list_number)):
      string = string + chr(list_number[i])
  return string
 
 


multicast_group = '224.10.10.10' 
port = 10000

led = machine.Pin('LED', machine.Pin.OUT)


#ssid = 'labred'
#password = 'labred2017'

station = WLAN_connection.init_connection(int_to_ascii(ssid), int_to_ascii(password))

while station.isconnected() == False:
  pass

print('WiFi Connection is successful')

temperature = 7.0
humidity = 61.0
a = 5.2735
b = -0.3503
Rl = 20000
value = 0
Rs = 0
Rs_Media = 0
Ro = 0

ppm_CO2_actual = 0



mq135 = MQ135(28)

print('Connecting to ' + str(multicast_group) + ' : ' + str(port))
web_socket_sender = SocketConnector(multicast_group, port)

while True:
  #message = b'Im Raspberry Pi Pico W, Whats u r name?'
  count = 0
  for i in range(0, 600):
    valor = mq135.read()
    Rs = Rl*(1023/valor)-Rl
    count = Rs + count
  Rs_Media = count/600
  time.sleep_ms(1000)
  ppm_CO2_actual = mq135.read()
  Ro = Rs_Media/(a*ppm_CO2_actual**b)
  print('Valor actual: ' + str(ppm_CO2_actual) + ' ppm')
  print('Rs media: ' + str(Rs_Media))
  print('Ro: ' + str(Ro))
  
  message = str(ppm_CO2_actual) + ' ' + str(Rs_Media) + ' ' + str(Ro)
  web_socket_sender.send_msg(message)
  
  
  led.off()
  time.sleep_ms(500)
  led.on()
  
