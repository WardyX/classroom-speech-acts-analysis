import mindspore.dataset as ds
from tqdm import tqdm
from pytorch_pretrained import BertModel, BertTokenizer
import numpy as np
import os

import mindspore
from mindspore.dataset import text, GeneratorDataset, transforms
from mindspore import nn, context

from mindnlp.transforms import PadTransform

from mindnlp.engine import Trainer, Evaluator
from mindnlp.engine.callbacks import CheckpointCallback, BestModelCallback
from mindnlp.metrics import Accuracy
def processToken(tokenList):
    for i in range(len(tokenList)):
        if i >=len(tokenList):
            break
        if tokenList[i]=='[':
            for j in range(i+1,len(tokenList)):
                if tokenList[j]==']':
                    tokenList[i:j+1]=["".join(tokenList[i:j+1])]
                    break
    return tokenList
class IterableDataset():
    def __init__(self, path):
        '''init the class object to hold the data'''
        self.path = path
        self.pad_size=32
        self.PAD, self.CLS = '[PAD]', '[CLS]'  # padding符号, bert中综合信息符号
        self.bert_path='./bert_pretrain'
        self.tokenizer = BertTokenizer.from_pretrained(self.bert_path)
        self.content=self.load_dataset()
        self.content=np.asarray(self.content)
        for i in range(len(self.content)):
            self.content[i][0]=np.asarray(self.content[i][0])
            self.content[i][3] = np.asarray(self.content[i][3])
        self._labels=self.content
    def __getitem__(self, index):
        return self.content[index][0],self.content[index][1]
    def __len__(self):
        return len(self.content)

    def load_dataset(self):
        contents = []
        with open(self.path, 'r', encoding='GBK') as f:
            for line in tqdm(f):
                lin = line.strip()
                if not lin:
                    continue
                content, label = lin.split('\t')
                # content=re.findall(r'\[KEY].*?\[KEY]',content)
                # content=content[0]
                token = self.tokenizer.tokenize(content)
                token = processToken(token)
                token = [self.CLS] + token
                seq_len = len(token)
                mask = []
                token_ids = self.tokenizer.convert_tokens_to_ids(token)
                if self.pad_size:
                    if len(token) < self.pad_size:
                        mask = [1] * len(token_ids) + [0] * (self.pad_size - len(token))
                        token_ids += ([0] * (self.pad_size - len(token)))
                    else:
                        mask = [1] * self.pad_size
                        token_ids = token_ids[:self.pad_size]
                        seq_len = self.pad_size
                contents.append((token_ids, int(label), seq_len, mask))
        return contents


def returnDataset(path):
    loader = IterableDataset(path)
    dataset = ds.GeneratorDataset(source=loader, column_names=["data","label"])
    dataset.batch(32)
    type_cast_op = transforms.TypeCast(mindspore.int32)
    type_cast_te = transforms.TypeCast(mindspore.float32)
    # dataset = dataset.map(operations=[type_cast_op], input_columns="label")
    # dataset = dataset.map(operations=[type_cast_te], input_columns="data")
    # dataset = dataset.map(operations=[type_cast_te], input_columns="mask")
    return dataset

if __name__ == '__main__':
    dataset_train = returnDataset("./CLASSCon/data/train.txt")
    dataset_val = returnDataset("./CLASSCon/data/dev.txt")
    dataset_test = returnDataset("./CLASSCon/data/test.txt")
    print(dataset_train.get_batch_size())
    for data in dataset_train.create_dict_iterator():
        print(data)


