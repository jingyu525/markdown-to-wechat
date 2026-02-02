"""Unit tests for CLI module."""

import pytest
import tempfile
from pathlib import Path
from markdown_to_wechat.cli import parse_arguments


class TestCLI:
    """Test cases for command-line interface."""

    def test_parse_basic_arguments(self):
        """Test parsing basic input and output files."""
        args = parse_arguments(['input.md', 'output.html'])
        assert args.input_file == 'input.md'
        assert args.output_file == 'output.html'
        assert not args.split
        assert not args.no_css

    def test_parse_split_flag(self):
        """Test parsing --split flag."""
        args = parse_arguments(['input.md', 'output.html', '--split'])
        assert args.split is True

    def test_parse_short_split_flag(self):
        """Test parsing -s flag."""
        args = parse_arguments(['input.md', 'output.html', '-s'])
        assert args.split is True

    def test_parse_no_css_flag(self):
        """Test parsing --no-css flag."""
        args = parse_arguments(['input.md', 'output.html', '--no-css'])
        assert args.no_css is True

    def test_parse_only_input(self):
        """Test parsing with only input file."""
        args = parse_arguments(['input.md'])
        assert args.input_file == 'input.md'
        assert args.output_file is None

    def test_main_with_valid_file(self, capsys):
        """Test main function with a valid file."""
        # Create a temporary markdown file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write('# Test\n\nContent')
            temp_file = f.name

        try:
            from markdown_to_wechat.cli import main
            import sys

            # Mock sys.argv
            original_argv = sys.argv
            sys.argv = ['markdown-to-wechat', temp_file]

            try:
                main()
            except SystemExit:
                pass

            # Check output
            captured = capsys.readouterr()
            assert '✅' in captured.out or 'Error' not in captured.err

        finally:
            # Cleanup
            sys.argv = original_argv
            Path(temp_file).unlink()

    def test_main_with_nonexistent_file(self, capsys):
        """Test main function with non-existent file."""
        from markdown_to_wechat.cli import main
        import sys

        original_argv = sys.argv
        sys.argv = ['markdown-to-wechat', 'nonexistent.md']

        with pytest.raises(SystemExit):
            main()

        sys.argv = original_argv
