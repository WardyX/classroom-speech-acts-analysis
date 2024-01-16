# coding: UTF-8
import torch
import torch.nn as nn
import torch.nn.functional as F
from pytorch_pretrained import BertModel,BertTokenizer


class Config(object):

    """配置参数"""
    def __init__(self, dataset):
        self.model_name = 'bert_Concat'
        self.train_path = dataset + '/data/train.txt'                                # 训练集
        self.dev_path = dataset + '/data/dev.txt'                                    # 验证集
        self.test_path = dataset + '/data/test.txt'                                  # 测试集
        self.class_list = [x.strip() for x in open(
            dataset + '/data/class.txt',encoding='utf-8').readlines()]                                # 类别名单
        self.save_path = dataset + '/saved_dict/' + self.model_name + '.ckpt'        # 模型训练结果
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')   # 设备

        self.require_improvement = 1000                                 # 若超过1000batch效果还没提升，则提前结束训练
        self.num_classes = len(self.class_list)                         # 类别数
        self.num_epochs = 12                                             # epoch数
        self.batch_size = 16                                           # mini-batch大小
        self.pad_size = 32                                              # 每句话处理成的长度(短填长切)
        self.learning_rate = 5e-5                                       # 学习率
        self.bert_path = './bert_pretrain'
        self.tokenizer = BertTokenizer.from_pretrained(self.bert_path)
        self.hidden_size = 3840
        self.filter_sizes = (2, 3, 4)                                   # 卷积核尺寸
        self.num_filters = 256                                          # 卷积核数量(channels数)
        self.dropout = 0.1
        self.rnn_hidden = 768
        self.num_layers = 2


class Model(nn.Module):

    def __init__(self, config):
        super(Model, self).__init__()
        self.bert = BertModel.from_pretrained(config.bert_path)
        for param in self.bert.parameters():
            param.requires_grad = True
        self.fc2=nn.Linear(config.hidden_size, 768)
        self.fc = nn.Linear(768, config.num_classes)

    def forward(self, x):
        xLongtensor = x[0]  # 输入的句子
        maskLongtensor = x[2]  # 对padding部分进行mask，和句子一个size，padding部分用0表示，如：[1, 1, 1, 1, 0, 0]
        # print("context:",context)
        # print("mask:",mask)
        clsTensors = []
        for x, y in zip(xLongtensor,maskLongtensor):
            context = x
            mask = y
            encoder_out, text_cls = self.bert(context, attention_mask=mask, output_all_encoded_layers=False)
            text_cls=text_cls.reshape(1,3840)
            clsTensors.append(text_cls)
        clsTensors = nn.Parameter(torch.cat(clsTensors, dim=0),requires_grad=True)
        #print("encoder_out:",encoder_out.shape)
        #print("text_cls:",clsTensors.shape)
        f_out=self.fc2(clsTensors)
        out = self.fc(f_out)
        return out