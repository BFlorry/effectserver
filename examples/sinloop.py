#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time
import math

# DMX-valojen määrä
NUM_LIGHTS = 24

# Valopalvelimen IP-osoite
HOSTNAME = "192.168.0.61"

# Paketin lähettäjä
USER = "hakkeri"

# Valojen kirkkaus, 0 < BRIGHTNESS < 1
BRIGHTNESS = 1



class Instanssi(object):
    """
    Python-luokka Instanssin valojen hallintaan. Laittaa vihreän valon kiertämään.
    """



    def __init__(self, nick, ip, port):
        self.ip = ip
        self.port = port
        self.nick = nick

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.reset()


    def reset(self):
        """Resetoi UDP-paketti"""
        self.packet = [ 1 ] # Speksin versio aina yksi

        self.packet.append(0) # Aloita nimitagi
        for char in self.nick:
            # Muunna nickin merkit ASCII:ksi
            self.packet.append(ord(char))
        self.packet.append(0) # Lopeta nimitagi


    def set(self, i, r, g, b):
        """Aseta valo i RGB-arvoon"""
        self.packet += [
            1, # Tehosteen tyyppi on yksi eli valo
            i, # Valon indeksi
            0, # Laajennustavu, aina nolla.
            r, # Punaisen määrä, 0-255
            g, # Vihreän määrä, 0-255
            b, # Sinisen määrä, 0-255
        ]


    def send(self):
        """Lähetä asetetut tavut ja nollaa pakettilista"""
        bytes = bytearray(self.packet)
        self.socket.sendto(bytes, (self.ip, self.port))
        self.reset()

    



def intensity(angle):
    # Siirtää käyrän Y-koordinaatiston välille 0-1 ja kertoo väriavaruuden maksimilla
    intensity = int(((math.sin(angle) * 0.5 + 0.5)* 255)* BRIGHTNESS) % 256
    return intensity
        

valot = Instanssi(USER, HOSTNAME, 9909)


# Markan plasmaefekti kaikille valoille yhtäaikaa

angle = 0

try:
    while True:
        
        intensr = intensity(angle)
        intensg = intensity(angle + 90)
        intensb = intensity(angle + 180)

        print (intensr, intensg, intensb)
        
        for i in range(0, NUM_LIGHTS):
            valot.set(i, intensr, intensg, intensb)
        valot.send()


        angle += 0.01
        angle = angle % 360


        time.sleep(0.02)
except KeyboardInterrupt:
    pass
