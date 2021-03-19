2021HW就要开始，各个单位又要开始关停业务、封堵IP了，为了方便绕过最粗暴的封堵，开启千年前陈旧的代理技术...（修改自XXX的auto-proxy）

自动切换代理

定时自动抓取代理,继续优化中

使用方法：
1. 安装redis数据库
2. 定时任务python alive_checker.py
3. python proxy_server.py 打开代理
4. 配置客户机windows的代理地址为运行脚本的服务器地址，端口默认8080

