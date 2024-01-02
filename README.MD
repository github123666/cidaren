## 有问题issues
`词达人刷分脚本`
- [x] 修复已知bug
- [x] 扩展脚本
- [x] 汉转英没有好的接口(目前只能利用google,正确率不高的原因)
- [x] 转原型的第三方库不是很好用

<details> <summary> 日志 </summary>

**目前存在的bug**  
+ 环境问题,google要挂梯子
+ 转成单词原型没有好用的库 

**2023-12-26**
+ 添加无需抓包的方法

**2023-12-24**
+ 修复服务器放回错误数据

**2023-12-24**
+ 解决一部分”单词填空“bug

**2023-12-23**
+ 新增选择全部单词
+ 过单词阅读卡片

**2023-12-23**
+ 获取 abc加密方式
+ 获取header '授权‘ 加密(目前看来是固定)  
+ 暂时无法解决的bug,用第三方库个别单词无法转成原型,需要手动过该题目

**2023-12-22**
+ 修复单选bug  
+ 修复填充单词bug

**2023-12-21**

+ 汉译英
+ 英译汉
+ 听力
+ 填写句子
+ complete单词
+ 稳定85分以上

**2023-12-19**

+ 完成选择题提交
+ 后面会补全
+ 写的有点乱,后面调整一下
</details>


## 声明

请遵循MIT协议,仅供学习参考

## 使用
方法一：获取微信code,拼手速,点下面授权cdr的链接标签页转一圈半就关掉,打开其他网页百度什么的,查看浏览记录,配置config.json
![img.png](img/img.png)
```angular2html
https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx2a694105a6abbe6d&redirect_uri=https%3A%2F%2Fapp.vocabgo.com%2Fstudent%2F%3Fauthorize%3D2&response_type=code&scope=snsapi_userinfo&state=STATE
```
方法二:  
自己抓包,抓token 

配置config.json里面token


配置环境
```angular2html
pip install -r requirements.txt
```
运行main.py   
![result](./img/result.png)
![result](./img/result2.png)