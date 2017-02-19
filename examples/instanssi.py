#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time

# DMX-valojen määrä
NUM_LIGHTS = 24

# Valopalvelimen IP-osoite
HOSTNAME = "192.168.0.61"

# Paketin lähettäjä
USER = "hakkeri"



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




valot = Instanssi(USER, HOSTNAME, 9909) # Muokkaa nick ja IP oikeiksi


# Sinistä kansalle. Aseta kaikki valot sinisiksi
for i in range(0, NUM_LIGHTS):
    valot.set(i, 0, 0,255)
# Lähetä valokäskyt kaikki kerralla
valot.send()


# Kiertävä vihreä valo

i = 0
# XXX: ikiloopit on pahasta
while True:
    valot.set(i, 0, 255, 0)
    valot.send()

    time.sleep(0.05)

    valot.set(i, 0, 0,255)
    valot.send()

    i += 1
    i = i % NUM_LIGHTS

    print(i)
