from coined_word import coinedword as CW_conv 
from token_sentence_converter import Toksen_converter as TS_conv
import os
from hanspell import spell_checker as sc

from lexrankr import LexRank

class ChatSummarizer:

	datapath = "./sample_data/"

	def __init__(self, input_sentences):
		self.fname = fname 
		self.cw = CW_conv.Coinedword(file="./coined_word/coinedword_dic.txt") 
		self.ts = TS_conv.Toksen(input_sentences)

	def preprocess(self):

		print ("running file:%s", self.fname)
		print("connected as sentences ")

		connected_lines = self.ts.as_it_is()
		cw_lines = [self.cw.convert(x) for x in connected_lines]
		print("spell checking ")
		sc_lines = [sc.check(x) for x in cw_lines]
		
		sc_lines = [x.checked for x in sc_lines]

		print("doing lexrank ")
	
	def summarize(self, n_summary)
		print("summarize in %d sentences" %n_summary)
		lexrank = LexRank()
		lexrank.summarize(" ".join(sc_lines))
		summaries = lexrank.probe(n_summary)  # `num_summaries` can be `None` (using auto-detected topics)
		for summary in summaries:
			print(summary)
		return summaries

	def highlight(self, threshold=0.5)
		print("highlight : return list of chats and scores ")

		

