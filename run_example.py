import ChatSummarize as ChatSum

if __name__=="__main__":
	for i in range(22):
		if i == 0 or i == 1 or i == 4:
			continue
		with open("./sample_data/chat%d.txt" %i, 'r', encoding='utf-8-sig')as f:
			lines = f.readlines()

		input_sentences = "".join(lines)
		#input_sentences = "[이주희] [2018.10.26 19:28] 밷?.. 있나염\n[노희광] [2018.10.26 19:28] 허은지\n[이주희] [2018.10.26 19:30] (이모티콘) \n[노희광] [2018.10.26 19:33] 아니면 이주희\n[이주희] [2018.10.26 19:37] (이모티콘) \n[김영은] [2018.10.26 19:46] 밷\n[김영은] [2018.10.26 19:46] 나좋아\n[김영은] [2018.10.26 19:46] 나퇴근했어\n[김영은] [2018.10.26 19:46] ㅋㅋㅋㅋㅋㅋㅋ\n[김영은] [2018.10.26 20:05] 이주희\n[김영은] [2018.10.26 20:05] 치는겨마는겨\n[허은지] [2018.10.26 20:06] 비오는날엔 찾지말아줘\n[허은지] [2018.10.26 20:07] (이모티콘) \n[이주희] [2018.10.26 20:10] ㅋㅋㅋㅋㅋ 사람이 안모이니.... 흙\n[이주희] [2018.10.26 20:10] 내일 일찍 만나서 치쟝 언닝"
		runner = ChatSum.ChatSummarizer(input_sentences)
		runner.preprocess()
		print("preprocess done.")
		#runner.summarize(4)
		runner.highlight()
		del (runner)

		