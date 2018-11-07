#-*-coding: utf-8
import os 
import sys 
#reload(sys)
#sys.setdefaultencoding('utf-8') 

# python 3 깔린 venv 진입 
# source  /Users/user/py3/bin/activate


def by_person_only(fname) :
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
def by_time_only():
	pass 
def __is_emoticon(chat):
	return "이모티콘" in chat 
def __is_short_reaction (chat):	
	return len(set(chat))<3 
def __remove_kk(chat):
	tok_list = ["ㅋ","ㅎ","?","!",".","ㅠ","@","ㅐ","ㅣ",'~','^',"ㅠ_ㅠ",":)",";"\
	"ㅛ","ㅜ", "ㄹ",":<"]
	new_chat = chat 
	for tok in tok_list:
		new_chat = new_chat.replace(tok,"")
	return new_chat
	

def as_it_is ():
	chat_dict={}
	prev_who = None
	to_print = ""
	total= ""
	# with open(fname,'r', encoding='utf-8') as f :
	# 	for line in f.readlines():
	for line in sys.stdin.readlines() :
		if True: 
			line = line.strip(" ").strip()
			try :
				who, when, what = line.split("]") 
			except:
				# print("ELSE CASE : split ]") 
				continue;
			who = who.strip(" [").strip("] ") 
			when = when.strip(" [").strip("] ") 
			what = what.strip()
			if __is_emoticon (what) or __is_short_reaction (what) : 
				continue 
			
			if prev_who != who :
				#print(to_print)
				if prev_who != None and len(to_print) !=0 :
					if to_print[-1] in ["?","!","."] :
						total += to_print + " "  
					else :
						total += to_print + ". "

				to_print = what 

			else :
				to_print += " " + what 

			
			
			prev_who = who 
	# last line 
	
	print(total)
			
#by_person_only ("../sample_data/chat2.txt")
# for i in range(2, 20, 1):
# 	if i == 4 : continue
# 	as_it_is("../sample_data/chat%d.txt" %i)
as_it_is() 

