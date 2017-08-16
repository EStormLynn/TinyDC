# TinyDC
一个简单的分布式计算框架，python搭建，支持调用外部程序执行计算。

把一个大任务分割成若干个独立的子任务，分派给多个运算单元执行，最后合并子任务运算结果

**加粗为C++部分**
## Client端
* 启动服务，创建任务，等待Worker连接
* 维护一个TaskMQ，记录TaskInfo
* 获取Worker连接，发送response.zip，分发Task
* 心跳检测Worker工作状态
* 接收Worker的result进行Merge

## Worker端
* getComputerInfo（hostName，ip，cpu，memory）
* 连接Client端，get计算需要的资源
* getTask（根据cpu核心数，优先get计算量大的task）
* **调用C++外部程序进行计算**
* 计算完成发送结果给Serve端


## TaskMQ(任务中间件)
python维护，负责任务的监控、分发，实现负载均衡错误

### 任务分发
根据客户端传来的computerInfo，以cpu核心数为主，把任务分发给Worker客户端

### 任务监控
记录任务信息，包含：
* 任务状态
    ```Python
    #任务状态
    TASK_STATUS_NOSPLITED = 'splited'   #未分派
    TASK_STATUS_COMPUTING = 'computing' #运算中
    TASK_STATUS_COMPUTED = 'computed'   #运算完
    TASK_STATUS_MERGEING = 'merging'    #待合并
    TASK_STATUS_COMPELED = 'completed'  #已完成
    TASK_STATUS_FAILED   = 'failed'     #失败
    ```

* 任务计算量
    
        effective cell nums  #需要计算的cell数量
* 任务消费者

        workID
* 任务开始时间

        time
        
### 容错
对于计算失败的任务，由Client端重新分配，Worker端重新开始其他的任务。


## 监控信息
**ComputerInfo**

Name|类型|状态|IP|CPU|线程数|完成任务数|心跳次数
-|-|-|-|-|-|-|-
HIH-D-10837|Leader|normal|20.240.166.12|4|1|9/20|55
C2|Worker|normal|20.240.166.14|4|4|2|55
C3|Worker|normal|20.240.166.15|8|4|3|55
C4|Worker|adnormal|20.240.166.16|4|4|3|55
C5|Worker|normal|20.240.166.17|4|4|3|55

**TaskInfo**

TaskName|状态|Effective Cell Nums|Worker|Time
-|-|-|-|-
Task0|Computed|200|C2|15:35
Task1|Computing|500|C3|15:45
Task2|Computing|300|C4|15:55
Task3|Mergering|200|C2|15:50
Task4|Failed|250|C5|15:52

**CREAT BY 司虎虎 2017/08/16**
