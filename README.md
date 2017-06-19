# Process-and-Resource-Management-Design

Operating System first assignment

[TOC]

### 总体设计

__管理器：__ 

1. - [ ] 进程创建
2. - [ ] 进程撤销
3. - [ ] 进程调度
4. - [ ] 多单元（multi_unit）资源管理
5. - [ ] 资源申请
6. - [ ] 资源释放
7. - [ ] 错误检测
8. - [ ] 定时器中断



__Test Shell :__

1. - [ ] 从终端或__测试文件__读取命令
2. - [ ] 将用户需求转换为调度内核函数(即调度进程和资源管理器)
3. - [ ] 在终端或__输出文件__中显示结果：如当前运行的进程、错误信息等



__终端或测试文件：__

1. - [ ] 给出相应的用户命令
2. - [ ] 模拟硬件引起的中断





### Test Shell设计

要求完成命令：

- init    // 初始化


- cr <name> <priority>(=1 or 2)     // 创建进程
- de <name>    // 删除进程
- req <resource name> <# of units>    // 申请资源
- rel <resource name> <# of units>    // 释放资源
- to    // 定时器中断



可选实现的命令：

- lr    // 列出当前所有资源和状态
- lp    // 列出当前所有进程和状态
- pinfo <name list>    // 提供指定进程(支持多个进程)的信息:  pinfo x y






### 进程管理设计

#### 进程状态与操作

进程状态：

- ready
- running
- blocked



进程操作：

- 创建(create) : (none) -> ready
- 撤销(destroy) : running/ready/blocked -> (none)
- 请求资源(Request) : running -> blocked （当资源没有时，进程阻塞）
- 释放资源(Release) : blocked -> ready （因申请资源而阻塞的进程被唤醒）
- 时钟中断(Time_out) : running -> ready
- 调度 : ready -> running    或    running -> ready


#### 进程控制块结构（PCB）

- __PID (name)__

- __Other_resources__

- __Status : Type & List__     

  // Type : ready, running, block

  // List : RL (Ready list) or BL (block list)

- __Creation_tree : Parent/Children__

- __Priority : 0, 1, 2 (Init, User, System)__




![pcb](https://github.com/AgentDS/Process-Resource-Management/raw/master/PCB.png)



#### 主要函数

* 创建进程

  ```c++
  Create(initialization parameters)    
  // 用进程的ID和优先级来初始化进程
  {
    create PCB data structure
    initialize PCB using parameters    // 包括进程的ID,优先级,状态等
    link PCB to creation tree
    insert(RL, PCB)    // 插入就绪响应优先级队列的尾部
    Scheduler()
  }
  ```

  ​

如图表示进程A为运行进程，在进程A运行过程中，创建用户进程B：

```cr B 1```

数据结构间关系应该为：![进程块间关系](https://github.com/AgentDS/Process-Resource-Management/raw/master/进程块间关系.png)

* 撤销进程

  ```c++
  Destroy(pid)
  {
    get pointer p to PCB using pid
    Kill_Tree(p)
    Scheduler()    // 调度其他进程执行
  }

  Kill_Tree(p)
  {
    // 嵌套调用
    for all child processes q Kill_Tree(q)    
    free resource    // 和release调用类似的功能
    delete PCB and update all pointers
  }

  ```

  ​



### 资源管理设计

#### 主要数据结构

__资源表示：__ 1xR1,2xR2,3xR3,4xR4

__资源管理块RCB : __

* RID : 资源的ID

* Status : 空闲单元的数量

* Waiting_List : list of blocked process

  ![RCB](https://github.com/AgentDS/Process-Resource-Management/raw/master/RCB.png)

#### 请求资源

按照FIFO规则调度

* 情况一：一类资源本身只有一个

  ```c++
  Request(rid)
  {
    r = Get_RCB(rid);
    if (r->Status == 'free')    
    // 只有一个资源时可用free和allocated来表示资源状态
    {
      r->Status = 'allocated';
      insert(sef->Other_Resources, r);
    }
    else
    {
      self->Status.Type = 'blocked';
      self->Status.List = r;
      remove(RL,self);
      insert(r->Waiting_List,self);
      Scheduler();
    }
  }
  ```

  ​

* 情况二：一类资源有多个(multi_unit)

```c++
Request(rid,n)    // n为请求资源数量
{
  r = Get_RCB(rid);
  if (u>=n)    // u为r->Status.u,即可用资源数量
  {
    u = u - n;
    insert(self->Other_Resources, r, n);
  }
  else
  {
    if (n>k) exit;
    self->Status.Type = 'blocked';
    self->Status.List = r;
    remove(RL,self);
    insert(r->Waiting_List,self);
    Scheduler();
  }
}
```





#### 释放资源

* 情况一：一类资源只有1个的情况

  ```c++
  Release(rid)
  {
    r = Get_RCB(rid);
    remove(self->Other_Resources, r);
    if (r->Waiting_List == NIL)  
    {
    r->Status = 'free'; 
    }
    else 
    {
    remove(r->Waiting_List, q);
    q->Status.Type = 'ready';
    q->Status.List = RL;    //就绪队列
    insert(q->Other_Resources, r);
    insert(RL, q); 
    Scheduler();
  }
  ```

  ​

* 情况二：一类资源有多个的情况

  ```c++
  Release(rid,n)
  {
    r = Get_RCB(rid);
    remove(self->Other_Resources,r,n);
    while (r->Waiting_List != NIL && u>=req_num)
    {
      u=u- req_num; 
      remove(r->Waiting_List, q);
      q->Status.Type = 'ready';
      q->Status.List = RL;
      insert(q->Other_Resources, r); 
      insert(RL, q);
    }
    Scheduler();
  }
  ```

  ​

### 进程调度与时钟中断设计

__调度策略：__

* 基于 3 个优先级别的调度:2，1，0

* 使用基于优先级的抢占式调度策略，在同一优先级内使用时间片轮转(RR)

* 基于函数调用来模拟时间共享

* 初始进程(Init process)具有双重作用:

  虚设的进程:具有最低的优先级，永远不会被阻塞

  进程树的根



__Scheduler:__

called at the end of every kernel call

```c++
Scheduler() {
find highest priority process p
if (self->priority < p->priority ||
self->Status.Type != 'running' ||
self == NIL) 
preempt(p, self)//在条件(3)(4)(5)下抢占当前进程
}
Condition (3): called from create or release, 即新创建进程的优先级或
资源释放后唤醒进程的优先级高于当前进程优先级
Condition (4): called from request or time-out， 即请求资源使得当前运行进程阻塞或者时钟中断使得当前运行进程变成就绪
Condition (5): called from destroy，进程销毁
Preemption: //抢占，将P变为执行，输出当前运行进程的名称
•	Change status of p to running (status of self already changed to ready/blocked)
•	Context switch—output name of running process

```

__时钟中断：__

模拟时间片或外部硬件中断

```c++
Time_out() 
{
find running process q; //当前运行进程q
remove(RL, q);// remove from head? yes
q->Status.Type = 'ready';
insert(RL, q);// insert into tail? yes
Scheduler();
}

```



### 系统初始化设计

启动时初始化管理器：

* 具有3个优先级的就绪队列RL初始化
* Init进程
* 4类资源，R1，R2，R3，R4，每类资源Ri有i个
