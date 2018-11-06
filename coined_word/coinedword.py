class Coinedword:
    def __init__(self, file="coinedword_dic.txt"):
        self.dic = {}
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                split = line.split(':')
                self.dic[split[0]] = split[1].strip()

    def convert(self, text):
        for coined, meaning in self.dic.items():
            text = text.replace(coined, meaning)
        return text