import os

import mindspore
from mindspore.dataset import text, GeneratorDataset, transforms
from mindspore import nn, context

from mindnlp.engine import Trainer, Evaluator
from mindnlp.engine.callbacks import CheckpointCallback, BestModelCallback
from mindnlp.metrics import Accuracy

from bert import Model,Config
from getDataset import returnDataset

dataset_train = returnDataset("./CLASSCon/data/train.txt")
dataset_val = returnDataset("./CLASSCon/data/dev.txt")
dataset_test = returnDataset("./CLASSCon/data/test.txt")

print(dataset_train)


# set bert config and define parameters for training
config=Config("ClassCon")
model = Model(config)

loss = nn.CrossEntropyLoss()
optimizer = nn.Adam(model.trainable_params(), learning_rate=2e-5)

metric = Accuracy()

# define callbacks to save checkpoints
ckpoint_cb = CheckpointCallback(save_path='checkpoint', ckpt_name='bert_emotect', epochs=1, keep_checkpoint_max=2)
best_model_cb = BestModelCallback(save_path='checkpoint', ckpt_name='bert_emotect_best', auto_load=True)

trainer = Trainer(network=model, train_dataset=dataset_train,
                  eval_dataset=dataset_val, metrics=metric,
                  epochs=5, loss_fn=loss, optimizer=optimizer, callbacks=[ckpoint_cb, best_model_cb],
                  jit=True)

trainer.run("label")