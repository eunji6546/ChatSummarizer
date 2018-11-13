import os 
import sys 

class NoiseDetector:
    def __init__(self, file="./noise_detector/noise_dic.txt"):
        self.dic = {}
        with open(file, 'r', encoding= 'UTF8') as f:
            self.noises = f.readlines()
            self.noises = [x.strip() for x in self.noises ] 

    def remove(self, text):
        for noise in self.noises:
            text = text.replace(noise, ' ')
        return text