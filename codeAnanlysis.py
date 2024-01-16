import xlrd
import matplotlib.pyplot as plt
import numpy as np
labelKind={0:"教师评价或回应学生",1:"教师提问",2:"教师指令",3:"教师讲授",4:"学生被动型应答",5:"学生创造型应答",6:"学生主动提问或发言",7:"沉寂杂音或讨论"}
ST={0:1,1:1,2:1,3:1,4:2,5:2,6:2,7:2}

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

def ProcessTimeAndSpeaker(data):
    for i in range(len(data)):
        data[i][0]=int(data[i][0])
        data[i][1] = int(data[i][1])
        data[i][2] = int(data[i][2])
        data[i][4] = int(data[i][4])
    for i in range(len(data)-1):
        #调整错误说话人编码
        data[i][2]=ST[data[i][4]-1]
        #调整编码
        data[i][4]=data[i][4]-1
        #调整时间轴
        if data[i][0]<data[i+1][0]:
            data[i][1]=data[i+1][0]
        elif data[i][0]==data[i+1][0]:
            for j in range(i+1,len(data)):
                if data[j][0]!=data[i][0]:
                    timeSP=(data[i][1]-data[i][0])//(j-i)
                    if timeSP==0:
                        print(data[i])
                    bg=data[i][0]
                    for k in range(i,j):
                        data[k][0]=bg
                        bg=bg+timeSP
                        data[k][1]=bg
                    break
                elif j==len(data)-1:
                    timeSP=(data[i][1]-data[i][0])//(j-i+1)
                    if timeSP==0:
                        print(data[i])
                    bg=data[i][0]
                    for k in range(i,j+1):
                        data[k][0]=bg
                        bg=bg+timeSP
                        data[k][1]=bg
                    break
    return data

def printNumber(dataList,name):
    print(name)
    print("总数:",len(dataList))
    countSet={}
    for key in labelKind.keys():
        countSet[key]=0
    for data in dataList:
        countSet[data[4]]+=1
    for key in countSet.keys():
        print(labelKind[key],":",countSet[key],",",countSet[key]/len(dataList))

def calAndDrawTensor(data):
    vals = np.zeros((8, 8)).astype(np.int)
    pairSet={}
    for i in range(8):
        for j in range(8):
            pairSet[str(i)+'-'+str(j)]=0
    for i in range(len(data)-1):
        before=data[i][4]
        after=data[i+1][4]
        vals[before][after]+=1
        pairSet[str(before)+'-'+str(after)]=pairSet[str(before)+'-'+str(after)]+1
    col = []
    for i in range(0, 8):
        col.append(i)
    row = []
    for i in range(0,8):
        row.append(i)

    plt.figure(figsize=(9, 9))
    tab = plt.table(cellText=vals,
                    colLabels=col,
                    rowLabels=row,
                    loc='center',
                    cellLoc='center',
                    rowLoc='center')
    tab.scale(1, 2)
    plt.axis('off')
    plt.show()
    lst_sort = sorted(pairSet.items(), key=lambda k: k[1],reverse=True)
    for tu in lst_sort:
        print(tu[0],tu[1])

data=read_excel_xls("CLASSCon/ExcelData/惠柠/初中数学3(示范课)/数-赵.xls")
data=data[1:]
data=ProcessTimeAndSpeaker(data)
print(data)
calAndDrawTensor(data)
#printNumber(afaf,"数学")

