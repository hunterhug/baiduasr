# Baidu ASR

百度API文档：[Here](https://ai.baidu.com/docs#/ASR-Online-Python-SDK/top)
 
语音识别:将人类的语音中的词汇内容转换为计算机可读的输入，例如按键、二进制编码或者字符序列

## Usage

需要：Python3.+，默认普通话(支持简单的英文识别)

```
pip3 install -r requirements.txt
```

然后编辑`config/config.json`：

```
{
  "appId": "14296900",
  "appKey": "PMtKEQ31A2gU4YTM52CrGIfD",
  "appSecret": "eGaS3lMPNXfkk2pp0vSIgRkkoR677Sz",
  "asrDir": "./dir",
  "resultDir": "./result",
  "resultFile": "./result.csv",
  "process": 30
}
```

1. asrDir 为音频目录，可为wav和pcm文件
2. resultDir 为识别结果目录
3. resultFile 结果汇总csv
4. process 调进程数

appID，appKey，appSecret等账户信息请上控制台获取，上百度API控制台获取。

运行识别：

```
python3 main.py
```

因为是增量进行识别，所以当你运行完毕后，将其识别结果汇总为一张`csv`，`UTF8` 编码，所以`Mac OX`打开时可能乱码，你自己应该处理：

```
python3 main.py csv
```

日志配置在`config/log.json`， 日志路径在用户根目录下！