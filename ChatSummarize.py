from coined_word import coinedword as CW_conv 
from token_sentence_converter import Toksen_converter as TS_conv
import os
import sys 
from hanspell import spell_checker as sc
from mactowin import mactowin
sys.path.insert(0,os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from lexrankr import LexRank

class ChatSummarizer:

	preprocessed = None
	summaries = None

	def __init__(self, input_sentences):

		self.cw = CW_conv.Coinedword(file="../coined_word/coinedword_dic.txt") 
	
		print("windows format change to mac format")
		
		self.input_sentences = mactowin.MactoWin().convert(input_sentences)
		

	def preprocess(self):

		print("connected as sentences ")
		self.ts = TS_conv.Toksen(self.input_sentences)
		self.connected_lines = self.ts.as_it_is()
		# self.connected_lines = self.ts.by_time_connect()
		self.cw_lines = [self.cw.convert(x) for x in self.connected_lines]
		print("spell checking ")
		self.sc_lines = [sc.check(x) for x in self.cw_lines]
		
		self.sc_lines = [x.checked for x in self.sc_lines]
		self.preprocessed = self.sc_lines 
		print("doing lexrank ")
	
	def summarize(self, n_summary):
		print("summarize in %d sentences" %n_summary)
		lexrank = LexRank()
		lexrank.summarize(" ".join(self.preprocessed))
		summaries = lexrank.probe(n_summary)  
		# `num_summaries` can be `None` (using auto-detected topics)

		for summary in summaries:
			print(summary)
		self.summaries = summaries
		return summaries

	def highlight(self, threshold=0.5):
		print("highlight : return list of chats and scores ")

		lexrank = LexRank()
		
		lexrank.summarize(" ".join(self.preprocessed))
		lexrank_sentences = [x.text for x in lexrank.sentences]

		scores = lexrank.sentence_score_pair()  
		
		self.preprocessed = [x.strip().strip(".").strip() for x in self.preprocessed]
		# print(self.preprocessed, len(self.preprocessed))
		# print(self.ts.chat_to_sentence_mapping, len(self.ts.chat_to_sentence_mapping))
		lex_idx = 0 
		skip_amount=0
		jump = 0 
		for ts_sentence in self.ts.chat_to_sentence_mapping:
			ts_idx, chat_idxs, sentence = ts_sentence
			# print ("from ts", ts_idx, ts_sentence )
			# print ("from output", lex_idx+skip_amount, self.preprocessed[lex_idx+skip_amount])
			# print ("from scores", lex_idx, scores[lex_idx])
			
			if lex_idx >= len(scores): break
			
			if len(sentence.strip()) == 0 :
				jump +=1
			else :
				if self.preprocessed[lex_idx+skip_amount] != scores[lex_idx][1] : 
					# print ("not same")
					#jump += 1 
					skip_amount += 1 
				else :
					# print("same same ")
					
					scores[lex_idx] = list(scores[lex_idx])
					scores[lex_idx][0] = lex_idx + jump  + skip_amount
					scores[lex_idx].append(chat_idxs)
					lex_idx +=1; 


		#----
		threshold = 1/int(scores[-1][0]+1)
		high_scores=[]

		for line in scores :
			if line[2] > threshold :
				high_scores.append(line[2])
		threshold = sum(high_scores)/len(high_scores)


		highlighted_lexsentences = [] 

		return_chat_idx = [] 
		for line in scores :
			if line[2] > threshold :
				highlighted_lexsentences.append(line)
				return_chat_idx += line[-1]

		i = 0 

		# for line in highlighted_lexsentences :
		# 	# print ("%d th highlight", i )
		# 	i+=1
		# 	for idx in line[-1]:
		# 		print(self.ts.input[idx])
		# # print("----")
		# print ("-----")

		i=0
		return_chat = [] 
		for line in self.ts.input:
			if i in return_chat_idx:
				return_chat.append([1, line])
			else :
				return_chat.append([0, line])
			i += 1 
		del(lexrank)
		return return_chat
		

	def include_additional (self, threshold=0.5):

		print("highlight : return list of chats and scores ")
		lexrank = LexRank()
		print (self.ts.chat_to_sentence_and_reaction_mapping)
		input_seq = [x[1]+"." for x in self.ts.chat_to_sentence_and_reaction_mapping]
		
		lexrank.summarize(" ".join(input_seq))
		lexrank_sentences = [x.text for x in lexrank.sentences]

		scores = lexrank.sentence_score_pair()  
		
		input_seq = [x.strip().strip(".").strip() for x in input_seq]
		print(scores)
		del(lexrank)

		
		
		
		




		

