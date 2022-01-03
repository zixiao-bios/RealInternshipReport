## RealInternshipReport

### 介绍

自动生成中南大学计科专业格式的实习日志、实习报告。

### 原理

爬取菜鸟教程网站的内容，使用 [sumy](https://github.com/miso-belica/sumy) 提取总结文字内容，再通过 [python-docx](https://github.com/python-openxml/python-docx) 按照规定格式写入 word 文档。

### 使用

前置条件：Python 3.5 +、pip 已安装

```shell
pip install requests_html
pip install sumy
pip install jieba
pip install python-docx
```

将 `log.py` 文件开头的 `generate_page_num, year, month, date` 变量修改为需要生成的页数、开始的年份、月份、日期。然后运行该文件，运行完成后会在同目录下生成 word 文档。