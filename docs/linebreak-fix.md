# 微信公众号换行问题修复说明

## 问题描述

用户反馈：在预览 HTML 文件时可以看到正确的换行，但复制到微信公众号编辑器后，文本不换行，全部显示在一行。

## 问题原因

经过分析，发现以下问题：

### 1. 缺少 `line-height` 内联样式
- **问题**：虽然 CSS 中定义了 `line-height: 1.75`，但微信公众号编辑器主要依赖内联样式
- **影响**：行高不明确，导致换行显示异常

### 2. 缺少换行控制属性
- **问题**：没有 `word-wrap` 和 `word-break` 属性
- **影响**：长文本无法正确换行，特别是在英文单词或数字序列中

### 3. `text-align: justify` 的影响
- **问题**：使用 `text-align: justify`（两端对齐）可能在某些情况下影响换行显示
- **影响**：在微信公众号编辑器中可能导致换行不稳定

## 修复方案

### 1. 段落样式修复

**修改前：**
```python
html_lines.append(f'<p style="margin-bottom:16px;text-align:justify;">{processed_line}</p>')
```

**修改后：**
```python
html_lines.append(f'<p style="margin-bottom:16px;text-align:left;line-height:1.75;word-wrap:break-word;word-break:break-word;">{processed_line}</p>')
```

**关键修改：**
- ✅ 添加 `line-height: 1.75` 内联样式
- ✅ 添加 `word-wrap: break-word`（允许在单词内换行）
- ✅ 添加 `word-break: break-word`（现代浏览器推荐）
- ✅ 将 `text-align: justify` 改为 `text-align: left`

### 2. CSS 样式更新

**段落样式：**
```css
/* 修改前 */
p {
    margin-bottom: 16px;
    text-align: justify;
}

/* 修改后 */
p {
    margin-bottom: 16px;
    text-align: left;
    line-height: 1.75;
    word-wrap: break-word;
    word-break: break-word;
}
```

**列表项样式：**
```css
/* 修改前 */
li {
    margin-bottom: 8px;
}

/* 修改后 */
li {
    margin-bottom: 8px;
    line-height: 1.75;
    word-wrap: break-word;
    word-break: break-word;
}
```

**引用块样式：**
```css
/* 修改前 */
blockquote {
    margin: 20px 0;
    padding: 15px 20px;
    background-color: #f8f9fa;
    border-left: 4px solid #3498db;
    color: #555;
}

/* 修改后 */
blockquote {
    margin: 20px 0;
    padding: 15px 20px;
    background-color: #f8f9fa;
    border-left: 4px solid #3498db;
    color: #555;
    line-height: 1.75;
    word-wrap: break-word;
    word-break: break-word;
}
```

## 技术说明

### word-wrap vs word-break

**`word-wrap: break-word`：**
- 允许在单词内部换行
- 兼容性较好（包括旧版浏览器）
- 仅在单词长度超过容器宽度时才换行

**`word-break: break-word`：**
- 现代标准，功能与 `word-wrap: break-word` 相同
- 推荐在新项目中使用
- 同时使用两个属性可以最大化兼容性

### line-height 的重要性

- **作用**：控制文本行之间的间距
- **推荐值**：1.5-1.75（正文）
- **原因**：提高可读性，避免文本过于紧凑

### text-align 的选择

**为什么不用 `justify`（两端对齐）：**
- 微信公众号编辑器对 `justify` 的支持不完善
- 可能导致最后一行文本显示异常
- 某些情况下会影响换行判断

**使用 `left`（左对齐）的优势：**
- 兼容性最好
- 换行稳定可靠
- 移动端显示效果一致

## 测试方法

### 1. 使用测试文件

```bash
cd /Users/zyb/Downloads/公众号运营/markdown-to-wechat

# 安装包
pip install -e .

# 转换测试文件
markdown-to-wechat tests/fixtures/test_linebreak.md output.html
```

### 2. 预览效果

在浏览器中打开 `output.html`，查看换行效果是否正常。

### 3. 复制到公众号编辑器

1. 在浏览器中选中 HTML 内容
2. 复制到微信公众号编辑器
3. 检查换行是否正常

## 预期效果

修复后，以下情况应该都能正确换行：

✅ 段落中的长文本
✅ 列表项中的长文本
✅ 引用块中的长文本
✅ 包含链接的长文本
✅ 包含粗体/斜体的长文本
✅ 表格单元格中的长文本

## 注意事项

1. **表格单元格**：需要额外处理，添加 `td` 样式
2. **代码块**：通常不需要换行，保持原样
3. **中文和英文混排**：两种换行属性都能正常处理

## 相关文件

- `src/markdown_to_wechat/converter.py` - 段落生成逻辑
- `src/markdown_to_wechat/config.py` - CSS 样式定义
- `tests/fixtures/test_linebreak.md` - 测试文件

## 参考资料

- [微信公众号编辑器技术限制](../.codebuddy/skills/markdown-to-wechat/references/wechat_editor_limitations.md)
- [CSS word-wrap 属性](https://developer.mozilla.org/en-US/docs/Web/CSS/word-wrap)
- [CSS word-break 属性](https://developer.mozilla.org/en-US/docs/Web/CSS/word-break)
