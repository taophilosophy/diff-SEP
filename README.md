# diff-SEP

斯坦福哲学百科全书爬取、对比更新脚本。该 python 脚本使用 ChatGPT 生成。

Python script used for crawling, comparing, and updating the Stanford Encyclopedia of Philosophy. This Python script is generated using ChatGPT.


## 用法

首先下载安装 Python 3：<https://www.python.org/downloads/>

然后下载 chromedriver.exe：<https://googlechromelabs.github.io/chrome-for-testing/>

**chromedriver.exe** 的版本号必须与你当前的 Chrome 版本尽可能靠近。可能最后的小版本会差几位数。（如果你没有 Chrome 你可能需要安装一下）

修改 `2.py` 中的 `driver_path = "C:\\Users\\ykla\\chromedriver.exe"` 为你的 `chromedriver.exe` 所在正确的路径。

```
$ pip install -r requirements.txt
$ python 1.py
$ python 2.py
$ python 3.py
```

`diff.txt` 和 `diff.log` 为差异。
