现在家庭宽带都具有IPV6地址, 结合桥接方式, 可以拥有一个自己的公网服务器. 本项目使用阿里云 python SDK 将本地 linux 服务器的ipv6地址,更新至阿里云云解析,实现DDNS.




## 使用本项目前的要求:
1. 家庭宽带支持IPV6, 且可以改成桥接.
2. 路由器可关闭IPV6防火墙或添加自定义规则.
3. 有一个闲置的电脑.
4. 有在阿里云托管的域名.

## 定时触发:

### 使用crontab

### 使用 systemd timer

## 使用步骤:

### 阿里云相关配置
1. 有在阿里云托管的域名.
2. 云解析
3. RAM用户和角色
https://help.aliyun.com/zh/ram/developer-reference/use-the-sts-openapi-example?spm=5176.smartservice_service_robot_chat_new.console-base_help.dexternal.73a0f625rgefDo

### 本地网络配置
2. 家庭宽带改桥接.

### 本地系统配置
3. 有一台安装好linux系统的服务器.

### 项目配置
1. .env



# TODO
完善readme,doc
加上一个缓存文件, 替代每次请求解析记录

