# API 文档

本文档详细说明了 markdown-to-wechat 的 Python API。

## 核心类

### MarkdownToWeChatConverter

主要的转换器类，负责将 Markdown 转换为微信兼容的 HTML。

#### 构造函数

```python
MarkdownToWeChatConverter()
```

初始化转换器。

**示例：**

```python
from markdown_to_wechat import MarkdownToWeChatConverter

converter = MarkdownToWeChatConverter()
```

#### 方法

##### convert()

```python
convert(markdown_text: str, include_css: bool = True) -> str
```

将 Markdown 文本转换为 HTML。

**参数：**

- `markdown_text` (str): 要转换的 Markdown 内容
- `include_css` (bool, optional): 是否在输出中包含 CSS 样式，默认为 True

**返回：**

- `str`: 适用于微信公众号的 HTML 字符串

**示例：**

```python
converter = MarkdownToWeChatConverter()
markdown = "# 欢迎使用\n\n这是一个示例。"
html = converter.convert(markdown, include_css=True)
```

##### convert_file()

```python
convert_file(
    input_file: str,
    output_file: Optional[str] = None,
    include_css: bool = True
) -> str
```

将 Markdown 文件转换为 HTML。

**参数：**

- `input_file` (str): 输入 Markdown 文件路径
- `output_file` (Optional[str]): 输出 HTML 文件路径（可选）
- `include_css` (bool, optional): 是否在输出中包含 CSS 样式，默认为 True

**返回：**

- `str`: 转换后的 HTML 内容

**异常：**

- `FileNotFoundError`: 当输入文件不存在时抛出

**示例：**

```python
converter = MarkdownToWeChatConverter()
html = converter.convert_file('input.md', 'output.html')
```

##### extract_title()

```python
extract_title(markdown_text: str, default_title: str = '文章') -> str
```

从 Markdown 文本中提取标题。

**参数：**

- `markdown_text` (str): Markdown 内容
- `default_title` (str, optional): 如果没有找到标题时使用的默认标题，默认为 '文章'

**返回：**

- `str`: 提取的标题

**示例：**

```python
converter = MarkdownToWeChatConverter()
title = converter.extract_title('# My Title', default='Default')
# title = 'My Title'
```

### PreviewGenerator

预览生成器类，负责生成预览 HTML 文件。

#### 构造函数

```python
PreviewGenerator()
```

初始化预览生成器。

**示例：**

```python
from markdown_to_wechat import PreviewGenerator

generator = PreviewGenerator()
```

#### 方法

##### generate_preview()

```python
generate_preview(
    markdown_text: str,
    html_content: str,
    title: str,
    output_file: Optional[str] = None,
    split: bool = False
) -> str
```

从 Markdown 和 HTML 内容生成预览 HTML。

**参数：**

- `markdown_text` (str): 原始 Markdown 文本
- `html_content` (str): 转换后的 HTML 内容
- `title` (str): 文档标题
- `output_file` (Optional[str]): 保存预览文件的路径（可选）
- `split` (bool, optional): 是否生成分屏预览，默认为 False

**返回：**

- `str`: 生成的预览 HTML 内容

**异常：**

- `FileNotFoundError`: 当模板文件未找到时抛出

**示例：**

```python
generator = PreviewGenerator()
preview = generator.generate_preview(
    markdown_text='# Title',
    html_content='<h1>Title</h1>',
    title='My Document',
    output_file='preview.html',
    split=False
)
```

##### generate_from_file()

```python
generate_from_file(
    markdown_file: str,
    html_content: str,
    output_file: Optional[str] = None,
    split: bool = False
) -> str
```

从 Markdown 文件生成预览。

**参数：**

- `markdown_file` (str): Markdown 文件路径
- `html_content` (str): 转换后的 HTML 内容
- `output_file` (Optional[str]): 保存预览文件的路径（可选）
- `split` (bool, optional): 是否生成分屏预览，默认为 False

**返回：**

- `str`: 生成的预览 HTML 内容

**示例：**

```python
converter = MarkdownToWeChatConverter()
generator = PreviewGenerator()

html = converter.convert_file('article.md')
preview = generator.generate_from_file(
    'article.md',
    html,
    'preview.html',
    split=True
)
```

## 配置模块

### config

配置和常量模块。

#### 常量

##### TITLE_PREFIX_TO_REMOVE

需要从标题中移除的前缀。

```python
from markdown_to_wechat.config import TITLE_PREFIX_TO_REMOVE
```

##### HEADING_STYLES

标题样式映射字典。

```python
from markdown_to_wechat.config import HEADING_STYLES

# HEADING_STYLES[1] 包含 h1 的样式
```

#### 函数

##### get_wechat_css()

```python
get_wechat_css() -> str
```

返回为微信公众号优化的 CSS 样式。

**返回：**

- `str`: CSS 样式字符串

**示例：**

```python
from markdown_to_wechat.config import get_wechat_css

css = get_wechat_css()
```

##### get_template_path()

```python
get_template_path(template_name: str) -> str
```

获取模板文件的路径。

**参数：**

- `template_name` (str): 模板文件名（如 'preview_template.html'）

**返回：**

- `str`: 模板文件的路径

**示例：**

```python
from markdown_to_wechat.config import get_template_path

template_path = get_template_path('preview_template.html')
```

## 使用示例

### 基本转换

```python
from markdown_to_wechat import MarkdownToWeChatConverter

converter = MarkdownToWeChatConverter()
markdown = """
# 欢迎使用

这是一个 **Markdown** 示例。

- 列表项 1
- 列表项 2

```python
print('Hello, WeChat!')
```
"""

html = converter.convert(markdown)
print(html)
```

### 文件转换

```python
from markdown_to_wechat import MarkdownToWeChatConverter

converter = MarkdownToWeChatConverter()
html = converter.convert_file('input.md', 'output.html')
```

### 生成预览

```python
from markdown_to_wechat import MarkdownToWeChatConverter, PreviewGenerator

converter = MarkdownToWeChatConverter()
generator = PreviewGenerator()

html = converter.convert_file('article.md')

# 生成单页预览
generator.generate_from_file('article.md', html, 'preview.html')

# 生成分屏预览
generator.generate_from_file('article.md', html, 'split_preview.html', split=True)
```

### 自定义样式

```python
from markdown_to_wechat import MarkdownToWeChatConverter

converter = MarkdownToWeChatConverter()

# 修改 CSS
converter.css_styles = '''
<style>
    body {
        font-family: 'Your Font', sans-serif;
        line-height: 2.0;
    }
</style>
'''

markdown = '# Custom Style'
html = converter.convert(markdown)
```

## 错误处理

### FileNotFoundError

当输入文件不存在时抛出。

```python
from markdown_to_wechat import MarkdownToWeChatConverter

converter = MarkdownToWeChatConverter()
try:
    converter.convert_file('nonexistent.md')
except FileNotFoundError as e:
    print(f"Error: {e}")
```

## 类型提示

所有函数都包含类型提示，可以使用 mypy 进行类型检查。

```bash
mypy src/markdown_to_wechat/
```

## 下一步

- 查看 [安装指南](installation.md)
- 查看 [使用示例](../examples/)
- 查看 [贡献指南](../CONTRIBUTING.md)
