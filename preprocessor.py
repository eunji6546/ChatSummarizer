from coined_word import coinedword as CW_conv 
from token_sentence_converter import Toksen_converter as TS_conv
import os
from hanspell import spell_checker as sc

from lexrankr import LexRank

if __name__=='__main__':
	
	cw = CW_conv.Coinedword(file="./coined_word/coinedword_dic.txt") 

	datapath = "./sample_data/"
	for fname in os.listdir(datapath):
		if fname.startswith("chat"):
			print(fname)
			ts = TS_conv.Toksen(datapath + fname)
			connected_lines = ts.as_it_is()
			print("connected as sentences ")
			cw_lines = [cw.convert(x) for x in connected_lines]
			print("replaced")
			# Noise Dector should be added 
			# Spelling Checker 
			sc_lines = [sc.check(x) for x in cw_lines]
			print("spell_checked")
			# KoNLPy
			# LexRank Algorithm 
			sc_lines = [x.checked for x in sc_lines]

			print(sc_lines)
			
			lexrank = LexRank()
			lexrank.summarize(" ".join(sc_lines))
			summaries = lexrank.probe(3)  # `num_summaries` can be `None` (using auto-detected topics)
			for summary in summaries:
			    print(summary)
			break

