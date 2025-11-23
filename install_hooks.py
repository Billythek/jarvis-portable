#!/usr/bin/env python3
"""
JARVIS Laptop System - Hooks Installation Script
=================================================

Installs JARVIS hooks into Claude Code configuration for automatic
conversation capture and learning.

This script:
1. Locates Claude Code hooks directory
2. Copies JARVIS hooks to Claude hooks directory
3. Makes hooks executable
4. Verifies installation

Usage:
    python install_hooks.py
"""

import os
import sys
import shutil
from pathlib import Path


def find_claude_hooks_dir():
    """Find Claude Code hooks directory"""

    # Common locations for Claude Code hooks
    possible_paths = [
        Path.home() / ".claude" / "hooks",
        Path.home() / ".config" / "claude" / "hooks",
        Path(os.environ.get("APPDATA", "")) / "claude" / "hooks",  # Windows
        Path(os.environ.get("LOCALAPPDATA", "")) / "claude" / "hooks",  # Windows
    ]

    for path in possible_paths:
        if path.exists():
            return path

    # If not found, create default
    default_path = Path.home() / ".claude" / "hooks"
    default_path.mkdir(parents=True, exist_ok=True)
    return default_path


def install_hooks():
    """Install JARVIS hooks into Claude Code"""

    print("=" * 70)
    print("  JARVIS LAPTOP SYSTEM - HOOKS INSTALLATION")
    print("=" * 70)
    print()

    # Get paths
    jarvis_dir = Path(__file__).parent
    jarvis_hooks_dir = jarvis_dir / ".claude" / "hooks"
    claude_hooks_dir = find_claude_hooks_dir()

    print(f"[1/4] Paths")
    print(f"  JARVIS directory: {jarvis_dir}")
    print(f"  JARVIS hooks: {jarvis_hooks_dir}")
    print(f"  Claude hooks: {claude_hooks_dir}")
    print()

    # Check JARVIS hooks exist
    if not jarvis_hooks_dir.exists():
        print("[ERROR] JARVIS hooks directory not found!")
        print(f"  Expected: {jarvis_hooks_dir}")
        return False

    hook_files = [
        "user-prompt-submit.py",
        "post-tool-use.py",
        "session-end.py"
    ]

    print("[2/4] Checking JARVIS hooks...")
    for hook_file in hook_files:
        hook_path = jarvis_hooks_dir / hook_file
        if hook_path.exists():
            print(f"  [OK] {hook_file}")
        else:
            print(f"  [MISSING] {hook_file} NOT FOUND")
            return False
    print()

    # Copy hooks
    print("[3/4] Installing hooks to Claude Code...")
    for hook_file in hook_files:
        src = jarvis_hooks_dir / hook_file
        dst = claude_hooks_dir / hook_file

        # Backup existing hook if present
        if dst.exists():
            backup = dst.with_suffix(".py.backup")
            print(f"  [BACKUP] {hook_file} -> {backup.name}")
            shutil.copy2(dst, backup)

        # Copy new hook
        shutil.copy2(src, dst)
        print(f"  [INSTALL] {hook_file}")

        # Make executable (Unix-like systems)
        if os.name != 'nt':  # Not Windows
            os.chmod(dst, 0o755)

    print()

    # Verify installation
    print("[4/4] Verifying installation...")
    all_ok = True
    for hook_file in hook_files:
        hook_path = claude_hooks_dir / hook_file
        if hook_path.exists():
            size = hook_path.stat().st_size
            print(f"  [OK] {hook_file} ({size} bytes)")
        else:
            print(f"  [FAILED] {hook_file}")
            all_ok = False

    print()
    print("=" * 70)

    if all_ok:
        print("  INSTALLATION SUCCESSFUL")
        print("=" * 70)
        print()
        print("JARVIS hooks are now installed and active!")
        print()
        print("What happens now:")
        print("  - Every prompt you send to Claude Code -> captured by JARVIS")
        print("  - Every tool Claude uses -> logged by JARVIS")
        print("  - Every session end -> saved by JARVIS")
        print()
        print("JARVIS will learn from all your interactions automatically.")
        print()
        print("Next steps:")
        print("  1. Start JARVIS: python start_jarvis.py")
        print("  2. Use Claude Code normally")
        print("  3. Check logs: cat logs/hooks.log")
        print()
        print("=" * 70)
        return True
    else:
        print("  INSTALLATION FAILED")
        print("=" * 70)
        print()
        print("Some hooks failed to install. Please check:")
        print(f"  • JARVIS hooks directory: {jarvis_hooks_dir}")
        print(f"  • Claude hooks directory: {claude_hooks_dir}")
        print(f"  • File permissions")
        print()
        return False


def uninstall_hooks():
    """Remove JARVIS hooks from Claude Code"""

    print("=" * 70)
    print("  JARVIS LAPTOP SYSTEM - HOOKS UNINSTALLATION")
    print("=" * 70)
    print()

    claude_hooks_dir = find_claude_hooks_dir()

    hook_files = [
        "user-prompt-submit.py",
        "post-tool-use.py",
        "session-end.py"
    ]

    print("Removing JARVIS hooks from Claude Code...")
    for hook_file in hook_files:
        hook_path = claude_hooks_dir / hook_file

        if hook_path.exists():
            # Check if it's a JARVIS hook
            content = hook_path.read_text(encoding="utf-8")
            if "JARVIS" in content:
                hook_path.unlink()
                print(f"  [REMOVED] {hook_file}")

                # Restore backup if exists
                backup = hook_path.with_suffix(".py.backup")
                if backup.exists():
                    shutil.copy2(backup, hook_path)
                    print(f"  [RESTORED] {backup.name}")
            else:
                print(f"  [SKIP] {hook_file} (not a JARVIS hook)")
        else:
            print(f"  [SKIP] {hook_file} (not installed)")

    print()
    print("=" * 70)
    print("  UNINSTALLATION COMPLETE")
    print("=" * 70)
    print()


def main():
    """Main entry point"""

    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall_hooks()
    else:
        success = install_hooks()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
