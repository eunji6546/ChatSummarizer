from coined_word import coinedword as CW_conv 
from token_sentence_converter import Toksen_converter as TS_conv
import os
import sys 
from hanspell import spell_checker as sc
from mactowin import mactowin
from noise_detector import noise_detec
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
		
		preprocessed = self.preprocessed[:]
		preprocessed = [x.strip().strip(".").strip() for x in preprocessed]
		lex_idx = 0 
		skip_amount = 0
		jump = 0 
		for ts_sentence in self.ts.chat_to_sentence_mapping:
			ts_idx, chat_idxs, sentence = ts_sentence
			
			if lex_idx >= len(scores): break
			
			if len(sentence.strip()) == 0 :
				jump += 1
			else :
				if preprocessed[lex_idx + skip_amount] != scores[lex_idx][1] :
					skip_amount += 1 
				else :					
					scores[lex_idx] = list(scores[lex_idx])
					scores[lex_idx][0] = lex_idx + jump + skip_amount
					scores[lex_idx].append(chat_idxs)
					lex_idx += 1; 
		self.highlight_lexrank = scores[:]
		print("highlight result")
		return_list = self._map_to_chat(self.highlight_lexrank)
		for chat in return_list :
			if chat[0] == 1 : 
				print(chat)
		return return_list


	def _map_to_chat (self, scores):
		#----
		threshold = 1 / int(scores[-1][0] + 1)
		high_scores=[]

		for line in scores :
			if line[2] > threshold :
				high_scores.append(line[2])
		threshold = sum(high_scores) / len(high_scores)
		
		more_high = [] 
		for s in high_scores :
			if s > threshold :
				more_high.append(s)
		threshold = sum(more_high) / len(more_high)
		
		highlighted_lexsentences = [] 


		return_chat_idx = [] 
		for line in scores :
			if line[2] > threshold :
				highlighted_lexsentences.append(line)
				return_chat_idx += line[-1]

		i = 0
		return_chat = [] 
		noiseDetec = noise_detec.NoiseDetector()
		for line in self.ts.input:
			if i in return_chat_idx:
				nd = noiseDetec.remove(line.split("]")[2].strip())
				if len(nd) == 0:
					return_chat.append([0, line])
				else:
					return_chat.append([1, line])
			else :
				return_chat.append([0, line])
			i += 1 
		self.highlight = return_chat[:]

		return return_chat
		

	def include_additional (self, threshold=0.5):

		print("additionals : ")
		lexrank = LexRank()

		input_seq = [x[1]+"." for x in self.ts.with_reaction]
		#?? input_seq = [x.strip().strip(".").strip() for x in input_seq]
		
		lexrank.summarize(" ".join(input_seq))
		lexrank_sentences = [x.text for x in lexrank.sentences]

		scores = lexrank.sentence_score_pair()  

		preprocessed = self.preprocessed[:]
		preprocessed = [x.strip().strip(".").strip() for x in preprocessed]
		
		lex_idx = 0 
		skip_amount = 0
		jump = 0 


		# from scores to reaction index mapping (change scores' index to reactions)
		
		for ts_sentence in self.ts.with_reaction:
			ts_idx, sentence = ts_sentence
			sentence = sentence.strip(" ")
			# print (ts_sentence, scores[lex_idx])
			
			if lex_idx >= len(scores): break
			
			if len(sentence.strip()) == 0 or len(sentence.split(" ")) <2:
				jump += 1
			else :
				if sentence != scores[lex_idx][1] :
					skip_amount += 1 
				else :					
					scores[lex_idx] = list(scores[lex_idx])
					scores[lex_idx][0] = lex_idx + jump + skip_amount
					
					lex_idx += 1; 

		self.additional_lexrank = scores[:]
		additional_dict = {} 
		for line in self.additional_lexrank:
			i, sentence, score = line 
			additional_dict[i] = score 

		idx = 0 
		for line in self.highlight_lexrank:
			i, sentence, score, chat_idxs = line 
			if i in additional_dict.keys() :
				self.highlight_lexrank[idx][2] += additional_dict[i]
				self.highlight_lexrank[idx][2] = self.highlight_lexrank[idx][2] * 0.5

			idx += 1 

		print ("new highlights with reaction")
		return_list = self._map_to_chat (self.highlight_lexrank)
		for chat in return_list :
			if chat[0] == 1 : 
				print(chat)
		
		return return_list

