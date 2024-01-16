import mindspore as ms
import mindspore.nn as nn
from mindspore import Tensor

from pytorch_pretrained import BertModel, BertTokenizer
import torch
from getDataset import returnDataset
import numpy as np
class Config(object):
    """配置参数"""

    def __init__(self, dataset):
        self.model_name = 'bert'
        self.train_path = dataset + '/data/train.txt'  # 训练集
        self.dev_path = dataset + '/data/dev.txt'  # 验证集
        self.test_path = dataset + '/data/test.txt'  # 测试集
        self.class_list = [x.strip() for x in open(
            dataset + '/data/class.txt', encoding='utf-8').readlines()]  # 类别名单
        self.save_path = dataset + '/saved_dict/' + self.model_name + '.ckpt'  # 模型训练结果

        # self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')   # 设备
        ms.set_context(device_target='CPU', device_id=0)

        self.require_improvement = 1000  # 若超过1000batch效果还没提升，则提前结束训练
        self.num_classes = len(self.class_list)  # 类别数
        self.num_epochs = 12  # epoch数
        self.batch_size = 16  # mini-batch大小
        self.pad_size = 200  # 每句话处理成的长度(短填长切)
        self.learning_rate = 5e-5  # 学习率
        self.bert_path = './bert_pretrain'
        self.tokenizer = BertTokenizer.from_pretrained(self.bert_path)
        self.hidden_size = 768


class Model(nn.Cell):

    def __init__(self, config):
        super().__init__()
        self.bert = BertModel.from_pretrained(config.bert_path)
        for param in self.bert.parameters():
            param.requires_grad = False
        self.fc = nn.Dense(config.hidden_size, config.num_classes)
        self.pad_size = 32
    def construct(self, data):
        context = data  # 输入的句子
        mask = []
        if self.pad_size:
            if len(context) < self.pad_size:
                mask = [1] * len(context) + [0] * (self.pad_size - len(context))
            else:
                mask = [1] * self.pad_size
                seq_len = self.pad_size
        context=context.asnumpy()
        mask=np.array(mask)
        context=torch.from_numpy(context)
        mask = torch.from_numpy(mask)
        context = torch.unsqueeze(context, dim=0)
        mask = torch.unsqueeze(mask, dim=0)
        _, pooled = self.bert(context, attention_mask=mask, output_all_encoded_layers=False)
        pooled=pooled.detach().numpy()
        pooled=Tensor(pooled)
        out = self.fc(pooled)
        # print(out)
        return out

if __name__ == '__main__':
    config=Config("ClassCon")
    model=Model(config)
    dataset_train = returnDataset("./CLASSCon/data/dev.txt")
    for data in dataset_train.create_dict_iterator():
        # print(data)
        print(model(data["data"]))
        break
