import os
import xlrd
from random import shuffle
speaker={1:"[T]",2:"[S]"}
labelKind={0:"教师评价或回应学生",1:"教师提问",2:"教师指令",3:"教师讲授",4:"学生被动型应答",5:"学生创造型应答",6:"学生主动提问或发言",7:"沉寂杂音或讨论"}
def get_filelist(dir):
    Filelist = []
    for home, dirs, files in os.walk(dir):
        for filename in files:
            # 文件名列表，包含完整路径
            Filelist.append(os.path.join(home, filename))
            # # 文件名列表，只包含文件名
            # Filelist.append( filename)
    return Filelist

def read_excel_xls(path):
    li=[]
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    for i in range(0, worksheet.nrows):
        liT=[]
        for j in range(0, worksheet.ncols):
            liT.append(worksheet.cell_value(i, j))
        li.append(liT)
    return li

#输出单个文件的训练样本与标签
def processOneExcel(fileName):
    data=read_excel_xls(fileName)
    # print(fileName)
    #print(afaf)
    processedData=[]
    for i in range(1,len(data)):
        # print(i)
        # print(afaf[i][2])
        # print(afaf[i][4])
        # temp=[说话人,文本,标签]
        temp=[int(data[i][2]),str(data[i][3]).strip(),int(data[i][4])]
        processedData.append(temp)

    processedData=[[2,"[NO]",8]]*4+processedData
    trainList=[]
    for i in range(4,len(processedData)):
        tempString="[KEY]"+speaker[processedData[i][0]]+processedData[i][1]+"[KEY]"
        for j in range(1,5):
            tempString=speaker[processedData[i-j][0]]+processedData[i-j][1]+"[NEXT]"+tempString
        trainList.append([tempString,processedData[i][2]-1])
    return trainList

def printNumber(dataList,name):
    print(name)
    print("总数:",len(dataList))
    countSet={}
    for key in labelKind.keys():
        countSet[key]=0
    for data in dataList:
        countSet[data[1]]+=1
    for key in countSet.keys():
        print(labelKind[key],":",countSet[key])
def writeData(trainLists):
    tensNumber=len(trainLists)//10
    shuffle(trainLists)
    train=trainLists[0:tensNumber*8]
    test=trainLists[tensNumber*8:tensNumber*9]
    dev=trainLists[tensNumber*9:]
    printNumber(trainLists,"ALL"),printNumber(train,"train"),printNumber(test,"test"),printNumber(dev,"dev")
    print("train,test,dev:",len(train),len(test),len(dev))
    with open('CLASSCon/data/train.txt', 'w') as f:
        for l in train:
            f.writelines(l[0]+'\t'+str(l[1])+'\n')
    with open('CLASSCon/data/test.txt', 'w') as f:
        for l in test:
            f.writelines(l[0]+'\t'+str(l[1])+'\n')
    with open('CLASSCon/data/dev.txt', 'w') as f:
        for l in dev:
            f.write(l[0]+'\t'+str(l[1])+'\n')
    return 0


files=get_filelist(r"CLASSCon\ExcelData")
trainLists=[]
for file in files:
    trainLists+=processOneExcel(file)

for conP in trainLists:
    conP[0]=conP[0].replace("[KEY]","")
print(trainLists[300:310])
writeData(trainLists)






