import matplotlib.pyplot as plt
import xlrd
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

def cut(lis):
    cutTime=30
    time=lis[1]-lis[0]
    temp=[]
    num=time//cutTime
    temp.append([lis[0],lis[0]+time%cutTime,lis[2]])
    end=lis[0]+time%cutTime
    for i in range(num):
        temp.append([end,end+30,lis[2]])
        end=end+cutTime
    return temp

def slices(f,b):
    t1=[f[0],f[0]+(f[1]-f[0])//2,0]
    t2=[f[0]+(f[1]-f[0])//2,b[0]+(b[1]-b[0])//2,1]
    t3=[b[0]+(b[1]-b[0])//2,b[1],0]
    return [t1,t2,t3]

def moveAverage(lis):
    window=20
    step=5
    beg=0
    end=beg+window
    while(True):
        all=0
        for j in range(beg,end):
            all+=lis[j]
        average=all/window
        for j in range(beg,end):
            lis[j]=average
        beg+=step
        end+=step
        if(end>len(lis)):
            break
    return lis

def calBehavior(datalists):
    plates=[]
    for datalist in datalists:
        if datalist[1]-datalist[0]<=30:
            plates.append(datalist)
        else:
            tempLists=cut(datalist)
            for t in tempLists:
                plates.append(t)
    for plate in plates:
        if plate[2]==2:
            plate[2]=0
    return plates

def calInteraction(plates):
    interPlates=[]
    front=plates[0][2]
    for plate in plates:
        if plate[2]==front:
            interPlates.append([plate[0],plate[1],0])
        else:
            f=interPlates.pop()
            b=plate
            temp=slices(f,b)
            for tp in temp:
                interPlates.append(tp)
    return interPlates

def calAndDrawRT(plates):
    x=[]
    y=[]
    all=0
    for i in range(plates[-1][1]):
        for plate in plates:
            if i>=plate[0] and i<plate[1]:
                x.append(i)
                all+=plate[2]
                y.append(plate[2])
    RT=all/(plates[-1][1]+1)
    y=moveAverage(y)
    plt.plot(x, y, 's-', color='r',marker='')
    plt.hlines(RT, 0, len(x), colors="b", linestyles="dashed")
    plt.xlabel("time")  # 横坐标名字
    plt.ylabel("RT")  # 纵坐标名字
    plt.show()
    return RT

def calAndDrawCH(plates):
    x=[]
    y=[]
    all=0
    for i in range(plates[-1][1]):
        for plate in plates:
            if i>=plate[0] and i<plate[1]:
                x.append(i)
                all+=plate[2]
                y.append(plate[2])
    CH=all/(plates[-1][1]+1)
    y = moveAverage(y)
    plt.plot(x, y, 's-', color='r', marker='')
    plt.hlines(CH, 0, len(x), colors="b", linestyles="dashed")
    plt.xlabel("time")  # 横坐标名字
    plt.ylabel("CH")  # 纵坐标名字
    plt.show()
    return CH

def PointDraw(plates,task):
    #plate=(beg,end,number)
    x=[]
    k1=[]
    for i in range(plates[-1][1]):
        for plate in plates:
            if i>=plate[0] and i<=plate[1]:
                x.append(i)
                k1.append(plate[2])
    plt.plot(x, k1, 's-', color='r',marker='')
    plt.xlabel("time")  # 横坐标名字
    plt.ylabel(task)  # 纵坐标名字
    plt.show()

def ProcessData(data):
    processData1=[]
    data[1][0]='0'
    for i in range(1,len(data)):
        temp=[int(data[i][0]),int(data[i][1]),int(data[i][2])]
        processData1.append(temp)
    processData2=[]
    temp=processData1[0]
    for data in processData1:
        if data[2]==temp[2]:
            temp[1]=data[1]
        else:
            processData2.append(temp)
            temp=data
    for i in range(len(processData2)):
        temp=processData2[i]
        temp[0]=temp[0]//1000
        temp[1]=temp[1]//1000
        processData2[i]=temp
    return processData2

def ProcessTimeAndSpeaker(data):
    for i in range(1,len(data)):
        data[i][0]=int(data[i][0])
        data[i][1] = int(data[i][1])
        data[i][2] = int(data[i][2])
        data[i][4] = int(data[i][4])
    for i in range(1,len(data)-1):
        #调整错误说话人编码
        data[i][2]=ST[data[i][4]-1]
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



if __name__=='__main__':
    data=read_excel_xls("CLASSCon/ExcelData/惠柠/初中数学3(示范课)/数-赵.xls")
    data=ProcessTimeAndSpeaker(data)
    processData=ProcessData(data)
    plates=calBehavior(processData)
    interPlates=calInteraction(plates)
    PointDraw(plates, "plates")
    PointDraw(interPlates, "interPlates")
    RT=calAndDrawRT(plates)
    CH=calAndDrawCH(interPlates)
    print(RT,CH)



