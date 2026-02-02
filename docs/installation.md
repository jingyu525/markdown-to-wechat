# 安装指南

本文档详细说明了如何在不同环境下安装 markdown-to-wechat。

## 系统要求

- Python 3.7 或更高版本
- pip（Python 包管理器）

## 安装方法

### 方法 1：使用 pip 安装（推荐）

这是最简单、最推荐的安装方式。

```bash
pip install markdown-to-wechat
```

### 方法 2：从源码安装

如果你想使用最新开发版本或修改代码，可以从源码安装。

#### 克隆仓库

```bash
git clone https://github.com/yourusername/markdown-to-wechat.git
cd markdown-to-wechat
```

#### 安装依赖

```bash
pip install -e .
```

`-e` 标志表示"可编辑模式"，这样你对代码的修改会立即生效。

### 方法 3：使用虚拟环境

推荐使用虚拟环境来隔离项目依赖。

#### 创建虚拟环境

```bash
# 使用 venv
python -m venv myenv

# 或使用 conda
conda create -n myenv python=3.9
```

#### 激活虚拟环境

```bash
# Linux/Mac
source myenv/bin/activate

# Windows
myenv\Scripts\activate
```

#### 安装包

```bash
pip install markdown-to-wechat
```

## 可选依赖

### 安装 Markdown 库

虽然 markdown-to-wechat 包含基本的 Markdown 转换功能，但安装 `markdown` 库可以获得更好的转换质量：

```bash
pip install markdown
```

### 安装开发依赖

如果你想参与开发，需要安装开发依赖：

```bash
pip install markdown-to-wechat[dev]
```

或在源码目录下：

```bash
pip install -e ".[dev]"
```

开发依赖包括：
- `pytest` - 测试框架
- `pytest-cov` - 测试覆盖率
- `black` - 代码格式化
- `flake8` - 代码风格检查
- `mypy` - 静态类型检查

## 验证安装

安装完成后，可以通过以下命令验证：

```bash
# 检查命令行工具是否可用
markdown-to-wechat --version

# 应该输出：markdown-to-wechat 1.0.0

# 测试 Python 导入
python -c "from markdown_to_wechat import MarkdownToWeChatConverter; print('Import successful!')"
```

## 升级

升级到最新版本：

```bash
pip install --upgrade markdown-to-wechat
```

## 卸载

如果需要卸载：

```bash
pip uninstall markdown-to-wechat
```

## 常见问题

### Q: 提示 "command not found: markdown-to-wechat"

A: 这通常是因为 pip 的 scripts 目录不在系统 PATH 中。你可以：

1. 使用 Python 模块方式运行：
   ```bash
   python -m markdown_to_wechat.cli article.md
   ```

2. 或将 pip 的 scripts 目录添加到 PATH：
   - Linux/Mac: `~/.local/bin`
   - Windows: `%APPDATA%\Python\Scripts`

### Q: 权限错误

A: 使用 `--user` 标志安装到用户目录：

```bash
pip install --user markdown-to-wechat
```

### Q: Python 版本不兼容

A: 确保使用 Python 3.7+。检查 Python 版本：

```bash
python --version
```

## 下一步

安装完成后，你可以：

1. 查看 [快速开始](../README.md#快速开始)
2. 阅读 [API 文档](api.md)
3. 查看 [使用示例](../examples/)

## 获取帮助

如果遇到安装问题，请：

1. 查看 [GitHub Issues](https://github.com/yourusername/markdown-to-wechat/issues)
2. 创建新的 issue 并提供详细信息
3. 发送邮件至 your.email@example.com
