![CallYouIcon](./img/CallYouIcon.png)

# CallYou！一个适用于教室大屏的通知软件


---


> [!WARNING]
> 该软件尚未完成，还有许多bug，请勿用于生产环境！

> [!IMPORTANT]
> 消息密文的秘钥以明文形式储存，不建议传送高隐私性内容！

> [!NOTE]
> 目前`V0.2.0`版本尚未完成开发，敬请期待！
> 如果有需要，请下载`V0.1.0`版本进行试用 **（非常不建议，该版本包含许多超级严重的bug未修复！！！！）**


## ❓这是什么？

这是一个适用于教室大屏（如希沃、鸿合等）的通知软件。如果你是老师，你可以使用发送端轻松地向教室里的学生发送消息（带有语音）。


## 🧐原理

该软件用户界面使用`Pyside6`，使用`pycryptodomex`对发送的消息进行AES加密，并使用`paho-mqtt`发布到设定的MQTT服务器（默认为EMQX公共服务器）上，接收端接收到消息后解密，弹窗显示在屏幕上方。


## 📷屏幕截图
> [!NOTE]
> 目前`V0.2.0`版本尚未完成开发，敬请期待！


## ❓如何设置`config.json`？

> [!TIP]
> 未标注非必填的均为必填项，下方注释 **并不符合JSON规范，仅做标注**
```json5
{
    "mode": "r", // 模式，r为接收端，s为发送端
    "mqtt": {
        "broker": "broker.emqx.io", // mqtt服务器地址（接收端和发送端需相同，示例为EMQX公共服务器）
        "port": 1883, // 端口（接收端和发送端需相同）
        "topic": "tks/callyou/pymqtt/TKCU001", // 主题（接收端和发送端需相同，尽可能不要与其他用户（相同服务器下）重复）
        "client_id": "PYTKCU-r-TKCU001", // Client ID（接收端和发送端需不同，尽可能不要与其他用户（相同服务器的相同topic下）重复）
        "username": "emqx", // 用户名（即使没有密码也必填）
        "password": "**********" // 密码（即使没有密码也必填）
    },
    "show": {
        "stay_time": 10000 // 消息弹窗停留时间（单位ms，接收端配置，发送端非必填）
    },
    "key": "EXAMPLEKEY" // 消息加密秘钥（符合pycryptodome AES加密秘钥标准并使用BASE64编码，可调用cryption.py下的 randkey(lenth: int) 函数生成，接收端和发送端需相同）
}
```


## 🧰开发环境

### `Python`

- 版本：`3.12.9`
- 主要使用模块：（详见仓库根目录下`requirements.txt`文件）
    ```
    cryptography==44.0.2
    Nuitka==2.6.7
    paho-mqtt==2.1.0
    pycryptodomex==3.21.0
    PySide6==6.8.2.1
    pyttsx3==2.98
    requests==2.32.3
    ```


## ❗重要更改

- 自`2025/3/2`起，从`PyQt6`转而使用`PySide6`，且从项目中移除了`QFluentWidgets`组件库，不再支持`v2.0.0`以下版本的`paho-mqtt`库。
- 自`2025/3/9`起，将`pycryptodome`替换为`pycryptodomex`


## 🌚已知还没有修改的bug

- [ ] 收到消息后浮窗文本框不实时更新
- [ ] `pycryptodomex`不与`Nuitka`兼容
- [ ] UI太丑了！！！！！！！！（虽然但是好像也不算bug...）


## 📝画饼

- [ ] 