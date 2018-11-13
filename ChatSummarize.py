from coined_word import coinedword as CW_conv 
from token_sentence_converter import Toksen_converter as TS_conv
import os
from hanspell import spell_checker as sc

from lexrankr import LexRank

class ChatSummarizer:

	preprocessed = None
	summaries = None

	def __init__(self, input_sentences):
		self.cw = CW_conv.Coinedword(file="./coined_word/coinedword_dic.txt") 
		self.ts = TS_conv.Toksen(input_sentences)

	def preprocess(self):

		print("connected as sentences ")

		connected_lines = self.ts.as_it_is()
		cw_lines = [self.cw.convert(x) for x in connected_lines]
		print("spell checking ")
		sc_lines = [sc.check(x) for x in cw_lines]
		
		sc_lines = [x.checked for x in sc_lines]
		self.preprocessed = sc_lines 
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
		print(len(self.preprocessed), self.preprocessed)
		lexrank.summarize(" ".join(self.preprocessed))
		lexrank_sentences = [x.text for x in lexrank.sentences]
		ts.produce_mapping(from_lexrank=lexrank_sentences)
		
		print(len(lexrank.sentences))

		scores = lexrank.sentence_score_pair()  

		# print(len(scores))
		# print(len(self.ts.chat_to_sentence_mapping))
		# print(scores)
		threshold = 1/int(scores[-1][0]+1)




		

