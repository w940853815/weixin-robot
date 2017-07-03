# weixin-robot
毕业设计---基于python的微信公众平台机器人的设计与实现

用到了几个技术

1. NGINX做负载均衡，反向代理

nginx.conf是nginx配置文件，如何配置请参考网上教程

2. 使用mysql数据库

数据库连接在config.py中配置，配置好主机，用户名和密码之后，新建一个数据库，数据库名为'weixin-robot'，然后运行db_creat.py脚本创建数据库，db_migrate.py脚本用来迁移数据库（存在一些问题，和数据库软件有关？）

3.  supervisor作进程管理工具

supervisord.conf是supervisor的配置文件，如何配置请参考网上教程

4. 后台管理系统采用adminlte(基于bootstrap3)框架，效果如下：

- 登录界面：

![image](https://github.com/w940853815/weixin-robot/blob/master/tmp/readme_img/QQ%E6%88%AA%E5%9B%BE20170701154618.png)

- 后天管理界面

![image](https://github.com/w940853815/weixin-robot/blob/master/tmp/readme_img/QQ%E6%88%AA%E5%9B%BE20170701154744.png)

5. aiml 全称Artificial Intelligence Markup Language(人工智能标记语言)

语法官方文档中有说明，对中文支持还算好，app/aiml_set文件夹存放aiml语料

6. BeautifulSoup爬虫

作为机器人的几个附加功能，有知乎问答，百度关键字查询

7. 图灵机器人api调用

注册一个账号，调用图灵api,解析封装返回微信即可

8. 动态语料库

将语料添加到数据库中，

---

微信公众号二维码

![image](https://github.com/w940853815/weixin-robot/blob/master/tmp/readme_img/qrcode_for_gh_a518a743ed79_258.jpg)





