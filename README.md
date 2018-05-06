## fweixin
>使用itchat,flask做的小玩具

**功能描述**

 * 显示好友,群聊信息
 * 统计好友比例
 * 定时给好友发送消息,或者连续多次发送
 * 发送消息给所有好友(没敢测试)
 
**使用说明**

```
到fweixin目录下执行python server.py,默认使用的8000端口
执行命令后会弹出二维码,使用微信扫描登录后,会自动打开浏览器显示好友列表
```
**<font color=red>**注意事项**</font>**

*使用yield和thread实现的定时发送,每起一个任务会起一个线程,所以不要同时起太多定时任务*

