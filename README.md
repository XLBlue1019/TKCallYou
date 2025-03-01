![CallYouIcon](./img/CallYouIcon.png)

# CallYou！一个适用于教室大屏的通知软件

---

> [!IMPORTANT]
> 该软件尚未完成，还有许多bug，请勿用于生产环境！

## ❓这是什么？

这是一个适用于教室大屏（如希沃、鸿合等）的通知软件。如果你是老师，你可以使用发送端轻松地向教室里的学生发送消息（带有语音）。

## 🧐原理

该软件使用 pycryptodome 对发送的消息进行 AES 加密，并发布到设定的 MQTT 服务器（默认为 EMQX 公共服务器）上，接收端接收到消息后解密，弹窗显示在屏幕上方。

## 🛠️使用组件

[zhiyiYo/PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)

## ❓如何设置`config.json`？

**注：** 未标注非必填的均为必填项，下方注释 **并不符合JSON规范，仅做标注**

```json5
{
    "mode": "r", // 模式，r为接收端，s为发送端
    "mqtt": {
        "broker": "broker.emqx.io", // mqtt服务器地址（接收端和发送端需相同，示例为EMQX公共服务器）
        "port": 1883, // 端口（接收端和发送端需相同）
        "topic": "tks/callyou/pymqtt/TKCU001", // 主题（接收端和发送端需相同，尽可能不要与其他用户（相同服务器下）重复）
        "client_id": "PYTKCU-r-TKCU001", // Client ID（接收端和发送端需不同，尽可能不要与其他用户（相同服务器下）重复）
        "username": "emqx", // 用户名（即使没有密码也必填）
        "password": "**********" // 密码（即使没有密码也必填）
    },
    "performance": {
        "refresh_time": 5000 // 刷新时间（每两次接收信息的间隔时间，单位ms，接收端配置，发送端非必填）
    },
    "show": {
        "stay_time": 10000 // 消息弹窗停留时间（单位ms，接收端配置，发送端非必填）
    },
    "key": "EXAMPLEKEY" // 消息加密秘钥（符合pycryptodome AES加密秘钥标准并使用BASE64编码，可调用cryption.py下的 randkey(lenth: int) 函数生成，接收端和发送端需相同）
}
```

## 🧰开发环境

### `Python`

版本：`3.13.2`

使用模块：见仓库根目录下`requirements.txt`文件


