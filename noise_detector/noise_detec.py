import os 
import sys 

class NoiseDetector:
    def __init__(self, file="./noise_detector/noise_dictionary.txt"):
        self.dic = {}
        with open(file, 'r', encoding= 'UTF8') as f:
            self.noises = f.readlines()
            self.noises = [x.strip() for x in self.noises ] 

    def remove(self, text):
        for noise in self.noises:
            text = text.replace(noise, '')
            
        # if len(text)==1 : return ""
        # if len(text.split(" "))<3 : return ""
        return text