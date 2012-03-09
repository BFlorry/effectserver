#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time


class Instanssi(object):

    def __init__(self, nick, ip, port):
        self.ip = ip
        self.port = port
        self.nick = nick

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.reset()

    def reset(self):
        self.packet = [ 1 ] # Speksin versio aina yksi

        self.packet.append(0) # Aloita tagi osa
        for char in self.nick:
            self.packet.append(ord(char))
        self.packet.append(0) # Lopeta tagi osa


    def set(self, i, r, g, b):
        self.packet += [
            1, # Tehosteen tyyppi on yksi eli valo
            i, # Valon indeksi
            0, # Laajennustavu. Aina nolla. Älä välitä tästä
            r, # Punaisuus
            g, # Vihreys
            b, # Sinisyys
        ]

    def send(self):
        bytes = bytearray(self.packet)
        self.socket.sendto(bytes, (self.ip, self.port))
        self.reset()


valot = Instanssi("epeli", "192.168.10.1", 9909)


# Sinistä kansalle
for i in range(0, 38):
    valot.set(i, 0, 0,255)

i = 0
while True:
    valot.set(i, 0, 255, 0)
    valot.send()

    time.sleep(0.1)

    valot.set(i, 0, 0,255)
    valot.send()

    i += 1
    i = i % 38

    print i



valot.send()


