#coding=utf-8
import time

# 任务状态
class TaskState:
    NOSPLIT   = 0       #未分发
    COMPUTING = 1       #计算中
    COMPUTED  = 2       #计算完成
    COMPLETED = 3       #合并完成
    FAILED    = 4       #失败

class task:
    def __init__(self,name,cellCnt):
        self.name=name
        self.CellCnt=cellCnt
        self.state=TaskState.NOSPLIT
        self.worker=""
        self.time=""

class TaskManager:
    # Task队列
    TaskMQ=[]
    NoSplitTaskCnt=0

    def readTask(self):
        f = open("taskVolumeData.txt","rb")
        # 获取任务信息和计算量
        for line in f.readlines():
            print line
            lineList=line.split(" ")
            t=task(lineList[0],lineList[1])
            self.TaskMQ.append(t)
        print "共有"+str(len(self.TaskMQ)) +"个任务"
        self.NoSplitTaskCnt=len(self.TaskMQ)


    # 任务分发，work来get task,函数返回taskName
    def splitTask(self,workerName):
        taskName=""
        for task in self.TaskMQ:
            if task.state==TaskState.NOSPLIT or task.state==TaskState.FAILED:
                task.state=TaskState.COMPUTING
                task.worker=workerName
                task.time=time.time()
                taskName=task.name
                break
        return taskName

    def __init__(self):
        self.readTask()





if __name__=="__main__":
    t=TaskManager()

    t.splitTask("computerA")
    t.splitTask("computerB")




