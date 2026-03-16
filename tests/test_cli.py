"""Unit tests for CLI module."""

import pytest
import tempfile
import os
import sys
from pathlib import Path
from markdown_to_wechat.cli import (
    parse_arguments,
    get_shell_rc,
    convert_directory,
)


class TestCLI:
    """Test cases for command-line interface."""

    def test_parse_basic_arguments(self, monkeypatch):
        """Test parsing basic input and output files."""
        monkeypatch.setattr(sys, 'argv', ['markdown-to-wechat', 'input.md', 'output.html'])
        args = parse_arguments()
        assert args.input_path == 'input.md'
        assert args.output_file == 'output.html'
        assert not args.split
        assert not args.no_css

    def test_parse_split_flag(self, monkeypatch):
        """Test parsing --split flag."""
        monkeypatch.setattr(sys, 'argv', ['markdown-to-wechat', 'input.md', 'output.html', '--split'])
        args = parse_arguments()
        assert args.split is True

    def test_parse_short_split_flag(self, monkeypatch):
        """Test parsing -s flag."""
        monkeypatch.setattr(sys, 'argv', ['markdown-to-wechat', 'input.md', 'output.html', '-s'])
        args = parse_arguments()
        assert args.split is True

    def test_parse_no_css_flag(self, monkeypatch):
        """Test parsing --no-css flag."""
        monkeypatch.setattr(sys, 'argv', ['markdown-to-wechat', 'input.md', 'output.html', '--no-css'])
        args = parse_arguments()
        assert args.no_css is True

    def test_parse_only_input(self, monkeypatch):
        """Test parsing with only input file."""
        monkeypatch.setattr(sys, 'argv', ['markdown-to-wechat', 'input.md'])
        args = parse_arguments()
        assert args.input_path == 'input.md'
        assert args.output_file is None

    def test_parse_install_alias(self, monkeypatch):
        """Test parsing --install-alias flag."""
        monkeypatch.setattr(sys, 'argv', ['markdown-to-wechat', '--install-alias'])
        args = parse_arguments()
        assert args.install_alias is True

    def test_parse_uninstall_alias(self, monkeypatch):
        """Test parsing --uninstall-alias flag."""
        monkeypatch.setattr(sys, 'argv', ['markdown-to-wechat', '--uninstall-alias'])
        args = parse_arguments()
        assert args.uninstall_alias is True

    def test_parse_stdout_flag(self, monkeypatch):
        """Test parsing --stdout flag."""
        monkeypatch.setattr(sys, 'argv', ['markdown-to-wechat', 'input.md', '--stdout'])
        args = parse_arguments()
        assert args.stdout is True

    def test_main_with_valid_file(self, capsys):
        """Test main function with a valid file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write('# Test\n\nContent')
            temp_file = f.name

        try:
            from markdown_to_wechat.cli import main

            original_argv = sys.argv
            sys.argv = ['markdown-to-wechat', temp_file, '--stdout']

            try:
                main()
            except SystemExit:
                pass

            captured = capsys.readouterr()
            assert '<!DOCTYPE html>' in captured.out or 'Error' not in captured.err

        finally:
            sys.argv = original_argv
            Path(temp_file).unlink()

    def test_main_with_nonexistent_file(self, capsys):
        """Test main function with non-existent file."""
        from markdown_to_wechat.cli import main

        original_argv = sys.argv
        sys.argv = ['markdown-to-wechat', 'nonexistent.md']

        with pytest.raises(SystemExit):
            main()

        sys.argv = original_argv


class TestShellDetection:
    """Test cases for shell detection."""

    def test_get_shell_rc_with_zsh(self, monkeypatch):
        """Test shell RC detection with zsh."""
        monkeypatch.setenv('SHELL', '/bin/zsh')
        result = get_shell_rc()
        assert result == os.path.expanduser('~/.zshrc')

    def test_get_shell_rc_with_bash(self, monkeypatch):
        """Test shell RC detection with bash."""
        monkeypatch.setenv('SHELL', '/bin/bash')
        result = get_shell_rc()
        assert result == os.path.expanduser('~/.bashrc')

    def test_get_shell_rc_unsupported(self, monkeypatch):
        """Test shell RC detection with unsupported shell."""
        monkeypatch.setenv('SHELL', '/bin/fish')
        result = get_shell_rc()
        assert result == ""


class TestBatchConversion:
    """Test cases for batch conversion."""

    def test_convert_directory_empty(self, capsys, tmp_path):
        """Test converting an empty directory."""
        total, success, failed = convert_directory(tmp_path)
        assert total == 0
        assert success == 0
        assert failed == 0

    def test_convert_directory_with_files(self, tmp_path):
        """Test converting a directory with markdown files."""
        md_file1 = tmp_path / "test1.md"
        md_file2 = tmp_path / "test2.md"
        
        md_file1.write_text("# Test 1\n\nContent 1", encoding='utf-8')
        md_file2.write_text("# Test 2\n\nContent 2", encoding='utf-8')
        
        total, success, failed = convert_directory(tmp_path)
        
        assert total == 2
        assert success == 2
        assert failed == 0
        
        html_file1 = tmp_path / "test1.html"
        html_file2 = tmp_path / "test2.html"
        
        assert html_file1.exists()
        assert html_file2.exists()
        
        assert "<!DOCTYPE html>" in html_file1.read_text(encoding='utf-8')
        assert "<!DOCTYPE html>" in html_file2.read_text(encoding='utf-8')

    def test_convert_directory_with_split(self, tmp_path):
        """Test converting a directory with split preview mode."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n\nContent", encoding='utf-8')
        
        total, success, failed = convert_directory(tmp_path, split_mode=True)
        
        assert total == 1
        assert success == 1
        assert failed == 0
        
        html_file = tmp_path / "test.html"
        assert html_file.exists()

    def test_convert_directory_with_no_css(self, tmp_path):
        """Test converting a directory without CSS."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n\nContent", encoding='utf-8')
        
        total, success, failed = convert_directory(tmp_path, no_css=True)
        
        assert total == 1
        assert success == 1
        assert failed == 0
        
        html_file = tmp_path / "test.html"
        content = html_file.read_text(encoding='utf-8')
        
        assert "<!DOCTYPE html>" not in content
        assert "<style>" not in content
