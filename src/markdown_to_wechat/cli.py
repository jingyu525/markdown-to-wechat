"""Command-line interface for markdown-to-wechat."""

import argparse
import os
import sys
from pathlib import Path
from typing import Tuple

from . import __version__
from .converter import MarkdownToWeChatConverter
from .preview import PreviewGenerator


def get_shell_rc() -> str:
    """
    Detect the shell configuration file path.
    
    Returns:
        Path to shell configuration file, or empty string if not supported
    """
    shell_name = ""
    
    if os.environ.get('SHELL'):
        shell_path = os.environ['SHELL']
        if shell_path.endswith('/zsh'):
            shell_name = 'zsh'
        elif shell_path.endswith('/bash'):
            shell_name = 'bash'
    
    if not shell_name:
        if os.environ.get('ZSH_VERSION'):
            shell_name = 'zsh'
        elif os.environ.get('BASH_VERSION'):
            shell_name = 'bash'
    
    if shell_name == 'zsh':
        return os.path.expanduser('~/.zshrc')
    elif shell_name == 'bash':
        return os.path.expanduser('~/.bashrc')
    else:
        return ""


def install_alias() -> int:
    """
    Install the md2wx alias in shell configuration file.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    shell_rc = get_shell_rc()
    
    if not shell_rc:
        print("错误: 无法检测到支持的shell类型 (支持 zsh/bash)", file=sys.stderr)
        print(f"当前 SHELL: {os.environ.get('SHELL', '未知')}", file=sys.stderr)
        return 1
    
    print(f"检测到 shell 配置文件: {shell_rc}")
    
    try:
        with open(shell_rc, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'alias md2wx=' in content:
            print("别名 md2wx 已存在，正在更新...")
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if line.startswith('alias md2wx='):
                    new_lines.append("alias md2wx='markdown-to-wechat'")
                else:
                    new_lines.append(line)
            content = '\n'.join(new_lines)
        else:
            content += '\n\n# Markdown to WeChat HTML converter\n'
            content += "alias md2wx='markdown-to-wechat'\n"
        
        with open(shell_rc, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("别名安装成功！")
        print("请运行以下命令使其生效:")
        print(f"  source {shell_rc}")
        print()
        print("之后可以使用: md2wx article.md")
        return 0
        
    except Exception as e:
        print(f"错误: 无法修改配置文件: {e}", file=sys.stderr)
        return 1


def uninstall_alias() -> int:
    """
    Uninstall the md2wx alias from shell configuration file.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    shell_rc = get_shell_rc()
    
    if not shell_rc:
        print("错误: 无法检测到支持的shell类型 (支持 zsh/bash)", file=sys.stderr)
        print(f"当前 SHELL: {os.environ.get('SHELL', '未知')}", file=sys.stderr)
        return 1
    
    print(f"检测到 shell 配置文件: {shell_rc}")
    
    try:
        with open(shell_rc, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'alias md2wx=' not in content:
            print("别名 md2wx 不存在")
            return 0
        
        lines = content.split('\n')
        new_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue
            if line.strip() == '# Markdown to WeChat HTML converter':
                continue
            if line.startswith('alias md2wx='):
                continue
            new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        with open(shell_rc, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("别名已卸载！")
        print("请运行以下命令使其生效:")
        print(f"  source {shell_rc}")
        return 0
        
    except Exception as e:
        print(f"错误: 无法修改配置文件: {e}", file=sys.stderr)
        return 1


def convert_directory(
    dir_path: Path,
    split_mode: bool = False,
    no_css: bool = False
) -> Tuple[int, int, int]:
    """
    Convert all Markdown files in a directory.
    
    Args:
        dir_path: Path to directory containing Markdown files
        split_mode: Whether to generate split preview
        no_css: Whether to exclude CSS styles
        
    Returns:
        Tuple of (total_count, success_count, failed_count)
    """
    converter = MarkdownToWeChatConverter()
    preview_generator = PreviewGenerator() if split_mode else None
    
    md_files = sorted(dir_path.glob('*.md'))
    
    if not md_files:
        print(f"警告: 目录中没有找到 Markdown 文件: {dir_path}")
        return 0, 0, 0
    
    total = len(md_files)
    success = 0
    failed = 0
    
    print(f"扫描目录: {dir_path}")
    if split_mode:
        print("模式: 分屏预览")
    if no_css:
        print("模式: 无CSS样式")
    print()
    
    for md_file in md_files:
        output_file = md_file.with_suffix('.html')
        print(f"转换: {md_file.name} -> {output_file.name}")

        try:
            if split_mode and preview_generator:
                # Let PreviewGenerator handle the conversion internally
                preview_generator.generate_from_file(
                    str(md_file),
                    html_content=None,  # Will be generated internally
                    output_file=str(output_file),
                    split=True
                )
            else:
                # For non-split mode, convert with CSS
                html_content = converter.convert_file(
                    str(md_file),
                    include_css=not no_css
                )
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)

            print(f"✅ 成功: {output_file}")
            success += 1

        except Exception as e:
            print(f"❌ 错误: 转换失败 {md_file.name}: {e}", file=sys.stderr)
            failed += 1

        print()
    
    print("=" * 50)
    print(f"总计: {total} 个文件")
    print(f"成功: {success} 个")
    print(f"失败: {failed} 个")
    
    return total, success, failed


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog='markdown-to-wechat',
        description='Convert Markdown to WeChat Official Account compatible HTML',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic conversion (auto-generate output filename)
  %(prog)s article.md

  # Convert with specific output file
  %(prog)s article.md article.html

  # Batch convert all Markdown files in a directory
  %(prog)s ./articles/

  # Generate preview with side-by-side view
  %(prog)s article.md preview.html --split

  # Output to stdout
  %(prog)s article.md --stdout

  # Install global alias 'md2wx'
  %(prog)s --install-alias
  source ~/.zshrc  # or ~/.bashrc

  # Use Markdown library if available for better conversion
  pip install markdown
  %(prog)s article.md output.html
        '''
    )

    parser.add_argument(
        'input_path',
        type=str,
        nargs='?',
        help='Input Markdown file or directory path'
    )

    parser.add_argument(
        'output_file',
        type=str,
        nargs='?',
        help='Output HTML file path (optional, auto-generated if not specified)'
    )

    parser.add_argument(
        '--split', '-s',
        action='store_true',
        help='Generate split preview with Markdown and HTML side by side'
    )

    parser.add_argument(
        '--no-css',
        action='store_true',
        help='Exclude CSS styles from output'
    )

    parser.add_argument(
        '--stdout',
        action='store_true',
        help='Output to stdout instead of file'
    )

    parser.add_argument(
        '--install-alias',
        action='store_true',
        help='Install global alias md2wx for markdown-to-wechat'
    )

    parser.add_argument(
        '--uninstall-alias',
        action='store_true',
        help='Uninstall global alias md2wx'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point for command-line interface."""
    args = parse_arguments()

    if args.install_alias:
        sys.exit(install_alias())

    if args.uninstall_alias:
        sys.exit(uninstall_alias())

    if not args.input_path:
        print("错误: 未指定输入路径", file=sys.stderr)
        print("使用 --help 查看帮助信息", file=sys.stderr)
        sys.exit(1)

    input_path = Path(args.input_path)

    if not input_path.exists():
        print(f"错误: 路径不存在: {args.input_path}", file=sys.stderr)
        sys.exit(1)

    if input_path.is_dir():
        if args.output_file:
            print("警告: 批量转换目录时，output_file 参数将被忽略", file=sys.stderr)
        
        total, success, failed = convert_directory(
            input_path,
            split_mode=args.split,
            no_css=args.no_css
        )
        
        sys.exit(0 if failed == 0 else 1)

    if not input_path.is_file():
        print(f"错误: '{args.input_path}' 不是文件", file=sys.stderr)
        sys.exit(1)

    converter = MarkdownToWeChatConverter()

    try:
        html_content = converter.convert_file(
            str(input_path),
            include_css=not args.no_css
        )
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: 转换失败: {e}", file=sys.stderr)
        sys.exit(1)

    if args.stdout:
        print(html_content)
        sys.exit(0)

    output_file = args.output_file
    if not output_file:
        output_file = str(input_path.with_suffix('.html'))

    if args.split:
        try:
            preview_generator = PreviewGenerator()
            # Let PreviewGenerator handle the conversion internally
            preview_generator.generate_from_file(
                str(input_path),
                html_content=None,  # Will be generated internally
                output_file=output_file,
                split=True
            )
            print(f"✅ 生成分屏预览: {output_file}")
        except FileNotFoundError as e:
            print(f"错误: {e}", file=sys.stderr)
            print("注意: 分屏预览模板应该在 'templates' 目录中", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"错误: 生成预览失败: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # For non-split mode, use the converted HTML with CSS
        html_content = converter.convert_file(
            str(input_path),
            include_css=not args.no_css
        )
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ 转换成功: {output_file}")


if __name__ == '__main__':
    main()
