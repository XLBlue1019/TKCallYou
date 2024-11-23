![CallYouIcon](https://soft.bluetinker.cn/cu/icon.png)

# CallYou！一个适用于教室大屏的通知软件

---

## 这是什么？

这是一个适用于教室大屏（如希沃、鸿合等）的通知软件。如果你是老师，你可以使用发送端轻松地向教室里的学生发送消息（带有语音）。

## 原理

该软件使用 pycryptodome 对发送的消息进行 AES 加密，并发布到设定的 MQTT 服务器（默认为 EMQX 公共服务器）上，接收端接收到消息后解密，弹窗显示在屏幕上方。

## 使用组件

[zhiyiYo/PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)


