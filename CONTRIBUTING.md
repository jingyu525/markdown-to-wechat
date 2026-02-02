# 贡献指南

感谢你对 markdown-to-wechat 项目的关注！我们欢迎任何形式的贡献。

## 🤝 如何贡献

### 报告问题

如果你发现了 bug 或有功能建议，请：

1. 在 [GitHub Issues](https://github.com/yourusername/markdown-to-wechat/issues) 中搜索是否已有类似问题
2. 如果没有，创建一个新的 issue，详细描述：
   - 问题的复现步骤
   - 预期行为
   - 实际行为
   - 环境信息（Python 版本、操作系统等）

### 提交代码

#### 1. Fork 项目

点击 GitHub 页面右上角的 "Fork" 按钮

#### 2. 克隆仓库

```bash
git clone https://github.com/yourusername/markdown-to-wechat.git
cd markdown-to-wechat
```

#### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

#### 4. 安装开发依赖

```bash
pip install -e ".[dev]"
```

#### 5. 进行开发

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 代码风格
- 为新功能添加测试
- 更新相关文档

#### 6. 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并查看覆盖率
pytest --cov=src/markdown_to_wechat --cov-report=html
```

#### 7. 代码格式化

```bash
# 格式化代码
black src/ tests/

# 检查代码风格
flake8 src/ tests/

# 类型检查
mypy src/
```

#### 8. 提交更改

```bash
git add .
git commit -m "feat: add new feature"  # 或 "fix: fix bug"
```

Commit message 遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具链相关

#### 9. 推送分支

```bash
git push origin feature/your-feature-name
```

#### 10. 创建 Pull Request

1. 在 GitHub 上创建 Pull Request
2. 填写 PR 模板，说明你的改动
3. 等待代码审查

## 📝 开发指南

### 项目结构

```
markdown-to-wechat/
├── src/
│   └── markdown_to_wechat/
│       ├── __init__.py       # 包初始化
│       ├── config.py         # 配置和常量
│       ├── converter.py      # 核心转换器
│       ├── preview.py        # 预览生成器
│       └── cli.py           # 命令行接口
├── templates/               # HTML 模板
├── tests/                   # 测试文件
├── docs/                    # 文档
├── examples/                # 使用示例
└── pyproject.toml          # 项目配置
```

### 编码规范

- 使用 4 空格缩进
- 遵循 PEP 8 规范
- 添加类型注解
- 编写清晰的文档字符串

```python
def example_function(param: str, optional_param: int = 0) -> bool:
    """
    函数的简短描述。

    详细描述函数的功能和行为。

    Args:
        param: 参数描述
        optional_param: 可选参数描述

    Returns:
        返回值描述

    Raises:
        ValueError: 可能抛出的异常
    """
    pass
```

### 测试规范

- 为新功能编写单元测试
- 使用 pytest 作为测试框架
- 测试覆盖率保持在 80% 以上

```python
import pytest
from markdown_to_wechat import MarkdownToWeChatConverter

def test_basic_conversion():
    converter = MarkdownToWeChatConverter()
    markdown = "# Test\n\nContent"
    html = converter.convert(markdown)

    assert '<h1' in html
    assert 'Test' in html
```

## 📧 联系方式

如有疑问，请通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件至 your.email@example.com

## 📄 许可证

提交代码即表示你同意将代码以 MIT 许可证发布。

---

再次感谢你的贡献！🎉
