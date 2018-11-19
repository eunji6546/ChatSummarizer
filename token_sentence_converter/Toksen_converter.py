#-*-coding: utf-8
import os 
import sys 
sys.path.append('../noise_detector')
from noise_detector import noise_detec as ND

#reload(sys)
#sys.setdefaultencoding('utf-8') 

# python 3 깔린 venv 진입 
# source  /Users/user/py3/bin/activate
def check_name(first, second):
    if first[0] == second[0]:
        return True
    else:
        return False
    
def check_time(first, second):
    #exactly same
    if first[1][0] == second[1][0] and first[1][1] == second[1][1]:
        return 0
    #1 minute differ
    
    first_hour = int(first[1][1].split(':')[0])
    first_minute = int(first[1][1].split(':')[1])
    second_hour = int(second[1][1].split(':')[0])
    second_minute = int(second[1][1].split(':')[1])
    
    if first_hour == second_hour and first_minute == second_minute-1:
        return 1
    
    else:
        return 2


class Toksen:

	
	# idx of this list is sentence-index and elements of it is chat-index 
	# and index start with zero
	chat_to_sentence_mapping = [] 

	# Toksen-sentence, rexrank-sentence mapping 
	toksen_to_lexrank_mapping=[] 



	def __init__(self, input_sentences):
		self.input = [x.strip("\r").strip() for x in input_sentences.split("\n")]
		self.noise_detector = ND.NoiseDetector() 


	def __is_emoticon(self, chat):
		return "이모티콘" in chat 
	def __is_short_reaction (self, chat):	
		return len(set(chat))<3 
	def __remove_kk(self, chat):
		tok_list = ["ㅋ","ㅎ","?","!",".","ㅠ","@","ㅐ","ㅣ",'~','^',"ㅠ_ㅠ",":)",";"\
		"ㅛ","ㅜ", "ㄹ",":<"]
		new_chat = chat 
		for tok in tok_list:
			new_chat = new_chat.replace(tok,"")
		return new_chat

	def get_chat_to_sentence_mapping (self):
		return self.chat_to_sentence_mapping
	# -- tok-sen connecting methods : choose one 



	def by_person_only(self) :
		"""
		input : filename to read
		output : dictionary of {"who":"chat"} 
		"""
		chat_dict={}
		
		
		for line in self.input:
			line = line.strip(" ").strip()
			if line[0] != "[" :
				# means yymmdd 
				continue;
			try :
				who, when, what = line.split("]") 
			except:
				print("ELSE CASE : split ]") 
				continue;
			who = who.strip(" [").strip("] ") 
			when = when.strip(" [").strip("] ") 
			what = what.strip() 
			"""
			if not who in chat_dict.keys():
				chat_dict[who]={}
			if not when in chat_dict[who].keys():
				chat_dict[who][when]=[what]
			else :
				chat_dict[who][when].append(what)
			"""
			if not when in chat_dict.keys():
				chat_dict[when]={}
			if not who in chat_dict[when].keys():
				chat_dict[when][who]=[what]
			else :
				chat_dict[when][who].append(what)
		print (chat_dict)
	
	def by_time_connect(self):
		
		original= self.input[:]
		total = []
		
		for i in range(len(original)):
			new = []
			splited = original[i].split(']', 2)
			splited[0] = splited[0].strip(' ')
			splited[0] = splited[0].strip('[')
			splited[1] = splited[1].strip(' ')
			splited[1] = splited[1].strip('[')        
		    
			new.append(splited[0]) #name
			new.append(splited[1].split(' ')) #time
			new.append(splited[2].strip()) #message
		    
			original[i] = new
		
		while(len(original) != 0):
			i = 1
			index_list =[0]
			message=""
			while(i<len(original)-1 and check_time(original[i], original[0]) == 0):
				if(check_name(original[0], original[i])):
					index_list.insert(0,i)
				i+=1
			
			#while(i<len(original)-1 and check_time(original[i], original[0]) ==1):
				#if(check_name(original[0], original[i])):
					#index_list.insert(0,i)
					#i+=1
				#else:
					#break
			chat_idxs_of_cur_sentence = [] 
			for i in index_list:
				message = self.noise_detector.remove( original[i][2]) +' '+ message
				chat_idxs_of_cur_sentence.append(i)
				original.pop(i)
			self.chat_to_sentence_mapping.append(chat_idxs_of_cur_sentence)
			message = message.strip() + ' .'
			total.append(message)
		
		f.close()
		return total
		

	def as_it_is (self):
		chat_dict={}
		prev_who = None
		to_print = ""
		total= []
		chat_idx = 0
		sentence_idx = 0 
		chat_idxs_of_cur_sentence = []

		for line in self.input :
	

			line = line.strip(" ").strip()
			try :
				who, when, what = line.split("]") 
			except:
				# print("ELSE CASE : split ]") 
				continue;
			who = who.strip(" [").strip("] ") 
			when = when.strip(" [").strip("] ") 
			what = what.strip()
			what = self.noise_detector.remove(what)
			#if self.__is_emoticon (what) or self.__is_short_reaction (what) : 
			#	continue 
			
			if prev_who != who :
				#print(to_print)
				if prev_who != None and len(to_print) !=0 :
					to_print = to_print.strip()
					self.chat_to_sentence_mapping.append([sentence_idx, chat_idxs_of_cur_sentence,to_print])
					chat_idxs_of_cur_sentence = [] 
					sentence_idx +=1 
					if len(to_print) >0 :
						 
						if to_print[-1] in ["?","!","."] :
							total.append(to_print )  
						else :
							total.append(to_print + ".")
					

				to_print = what 

			else :
				to_print += " " + what 

			chat_idxs_of_cur_sentence.append(chat_idx)
			
			prev_who = who 
			chat_idx += 1 

		# last line 
		if len(to_print) >0 : 
			total.append(to_print.strip())
		self.chat_to_sentence_mapping.append([sentence_idx, chat_idxs_of_cur_sentence, to_print])
		self.toksen = total 
		return total 
	
	
			

