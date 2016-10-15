

在使用虚拟机的时候，常需要手动指定 IP 地址，但是我们又不知道有哪些 IP 被使用了，
还有哪些 IP 可以使用，这时候，我们就需要一个工具，来帮助我们查看可用的 IP，这是我
做这个镜像的目的。

## 一、下载代码

```bash
git clone https://github.com/recall704/bayip.git
```


## 二、生成镜像

```bash
docker build -t bayip:v1.0.0 .
```

## 三、运行

```bash
docker run -d  --network host --restart=always -e HOSTS="192.168.1.0/24" --name bayip-test -d bayip:v1.0.0
```

运行时可以使用 host 模式，也可以使用桥接模式，桥接模式需要指定内部端口为 8888，例如
`-p 8086:8888`

HOSTS 参数需要按实际情况填写，对应为需要扫描的网段，一般是主机所在的网段。

## 四、接口
服务有两个接口

1. 获取当前在线主机：

```
curl http://192.168.1.33:8888/v1/online
```

3. 获取可用 IP

```
curl http://192.168.1.33:8888/v1/offline
```

## 五、其它
程序在执行的时候调用的是 nmap，执行大概需要 20s 左右，请耐心等待。

## 六、License
MIT
