from coined_word import coinedword as CW_conv 
from token_sentence_converter import Toksen_converter as TS_conv
import os
import sys 
# from hanspell import spell_checker as sc
import spell_check as sc
from mactowin import mactowin
from noise_detector import noise_detec
sys.path.insert(0,os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from lexrankr import LexRank
import scipy.stats


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
		#self.connected_lines = self.ts.as_it_is()
		self.ts.reaction_mapping()
		self.connected_lines = self.ts.by_time_connect()
		self.cw_lines = [self.cw.convert(x) for x in self.connected_lines]
		print("spell checking ")
		self.sc_lines = [sc.check(x) for x in self.cw_lines]
		# self.sc_lines = [x.checked for x in self.sc_lines]
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
			if line[2] >= threshold :
				high_scores.append(line[2])
		threshold = sum(high_scores) / len(high_scores)
		
		# more_high = [] 
		# for s in high_scores :
		# 	if s > threshold :
		# 		more_high.append(s)
		# threshold = sum(more_high) / len(more_high)
		
		highlighted_lexsentences = [] 

		return_chat_idx = [] 
		for line in scores :
			if line[2] >= threshold :
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

	def include_additional_frequency(self, threshold = 0.05):
		total_noise_num =0
		total_noise_num_by_person = []
		total_noise_num_by_noise = []

		# print(self.ts.sentence_reaction_mapping)
		# print(self.ts.person_reaction_frequency)

		for i in range(len(self.ts.person_reaction_frequency)):
			sum1 = 0
			if i == 0:
				total_noise_num_by_noise = self.ts.person_reaction_frequency[i][1]
			for j in range(len(self.ts.person_reaction_frequency[i][1])):
				if(i>0):
					total_noise_num_by_noise[j]+=self.ts.person_reaction_frequency[i][1][j]
				sum1+=self.ts.person_reaction_frequency[i][1][j]
			
			total_noise_num_by_person.append(sum1)
			total_noise_num +=sum1

		#value that the person uses reaction often
		#if it is high, then the score should be less because the person usually use reaction
		#total_noise_num_by_person[i]/total_noise_num
		
		#value the people use the reaction often
		#if it two low, then it would be just noise thing.

		usable_noise = []
		result = [0] * len(self.ts.sentence_reaction_mapping)
		for i in range(len(total_noise_num_by_noise)):
			if total_noise_num_by_noise[i]/total_noise_num >= threshold:
				usable_noise.append(i)
		
		for i in range(len(self.ts.sentence_reaction_mapping)):
			current = scipy.stats.norm(i-1,1.5)

			person_index = 0
			for l in range(len(self.ts.person_reaction_frequency)):
				if self.ts.sentence_reaction_mapping[i][1] == self.ts.person_reaction_frequency[l][0]:
					person_index = l
					break
			for j in range(len(usable_noise)):
				for k in range(len(result)):
					if(total_noise_num_by_person[person_index] ==0):
						continue
					result[k]+=	current.pdf(k) * self.ts.sentence_reaction_mapping[i][2][usable_noise[j]] / total_noise_num_by_person[person_index]


		sum1 = 0
		for i in range(len(result)):
			sum1 += result[i]

		for i in range(len(result)):
			result[i] = result[i]/sum1


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

		for i in range(len(result)):
			for j in range(len(scores)):
				if i in scores[j][3]:
					scores[j][2]+=result[i]*0.2
					break
		for j in range(len(scores)):
			scores[j][2] = scores[j][2]/1.2
		print(scores)

		self.highlight_lexrank = scores[:]
		print("highlight result")
		return_list = self._map_to_chat(self.highlight_lexrank)
		for chat in return_list :
			if chat[0] == 1 : 
				print(chat)
		return return_list


		# lexrank = LexRank()
		
		# lexrank.summarize(" ".join(self.preprocessed))
		# lexrank_sentences = [x.text for x in lexrank.sentences]

		# scores = lexrank.sentence_score_pair()  
		
		# self.preprocessed = [x.strip().strip(".").strip() for x in self.preprocessed]
		# # print(self.preprocessed, len(self.preprocessed))
		# # print(self.ts.chat_to_sentence_mapping, len(self.ts.chat_to_sentence_mapping))
		# lex_idx = 0 
		# skip_amount=0
		# jump = 0 
		# for ts_sentence in self.ts.chat_to_sentence_mapping:
		# 	ts_idx, chat_idxs, sentence = ts_sentence
		# 	# print ("from ts", ts_idx, ts_sentence )
		# 	# print ("from output", lex_idx+skip_amount, self.preprocessed[lex_idx+skip_amount])
		# 	# print ("from scores", lex_idx, scores[lex_idx])
			
		# 	if lex_idx >= len(scores): break
			
		# 	if len(sentence.strip()) == 0 :
		# 		jump +=1
		# 	else :
		# 		if self.preprocessed[lex_idx+skip_amount] != scores[lex_idx][1] : 
		# 			# print ("not same")
		# 			#jump += 1 
		# 			skip_amount += 1 
		# 		else :
		# 			# print("same same ")
					
		# 			scores[lex_idx] = list(scores[lex_idx])
		# 			scores[lex_idx][0] = lex_idx + jump + skip_amount
		# 			scores[lex_idx].append(chat_idxs)
		# 			lex_idx +=1; 

		# print(scores)
		# print(result)
		# for i in range(len(result)):
		# 	for j in range(len(scores)):
		# 		if i in scores[j][3]:
		# 			scores[j][2]+=result[i]*0.5
		# 			break
		# for j in range(len(scores)):
		# 	scores[j][2] = scores[j][2]/1.5
		# print(scores)


		# #----
		# threshold = 1/int(scores[-1][0]+1)
		# high_scores=[]

		# for line in scores :
		# 	if line[2] > threshold :
		# 		high_scores.append(line[2])
		# threshold = sum(high_scores)/len(high_scores)


		# highlighted_lexsentences = [] 

		# return_chat_idx = [] 
		# for line in scores :
		# 	if line[2] > threshold :
		# 		highlighted_lexsentences.append(line)
		# 		return_chat_idx += line[-1]

		# i = 0 

		# for line in highlighted_lexsentences :
		# 	print ("%d th highlight", i )
		# 	i+=1
		# 	for idx in line[-1]:
		# 		print(self.ts.input[idx])
		# # print("----")
		# 	print ("-----")

		# i=0
		# return_chat = [] 
		# for line in self.ts.input:
		# 	if i in return_chat_idx:
		# 		return_chat.append([1, line])
		# 	else :
		# 		return_chat.append([0, line])
		# 	i += 1 
		# del(lexrank)
		# return return_chat

