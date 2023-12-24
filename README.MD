## 有问题issues
`词达人全自动,还在测试阶段,使用需要抓取token`
## 日志
**2023-12-23**
+ 新增选择全部单词
+ 过单词阅读卡片

**2023-12-23**
+ 获取 abc加密方式
+ 获取'授权‘加密(目前看来是固定)  
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

## 声明

请遵循MIT协议,仅供学习参考

## 使用
目前只有CET4书的测试,token需要自己抓取
```angular2html
pip install -r requirements.txt
```
配置 api/request_header.py 里面headers的token  
运行main.py   
![result](./img/result.png)
![result](./img/result2.png)