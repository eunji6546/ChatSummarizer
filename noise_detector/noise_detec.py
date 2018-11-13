class NoiseDetector:
    def __init__(self, file="noise_dic.txt"):
        self.dic = {}
        with open(file, 'r', encoding= 'UTF8') as f:
            noises = f.readlines()
            for noise in noises:
                noise = noise.strip()

    def remove(self, text):
        for noise in noises:
            text = text.replace(noise, ' ')
        return text