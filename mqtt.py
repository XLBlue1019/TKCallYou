from paho.mqtt import client as mqtt_client

class MQTTClient():
    def __init__(self):
        super().__init__()

        # 初始化各配置变量
        self.broker = ""
        self.port = 0
        self.topic = ""
        self.client_id = ""

        self.username = ""
        self.password = ""

    # 连接到MQTT服务器
    def connect_mqtt(self, 
                     on_connect = lambda client, userdata, flags, rc: print("Connected to MQTT Broker!" if rc == 0 else f"Failed to connect, return code {rc}") # 默认连接后的事件
                     ):
        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, self.client_id)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
        return self.client

    # 订阅话题
    def subscribe(self, 
                  on_message = lambda client, userdata, msg: print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic") # 默认收到消息后的事件
                  ):
        self.client.subscribe(topic=self.topic, qos=0)
        self.client.on_message = on_message

    # 取消订阅
    def unsubscribe(self):
        self.client.on_message = None
        self.client.unsubscribe(self.topic)
        
    # 发布信息
    def publish(self, msg):
        result = self.client.publish(self.topic, msg)
        status = result[0]
        return status
