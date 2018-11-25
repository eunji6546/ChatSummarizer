import pandas as pd
from ChatSummarize import ChatSummarizer

num_data = 11
num_chat = 5
accuracy = [0] * num_chat
precision = [0] * num_chat
recall = [0] * num_chat
highlight = []

for i in range(1, num_data + 1):
    for j in range(num_chat):
        data = pd.read_excel("./test_data/test_data_" + str(i) + ".xlsx", sheet_name="Sheet"+str(j + 1))

        if i == 1:
            chat = "\n".join(list(data.chat))
            chatSummarizer = ChatSummarizer(chat)
            chatSummarizer.preprocess()
            highlight.append(chatSummarizer.highlight())

        # True positive/negative, False positive/negative
        tp = 0
        tn = 0
        fp = 0
        fn = 0

        for test, hl in zip(data.highlight, highlight[j]):
            if test == hl[0]:
                if test == 0:
                    tn += 1
                else:
                    tp += 1
            else:
                if test == 0:
                    fp += 1
                else:
                    fn += 1

        accuracy[j] += (tn + tp) / (tp + tn + fp + fn)
        precision[j] += tp / (tp + fp)
        recall[j] += tp / (tp + fn)
    
accuracy = [(x / num_data) for x in accuracy]
precision = [(x / num_data) for x in precision]
recall = [(x / num_data) for x in recall]

print("Accuracy: ", end="")
print(accuracy)
print("Precision: ", end="")
print(precision)
print("Recall: ", end="")
print(recall)