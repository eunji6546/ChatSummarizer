if __name__ == '__main__':
    current_time = '2018.11.6'
    for j in range(21):
        if(j ==2):
            continue        
        f = open('C:/Users/ehgus/Desktop/����/project/ChatSummarizer/sample_data/chat'+str(j+2)+'.txt', "r", encoding='UTF8')
        f2 = open('chat'+str(j+2)+'.txt', "w", encoding='UTF8')
        
        original_text = f.readlines()
        #[15�ΰ��� �����] [���� 11:49] �� ���� ���� �������� õ���̳�
        for i in range(len(original_text)):
            splited = original_text[i].split(']', 2)
            if(len(splited) < 3):
                splited = original_text[i].split(' ',3)
                if(splited[0] == '2018��'):
                    current_time = splited[0].strip('��')+'.'+splited[1].strip('��')+'.'+splited[2].strip('��')
                    continue
                continue
            
            splited[1] = splited[1].strip(' ')
            splited[1] = splited[1].strip('[')
                
            if(splited[1].split(' ')[0] == '����'):
                if(int(splited[1].split(' ')[1].split(':')[0]) == 12):
                    f2.write(splited[0]+ '] '+'['+current_time+ ' ' + str(int(splited[1].split(' ')[1].split(':')[0])-12) +':'+splited[1].split(' ')[1].split(':')[1] +'' + '] '+ splited[2])
                else:
                    f2.write(splited[0]+ '] '+'['+current_time + ' ' +splited[1].split(' ')[1]+']' + ' '+ splited[2])
            elif(splited[1].split(' ')[0] == '����'):
                if(int(splited[1].split(' ')[1].split(':')[0]) == 12):
                    f2.write(splited[0]+ '] '+'['+current_time+ ' ' + splited[1].split(' ')[1].split(':')[0] +':'+splited[1].split(' ')[1].split(':')[1] +'' + '] '+ splited[2])
                else:
                    f2.write(splited[0]+ '] '+'['+current_time+ ' ' + str(int(splited[1].split(' ')[1].split(':')[0])+12) +':'+splited[1].split(' ')[1].split(':')[1] +'' + '] '+ splited[2])
            else:
                f2.write(original_text[i])
        f.close()
        f2.close()
