#-*-coding: utf-8
import os 
import sys 
#reload(sys)
#sys.setdefaultencoding('utf-8') 

# python 3 깔린 venv 진입 
# source  /Users/user/py3/bin/activate
class Toksen:

	def __init__(self, fname):
		self.fname = fname 

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

	# -- tok-sen connecting methods : choose one 



	def by_person_only(self) :
		"""
		input : filename to read
		output : dictionary of {"who":"chat"} 
		"""
		chat_dict={}
		
		with open(fname,'r', encoding='utf-8') as f :
			for line in f.readlines():
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
	
	def by_time_only(self):
		pass 
		

	def as_it_is (self):
		chat_dict={}
		prev_who = None
		to_print = ""
		total= []
		with open(self.fname,'r', encoding='utf-8') as f :
			for line in f.readlines():
		
				line = line.strip(" ").strip()
				try :
					who, when, what = line.split("]") 
				except:
					# print("ELSE CASE : split ]") 
					continue;
				who = who.strip(" [").strip("] ") 
				when = when.strip(" [").strip("] ") 
				what = what.strip()
				#if self.__is_emoticon (what) or self.__is_short_reaction (what) : 
				#	continue 
				
				if prev_who != who :
					#print(to_print)
					if prev_who != None and len(to_print) !=0 :
						if to_print[-1] in ["?","!","."] :
							total.append(to_print )  
						else :
							total.append(to_print + ".")

					to_print = what 

				else :
					to_print += " " + what 
				
				prev_who = who 
		# last line 
		total.append(to_print)
		self.toksen = total 
		return total 
			

