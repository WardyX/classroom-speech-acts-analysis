import matplotlib.pyplot as plt
import numpy as np

def draw():
    # confusion = np.array(([ 18,   3  , 1  ,14  , 2 ,  0  , 0 ,  0],
    #                     [  0 ,188  , 2  , 9  , 2  , 1  , 0  , 4],
    #                     [  3  , 6 , 73  ,18  , 0  , 0  , 0 ,  1],
    #                     [ 11  ,11 , 17 ,264   ,8   ,3  , 0   ,1],
    #                     [  4  , 2 ,  2 ,  4 ,111 ,  0   ,0 , 17],
    #                     [  0  , 1 ,  0 ,  0  , 7 ,  0 ,  0 ,  1],
    #                     [  1 ,  0 ,  0 ,  0 ,  0  , 0 ,  0 ,  2],
    #                     [  1 ,  0 ,  1 ,  4 , 12  , 0  , 0 ,174]))

    # confusion = np.array(([  3 ,  7  , 2 , 23  , 3  , 0   ,0  , 0],
    #                     [  1 ,169   ,4  ,27   ,1 ,  0 ,  0  , 4],
    #                     [  2 ,  6  ,44 , 32   ,3  , 0  , 0 , 14],
    #                     [  2  ,27 , 13, 227 , 25  , 0  , 0 , 21],
    #                     [  1 , 11 ,  4  ,44  ,61 ,  0 ,  0  ,19],
    #                     [  0 ,  0 ,  0  , 4  , 2  , 2 ,  0  , 1],
    #                     [  0  , 0   ,0  , 3  , 0 ,  0 ,  0 ,  0],
    #                     [  0 ,  5  , 8 , 32  , 7  , 0 ,  0, 140]))
    confusion = np.array(([  0  , 8  ,19 , 20 ,  0  , 0  , 0 , 10],
                        [  0 ,193  , 5  , 9  , 0  , 0  , 0 ,  1],
                        [  0  , 3 , 47 , 31 ,  0  , 0  , 0 , 11],
                        [  0 , 24 , 20, 254 ,  3 ,  0 ,  0 , 11],
                         [  0  , 2 ,  0 , 17 , 31  , 0 ,  0 , 71],
                        [  0 ,  0 ,  0  , 1  , 0 ,  0  , 0  , 2],
                        [  0 ,  0  , 0  , 1  , 0  , 0  , 0 ,  1],
                        [  0  , 6 ,  0  , 9  , 5 ,  0  , 0 ,189]))
#
#     ([[  3  10   5  21   3   0   0  11]
#  [  1 150   2  41   6   0   0   5]
#  [  0   9  11  33   3   0   0  21]
#  [  0  34   3 257  20   0   0  28]
#  [  0   4   2  54  49   0   0  20]
#  [  0   0   0   3   2   0   0   0]
#  [  0   0   0   1   0   0   0   2]
#  [  0  10   0  30   8   0   0 142]]
# )

    # 热度图，后面是指定的颜色块，可设置其他的不同颜色
    plt.imshow(confusion, cmap=plt.cm.Blues)
    # ticks 坐标轴的坐标点
    # label 坐标轴标签说明
    indices = range(len(confusion))
    # 第一个是迭代对象，表示坐标的显示顺序，第二个参数是坐标轴显示列表
    # plt.xticks(indices, [0, 1, 2])
    # plt.yticks(indices, [0, 1, 2])
    plt.xticks(indices, ["教师评价或回应学生","教师提问","教师指令","教师讲授","学生被动应答","学生创造应答","学生主动\n提问或发言","沉寂杂音或讨论"])
    plt.yticks(indices, ["教师评价或回应学生","教师提问","教师指令","教师讲授","学生被动应答","学生创造应答","学生主动\n提问或发言","沉寂杂音或讨论"])

    plt.colorbar()

    plt.xlabel('预测值')
    plt.ylabel('真实值')
    plt.title('混淆矩阵')

    # plt.rcParams两行是用于解决标签不能显示汉字的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 显示数据
    for first_index in range(len(confusion)):  # 第几行
        for second_index in range(len(confusion[first_index])):  # 第几列
            plt.text(first_index, second_index, confusion[first_index][second_index])
    # 在matlab里面可以对矩阵直接imagesc(confusion)
    # 显示
    plt.show()

draw()

