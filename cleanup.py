#!/usr/bin/env python3
import shutil
from pathlib import Path

# Delete the egg-info directory
egg_info_dir = Path('/Users/zyb/Downloads/公众号运营/markdown-to-wechat/src/markdown_to_wechat.egg-info')

if egg_info_dir.exists():
    shutil.rmtree(egg_info_dir)
    print(f"✅ Deleted: {egg_info_dir}")
else:
    print(f"⚠️ Directory not found: {egg_info_dir}")

# Delete this cleanup script
cleanup_script = Path(__file__)
cleanup_script.unlink()
