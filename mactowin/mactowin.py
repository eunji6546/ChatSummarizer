class MactoWin:

    def __init__(self):
        self.input = input
        self.current_time = '2018.11.6'

    def convert(self, text):
        # for j in range(21):
        #     if(j ==2):
        #         continue        
        #     f = open('C:/Users/ehgus/Desktop/ÀüÇÁ/project/ChatSummarizer/sample_data/chat'+str(j+2)+'.txt', "r", encoding='UTF8')
        #     f2 = open('chat'+str(j+2)+'.txt', "w", encoding='UTF8')
        
        original_text = text.split('\n')
        i=0
        while(len(original_text)>i):
            if(i>=1 and len(original_text[i].split(']', 2))<3 and original_text[i].split(']', 2)[0] != 2018):
                original_text[i-1] = original_text[i-1].strip('\n').strip("\r") + " " + original_text[i].strip("\r") +'\n'
                original_text.pop(i)
                continue
            original_text[i] = original_text[i]+'\n'
            i+=1
        print(original_text)

        if(len(original_text[0].split('['))>2 and original_text[0].split('[')[2][0] =='2'):
            return text



        converted =""
        for i in range(len(original_text)):
            splited = original_text[i].split(']', 2)
            if(len(splited) < 3):
                splited = original_text[i].split(' ',3)
                if(splited[0] == '2018년'):
                    self.current_time = splited[0].strip('년')+'.'+splited[1].strip('월')+'.'+splited[2].strip('일')
                    continue
                continue
            
            splited[1] = splited[1].strip(' ')
            splited[1] = splited[1].strip('[')
                
            if(splited[1].split(' ')[0] == '오전'):
                if(int(splited[1].split(' ')[1].split(':')[0]) == 12):
                    converted = converted + splited[0]+ '] '+'['+self.current_time+ ' ' + str(int(splited[1].split(' ')[1].split(':')[0])-12) +':'+splited[1].split(' ')[1].split(':')[1] +'' + ']'+ splited[2]
                    #f2.write(splited[0]+ '] '+'['+current_time+ ' ' + str(int(splited[1].split(' ')[1].split(':')[0])-12) +':'+splited[1].split(' ')[1].split(':')[1] +'' + '] '+ splited[2])
                else:
                    converted = converted + splited[0]+ '] '+'['+self.current_time + ' ' +splited[1].split(' ')[1]+']' + splited[2]
                    #f2.write(splited[0]+ '] '+'['+current_time + ' ' +splited[1].split(' ')[1]+']' + ' '+ splited[2])
            elif(splited[1].split(' ')[0] == '오후'):
                if(int(splited[1].split(' ')[1].split(':')[0]) == 12):
                    converted = converted + splited[0]+ '] '+'['+self.current_time+ ' ' + splited[1].split(' ')[1].split(':')[0] +':'+splited[1].split(' ')[1].split(':')[1] +'' + ']'+ splited[2]
                    #f2.write(splited[0]+ '] '+'['+current_time+ ' ' + splited[1].split(' ')[1].split(':')[0] +':'+splited[1].split(' ')[1].split(':')[1] +'' + '] '+ splited[2])
                else:
                    converted = converted + splited[0]+ '] '+'['+self.current_time+ ' ' + str(int(splited[1].split(' ')[1].split(':')[0])+12) +':'+splited[1].split(' ')[1].split(':')[1] +'' + ']'+ splited[2]
                    #f2.write(splited[0]+ '] '+'['+current_time+ ' ' + str(int(splited[1].split(' ')[1].split(':')[0])+12) +':'+splited[1].split(' ')[1].split(':')[1] +'' + '] '+ splited[2])
            else:
                converted = converted + original_text[i]
                #f2.write(original_text[i])

        return converted
#            f.close()
#            f2.close()
