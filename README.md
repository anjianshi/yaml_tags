基于 pyyaml，提供一些辅助的 tag

## 使用方式

1. 引入并实例化 Tag class
2. 把 Tag 实例注册到 pyyaml 的 loader 中
3. 使用 pyyaml 的 load / safe_load 等函数解析 yaml 内容

## 使用范例（以 inc tag 为例）

```yaml
# some_file.inc.yaml
x: 100
y: 200
```

```python
# run.py
import yaml
from yaml_tags import IncTag

IncTag().register()
data = yaml.load("""
    val_1: abc
    val_2: !inc some_file
""")
# data == {"val_1": "abc", "val_2": {"x": 100, "y": 200}}
```

```python
# 自定义 tag name
IncTag().register("!cust_tag_name")
data = yaml.load("""
    val: !cust_tag_name filename
""")
# data == {"val": {"x": 100, "y": 200}}
```

```python
# 手动指定要注册到哪个 Loader（默认注册到 yaml.Loader）
IncTag().register(loader=yaml.SafeLoader)
data = yaml.safe_load("""
    val: !inc some_file
""")
# data == {"val": {"x": 100, "y": 200}}
```

```python
# 在构建 IncTag 实例时，指定自定义选项（不同类型的 tag 有不同的选项）
IncTag(file_ext=".xyz.yaml").register()
data = yaml.load("""
    # 这将会载入 some_file.xyz.yaml 不过因为此文件不存在，所以会报错
    val: !inc some_file
""")
```


## Inc Tag
#### 格式
```yaml
# 以字符串的形式指定要载入的文件的路径（不包括扩展名）
a: !inc filename
b: !inc somepath/filename
c: !inc /absolute_path/filename
```

#### 载入路径的确定

inc tag 对文件路径的确定受三个因素的影响：

1. 构建 IncTag 实例时传入的 basepath
2. 通过 inc tag 指定的路径(下面称之为 inc_path）是绝对路径还是相对路径
3. 调用 yaml.load() 等函数时，传入的是文件句柄还是字符串

具体规则如下：
```
# 若指定了 basepath，则只允许引入 basepath 下的文件。
# 且 inc_path 无论是绝对路径还是相对路径，都会以 basepath 为基准。
# basepath 本身如果是相对路径，会以当前 Python 运行环境中的当前目录(os.getcwd())为基准，将其转换为绝对路径

# basepath = /data
!inc file         # 载入 /data/file.yaml
!inc abc/file     # 载入 /data/abc/file.yaml
!inc /abc/file    # 载入 /data/abc/file.yaml


# 未指定 basepath 的情况下，如果 inc_path 是绝对路径，则直接载入此路径对应的文件
# basepath = None
!inc /abc/file   # 载入 /abc/file.yaml


# 未指定 basepath 的情况下，如果 inc_path 是相对路径，则要分两种情况
# 1. 传给 yaml.load() 的是文件句柄。此时会以此文件所处目录作为基准，来载入 inc_path 所指的文件
# yaml.load(open("/somepath/main.yaml"))
!inc child      # 载入 /somepath/child.yaml

# 2. 传给 yaml.load() 的是字符串。此时会以当前 Python 运行环境的当前目录（os.getcwd()）为基准，进行载入
# os.chdir("/otherpath")
# yaml.load("yaml_content")
!inc child      # 载入 /otherpath/child.yaml
```


#### 自定义选项
以下选项可以在构建 IncTag 实例时传给它：

- `file_ext`  要载入的文件的扩展名，默认为 `.yaml`
- `basepath`  它的作用见上面的 `载入路径的确定` 小节
- `inc_file_loader` 使用哪个 yaml loader 来载入 inc 目标文件，默认使用载入了当前文件的 loader
  可以通过为 inc 目标文件单独指定一个 loader，来控制它们能使用的 tag。
  例如给它们设置一个不支持 inc tag 的 loader，就可以禁止 inc 文件再次引入其他 inc 文件。

