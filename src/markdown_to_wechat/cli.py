"""Command-line interface for markdown-to-wechat."""

import argparse
import sys
from pathlib import Path

from .converter import MarkdownToWeChatConverter
from .preview import PreviewGenerator


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
  # Basic conversion
  %(prog)s article.md article.html

  # Generate preview with side-by-side view
  %(prog)s article.md preview.html --split

  # Output to stdout
  %(prog)s article.md

  # Use Markdown library if available for better conversion
  pip install markdown
  %(prog)s article.md output.html
        '''
    )

    parser.add_argument(
        'input_file',
        type=str,
        help='Input Markdown file path'
    )

    parser.add_argument(
        'output_file',
        type=str,
        nargs='?',
        help='Output HTML file path (optional, defaults to stdout)'
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
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point for command-line interface."""
    args = parse_arguments()

    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)

    if not input_path.is_file():
        print(f"Error: '{args.input_file}' is not a file", file=sys.stderr)
        sys.exit(1)

    # Initialize converter
    converter = MarkdownToWeChatConverter()

    # Convert Markdown to HTML
    try:
        html_content = converter.convert_file(
            args.input_file,
            include_css=not args.no_css
        )
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)

    # Handle split preview
    if args.split:
        try:
            preview_generator = PreviewGenerator()
            preview_html = preview_generator.generate_from_file(
                args.input_file,
                html_content,
                output_file=args.output_file,
                split=True
            )

            # Output preview content if no file specified
            if not args.output_file:
                print(preview_html)

        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            print("Note: Split preview templates should be in the 'templates' directory", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error during preview generation: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Regular output
        if args.output_file:
            # File already saved by convert_file
            pass
        else:
            # Print to stdout
            print(html_content)


if __name__ == '__main__':
    main()
