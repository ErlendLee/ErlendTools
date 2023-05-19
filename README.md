# ErlendTools

自己在工作中编写的Sublime小工具

## 安装
1、在sublime安装目录下创建 Data 目录。

2、重新启动sublime，将当前代码复制到 Data\Packages\ErlendTools 下

3、如果需要翻译功能，请申请并配置百度翻译的appid和appkey

4、快捷键配置：Default (Windows).sublime-keymap

## 功能
### 百度翻译
调用了百度翻译的免费api接口。
维护ErlendTRS.py中以下变量
```
appid = '替换为你的appid'
appkey = 'appkey替换为你的appkey'
```

### 格式化对齐文本
对选中的文本，使用空格分列，填充长度，按列对齐，方便列模式处理
```
aaa bb
cc ddddd
eeeeeee  f
转换为：
aaa     bb
cc      ddddd
eeeeeee f
```

### 删除空行
删除选中文本中的空行

### 数字求和
提取选中文本中的数值，进行求和，效果如下：
```
昨日粮油销售了50元，冰激凌销售了1.00元，口香糖销售金额为0.5，水果销售金额为.99元
----------
['50', '1.00', '0.5', '.99']
52.49

```

### 快捷切换VIM模式

### ···