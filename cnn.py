#coding=utf-8
from __future__ import absolute_import
from __future__ import print_function
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.advanced_activations import PReLU
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.utils import np_utils, generic_utils
from mnist_load_data import load_data
import random
# 加载数据
data, label = load_data(path="./data/mnist.pkl.gz")[0]
val_data,val_label=load_data(path="./data/mnist.pkl.gz")[1]
test_data,test_label=load_data(path="./data/mnist.pkl.gz")[2]
data=data.reshape(data.shape[0],1,28,28)
test_data=test_data.reshape(test_data.shape[0],1,28,28)
test_label=np_utils.to_categorical(test_label,10)
val_data=val_data.reshape(val_data.shape[0],1,28,28)
val_label=np_utils.to_categorical(val_label,10)
# 打乱数据
index = [i for i in range(len(data))]
random.shuffle(index)
data = data[index]
label = label[index]
print(data.shape[0], ' samples')

# label为0~9共10个类别，keras要求格式为binary class matrices,转化一下，直接调用keras提供的这个函数
label = np_utils.to_categorical(label, 10)

###############
# 开始建立CNN模型
###############

# 生成一个model
model = Sequential()

# 第一个卷积层，4个卷积核，每个卷积核大小5*5。1表示输入的图片的通道,灰度图为1通道。
# border_mode可以是valid或者full，具体看这里说明：http://deeplearning.net/software/theano/library/tensor/nnet/conv.html#theano.tensor.nnet.conv.conv2d
# 激活函数用tanh
# 你还可以在model.add(Activation('tanh'))后加上dropout的技巧: model.add(Dropout(0.5))
model.add(Convolution2D(4, 5, 5, border_mode='valid',dim_ordering="th",input_shape=(1,28,28)))
model.add(Activation('tanh'))

# 第二个卷积层，8个卷积核，每个卷积核大小3*3。4表示输入的特征图个数，等于上一层的卷积核个数
# 激活函数用tanh
# 采用maxpooling，poolsize为(2,2)
model.add(Convolution2D(8, 3, 3, border_mode='valid',dim_ordering="th"))
model.add(Activation('tanh'))
model.add(MaxPooling2D(pool_size=(2, 2),dim_ordering="th"))

# 第三个卷积层，16个卷积核，每个卷积核大小3*3
# 激活函数用tanh
# 采用maxpooling，poolsize为(2,2)
model.add(Convolution2D(16,  3, 3, border_mode='valid',dim_ordering="th"))
model.add(Activation('tanh'))
model.add(MaxPooling2D(pool_size=(2, 2),dim_ordering="th"))

# 全连接层，先将前一层输出的二维特征图flatten为一维的。
# Dense就是隐藏层。16就是上一层输出的特征图个数。4是根据每个卷积层计算出来的：(28-5+1)得到24,(24-3+1)/2得到11，(11-3+1)/2得到4
# 全连接有128个神经元节点,初始化方式为normal
model.add(Flatten())
model.add(Dense(128, init='normal'))
model.add(Activation('tanh'))

# Softmax分类，输出是10类别
model.add(Dense(10, init='normal'))
model.add(Activation('softmax'))


#############
# 开始训练模型
##############
# 使用SGD + momentum
# model.compile里的参数loss就是损失函数(目标函数)
sgd = SGD(lr=0.05, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd ,class_mode="categorical")

# 调用fit方法，就是一个训练过程. 训练的epoch数设为10，batch_size为100．
# 数据经过随机打乱shuffle=True。verbose=1，训练过程中输出的信息，0、1、2三种方式都可以，无关紧要。show_accuracy=True，训练时每一个epoch都输出accuracy。
# validation_split=0.2，将20%的数据作为验证集。
model.fit(data, label, batch_size=100, nb_epoch=10 ,shuffle=True,verbose=1 ,validation_data=(val_data,val_label))

score=model.evaluate(test_data,test_label,batch_size=100,verbose=1)
print(score)
