# simple_sipder
一个简单的爬虫软件实例
爬取的是中国卡车网上的所有在售卡车数据，以csv的方式储存

先要安装需要的库，本地或切换到虚拟环境之后执行

``` bash
pip install -r requirements.txt
```

直接运行
```bash
python3 spider.py
```

目录下自动生成csv文件
固定爬取 https://www.chinatruck.org/product/ 下所有的卡车型号数据