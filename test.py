from pytorch_pretrained import BertModel, BertTokenizer
import torch
import torch.nn as nn
PAD, CLS = '[PAD]', '[CLS]'
pad_size=32
text=[['[S]你好[NEXT]',"[MASK]我的天哪","哈哈","我的天哪","哈哈"],['嘿嘿嘿',"我的天哪","哈哈","我的天哪","哈哈"],['你',"我的天哪","哈哈","我的天哪","哈哈"]]
label=[1,2,3]
new_tokens = ['[CLS]', '[NEXT]']

tokenizer = BertTokenizer.from_pretrained('./bert_pretrain')
contents=[]
for onebatch in text:
    token_idsList=[]
    maskList=[]
    for content in onebatch:
        token = tokenizer.tokenize(content)
        print(token)
        token = [CLS] + token
        seq_len = len(token)
        mask = []
        token_ids = tokenizer.convert_tokens_to_ids(token)
        print(token_ids)

        if pad_size:
            if len(token) < pad_size:
                mask = [1] * len(token_ids) + [0] * (pad_size - len(token))
                token_ids += ([0] * (pad_size - len(token)))
            else:
                mask = [1] * pad_size
                token_ids = token_ids[:pad_size]
                seq_len = pad_size
        token_idsList.append(token_ids)
        maskList.append(mask)
    contents.append((token_idsList, 1, seq_len, maskList))

bert=BertModel.from_pretrained('./bert_pretrain')

xLongtensor = torch.LongTensor([_[0] for _ in contents])
maskLongtensor = torch.LongTensor([_[3] for _ in contents])

hidden_size = 768


dropout = 0.1
rnn_hidden = 768
num_layers = 2
lstm = nn.LSTM(hidden_size, rnn_hidden, num_layers,
                            bidirectional=True, batch_first=True, dropout=dropout)
#16x32x768
clsTensors=[]
for x,y in zip(xLongtensor,maskLongtensor):
    context = x
    mask = y
    print(context.shape)
    encoder_out, text_cls = bert(context, attention_mask=mask, output_all_encoded_layers=False)
    text_cls=text_cls.unsqueeze_(0)
    clsTensors.append(text_cls)
print(clsTensors[0].shape)
clsTensors=torch.cat(clsTensors,dim=2)
print(clsTensors.shape)

print(lstm(clsTensors))


#
# def processToken(tokenList):
#     for i in range(len(tokenList)):
#         if i >=len(tokenList):
#             break
#         if tokenList[i]=='[':
#             for j in range(i+1,len(tokenList)):
#                 if tokenList[j]==']':
#                     print(tokenList[i:j+1])
#                     print("".join(tokenList[i:j+1]))
#                     tokenList[i:j+1]=["".join(tokenList[i:j+1])]
#                     print(tokenList)
#                     break
#     return tokenList
#
# processToken(["[","N","E","]","你好","[","S","]"])

# import re
#
# a="[KEY]123[KEY]dsfsfs"
# b = re.findall(r'\[KEY].*?\[KEY]',a)
# print(b)
