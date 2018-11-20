class Coinedword:
    def __init__(self, file="coinedword_dic.txt"):
        self.dic = {}
        with open(file, 'r', encoding= 'UTF8') as f:
            lines = f.readlines()
            for line in lines:
                split = line.split(':')
                self.dic[split[0]] = split[1].strip()

    def convert(self, text):
        words = sorted(self.dic.items(), reverse=True)
        for coined, meaning in words:
            text = text.replace(coined, meaning)
        return text