import datetime
import time

# win10 安装蓝牙依赖包 https://blog.csdn.net/weixin_38676276/article/details/113027104
import bluetooth


class BluetoothConnection:
    def __init__(self):
        # 是否找到到设备
        self.find = False
        # 附近蓝牙设备
        self.nearby_devices = None

    def find_nearby_devices(self):
        print("Detecting nearby Bluetooth devices...")
        # 可传参数 duration--持续时间 lookup-name=true 显示设备名
        # 大概查询10s左右
        # 循环查找次数
        loop_num = 3
        i = 0
        try:
            self.nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=5)
            while self.nearby_devices.__len__() == 0 and i < loop_num:
                self.nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=5)
                if self.nearby_devices.__len__() > 0:
                    break
                i = i + 1
                time.sleep(2)
                print("No Bluetooth device around here! trying again {}...".format(str(i)))
            if not self.nearby_devices:
                print("There's no Bluetooth device around here. Program stop!")
            else:
                print("{} nearby Bluetooth device(s) has(have) been found:".format(self.nearby_devices.__len__()), self.nearby_devices)  # 附近所有可连的蓝牙设备s
        except Exception as e:
            # print(traceback.format_exc())
            # 不知是不是Windows的原因，当附近没有蓝牙设备时，bluetooth.discover_devices会报错。
            print("There's no Bluetooth device around here. Program stop(2)!")

    def find_target_device(self, target_name, target_address):
        self.find_nearby_devices()
        if self.nearby_devices:
            for addr, name in self.nearby_devices:
                if target_name == name and target_address == addr:
                    print("Found target bluetooth device with address:{} name:{}".format(target_address, target_name))
                    self.find = True
                    break
            if not self.find:
                print("could not find target bluetooth device nearby. "
                      "Please turn on the Bluetooth of the target device.")

    def connect_target_device(self, target_name, target_address):
        self.find_target_device(target_name=target_name, target_address=target_address)
        if self.find:
            print("Ready to connect")
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            try:
                sock.connect((target_address, 1))
                print("Connection successful. Now ready to get the data")
                data_dtr = ""
                # 以下代码根据需求更改
                while True:
                    data = sock.recv(1024)
                    data_dtr += data.decode()
                    if '\n' in data.decode():
                        # data_dtr[:-2] 截断"\t\n",只输出数据
                        print(datetime.datetime.now().strftime("%H:%M:%S")+"->"+data_dtr[:-2])
                        data_dtr = ""
            except Exception as e:
                print("connection fail\n", e)
                sock.close()


if __name__ == '__main__':
    target_name = "BT04-A"
    target_address = "B4:4B:0E:04:16:25"
    BluetoothConnection().connect_target_device(target_name=target_name, target_address=target_address)
