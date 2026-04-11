#!/usr/bin/env python3

import os
import re
import shlex
import subprocess
import shutil
import glob
import hashlib
import stat
import pwd
import grp
import datetime
from pathlib import Path
from typing import List, Dict, Callable, Tuple, Set
from concurrent.futures import ThreadPoolExecutor, as_completed


# ============================================================================
# Color System
# ============================================================================

class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


def cprint(text, color=Color.RESET):
    print(f"{color}{text}{Color.RESET}")


# ============================================================================
# Help System
# ============================================================================

HELP = {
    "copy": {
        "usage": "copy SRC to DST1|DST2",
        "desc": "Copy file to one or more destinations",
        "example": "copy a.txt to backup/|test/"
    },
    "move": {
        "usage": "move SRC to DST1|DST2",
        "desc": "Move file to destinations",
        "example": "move a.txt to backup/"
    },
    "find": {
        "usage": "find PATTERN [ROOT]",
        "desc": "Find files recursively",
        "example": "find *.py ."
    },
    "finddup": {
        "usage": "finddup [ROOT]",
        "desc": "Find duplicate files (by content) and choose action",
        "example": "finddup /home/user/docs"
    },
    "for": {
        "usage": "for VAR in PATTERN => COMMAND",
        "desc": "Loop over matched files",
        "example": "for f in *.py => echo {}"
    },
    "dry": {
        "usage": "dry on|off",
        "desc": "Enable or disable dry-run mode",
        "example": "dry on"
    },
    "exit": {
        "usage": "exit",
        "desc": "Exit EasyBash",
        "example": "exit"
    },
    "tree": {
        "usage": "tree [PATH]",
        "desc": "Display directory tree with detailed file info (size, permissions, owner, group, mtime)",
        "example": "tree /home/user/docs"
    },
    "update": {
        "usage": "update",
        "desc": "Update EasyBash from remote git repository",
        "example": "update"
    }
}


# ============================================================================
# Path Manager
# ============================================================================

class PathManager:
    @staticmethod
    def expand_glob(paths: List[str]) -> List[str]:
        expanded = []
        for p in paths:
            if any(c in p for c in ('*', '?', '[')):
                expanded.extend(glob.glob(p, recursive=True))
            else:
                expanded.append(p)
        return expanded

    @staticmethod
    def filter_dirs(paths: List[str]) -> List[str]:
        out = []
        for p in paths:
            if Path(p).exists():
                out.append(p)
            else:
                cprint(f"[WARN] Path does not exist: {p}", Color.YELLOW)
        return out


# ============================================================================
# Executor
# ============================================================================

class Executor:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    def run_cmd(self, cmd, cwd=None):
        if self.dry_run:
            cprint(f"[DRY-RUN] cd {cwd} && {' '.join(cmd)}", Color.YELLOW)
            return 0

        try:
            return subprocess.run(cmd, cwd=cwd, timeout=30).returncode
        except subprocess.TimeoutExpired:
            cprint("[ERROR] Command timed out", Color.RED)
            return 1
        except Exception as e:
            cprint(f"[ERROR] {e}", Color.RED)
            return 1

    def parallel(self, paths, cmd):
        paths = PathManager.filter_dirs(PathManager.expand_glob(paths))
        if not paths:
            cprint("[ERROR] No valid paths for parallel execution", Color.RED)
            return

        success = 0
        fail = 0

        with ThreadPoolExecutor(max_workers=8) as ex:
            futures = [ex.submit(self.run_cmd, cmd, p) for p in paths]
            for f in as_completed(futures):
                if f.result() == 0:
                    success += 1
                else:
                    fail += 1

        cprint(f"[SUMMARY] success={success}, fail={fail}", Color.CYAN)

    def chain(self, paths, cmd):
        paths = PathManager.filter_dirs(PathManager.expand_glob(paths))
        if not paths:
            cprint("[ERROR] No valid paths for chain execution", Color.RED)
            return

        for p in paths:
            cprint(f"[CHAIN] {p}", Color.BLUE)
            r = self.run_cmd(cmd, p)
            if r != 0:
                cprint("[CHAIN STOP] command failed", Color.RED)
                break

    def single(self, cmd):
        self.run_cmd(cmd)


# ============================================================================
# File Ops
# ============================================================================

class FileOps:
    @staticmethod
    def _strip_quotes(s: str) -> str:
        if len(s) >= 2 and (s[0] == s[-1] == '"' or s[0] == s[-1] == "'"):
            return s[1:-1]
        return s

    @staticmethod
    def copy(src, dsts):
        src_path = Path(src)

        if not src_path.exists():
            cprint(f"[ERROR] Source not found: {src}", Color.RED)
            return False

        success = True

        for d in dsts:
            try:
                d = Path(FileOps._strip_quotes(d))
                target = d / src_path.name if d.is_dir() else d
                shutil.copy2(src_path, target)
                cprint(f"[COPY] {src} -> {target}", Color.GREEN)
            except Exception as e:
                success = False
                cprint(f"[ERROR] Copy failed: {e}", Color.RED)

        return success

    @staticmethod
    def move(src, dsts):
        success = FileOps.copy(src, dsts)
        if success:
            try:
                Path(src).unlink()
                cprint(f"[MOVE] removed {src}", Color.GREEN)
            except Exception as e:
                cprint(f"[ERROR] Failed to remove source: {e}", Color.RED)
        else:
            cprint("[MOVE] aborted due to copy failure", Color.RED)

    @staticmethod
    def delete_file(path: Path, dry_run: bool):
        if dry_run:
            cprint(f"[DRY-RUN] Would delete: {path}", Color.YELLOW)
            return True
        try:
            path.unlink()
            cprint(f"[DELETE] Removed: {path}", Color.GREEN)
            return True
        except Exception as e:
            cprint(f"[ERROR] Could not delete {path}: {e}", Color.RED)
            return False

    @staticmethod
    def move_file(src: Path, dst_dir: Path, dry_run: bool):
        dst = dst_dir / src.name
        if dry_run:
            cprint(f"[DRY-RUN] Would move: {src} -> {dst}", Color.YELLOW)
            return True
        try:
            shutil.move(str(src), str(dst))
            cprint(f"[MOVE] Moved: {src} -> {dst}", Color.GREEN)
            return True
        except Exception as e:
            cprint(f"[ERROR] Could not move {src} to {dst}: {e}", Color.RED)
            return False


# ============================================================================
# Finder
# ============================================================================

class Finder:
    @staticmethod
    def find(pattern, root="."):
        results = list(Path(root).rglob(pattern))
        if not results:
            cprint(f"[FIND] No matches for '{pattern}' in '{root}'", Color.YELLOW)
        for r in results:
            cprint(f"[FIND] {r}", Color.CYAN)
        return results


# ============================================================================
# Duplicate Finder
# ============================================================================

class DuplicateFinder:
    @staticmethod
    def _hash_file(path: Path, chunk_size=8192) -> str:
        """Compute MD5 hash of a file."""
        hasher = hashlib.md5()
        try:
            with open(path, "rb") as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except (IOError, OSError) as e:
            cprint(f"[WARN] Cannot read {path}: {e}", Color.YELLOW)
            return ""

    @staticmethod
    def find_duplicates(root: Path) -> List[List[Path]]:
        """Return list of duplicate file groups (each group has at least 2 files)."""
        if not root.is_dir():
            cprint(f"[ERROR] {root} is not a directory", Color.RED)
            return []

        # Step 1: group by file size (fast filter)
        size_map: Dict[int, List[Path]] = {}
        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue
            try:
                size = file_path.stat().st_size
                size_map.setdefault(size, []).append(file_path)
            except OSError:
                continue

        # Step 2: for each size group with more than one file, hash them
        duplicates: Dict[str, List[Path]] = {}
        for size, files in size_map.items():
            if len(files) < 2:
                continue
            hash_map: Dict[str, List[Path]] = {}
            for f in files:
                h = DuplicateFinder._hash_file(f)
                if h:
                    hash_map.setdefault(h, []).append(f)
            for h, group in hash_map.items():
                if len(group) > 1:
                    # Use (size, hash) as key to avoid collisions
                    key = f"{size}:{h}"
                    duplicates.setdefault(key, []).extend(group)

        # Return only groups with >=2 files
        return [group for group in duplicates.values() if len(group) >= 2]

    @staticmethod
    def interactive_handle_duplicates(duplicate_groups: List[List[Path]], dry_run: bool):
        """For each group, ask user what to do: keep all, delete all but one, or move duplicates."""
        if not duplicate_groups:
            cprint("No duplicate files found.", Color.GREEN)
            return

        total_groups = len(duplicate_groups)
        for idx, group in enumerate(duplicate_groups, 1):
            cprint(f"\n--- Duplicate group {idx}/{total_groups} ---", Color.CYAN)
            for i, f in enumerate(group):
                cprint(f"  {i+1}. {f}", Color.BLUE)

            # Show actions
            cprint("\nOptions:", Color.YELLOW)
            cprint("  [k] Keep all (do nothing)", Color.GREEN)
            cprint("  [d] Delete duplicates (keep only the first file)", Color.RED)
            cprint("  [m] Move duplicates to a folder", Color.BLUE)

            while True:
                choice = input("Your choice (k/d/m): ").strip().lower()
                if choice in ('k', 'd', 'm'):
                    break
                cprint("Invalid choice. Please enter k, d, or m.", Color.RED)

            if choice == 'k':
                cprint("Keeping all files in this group.", Color.GREEN)
                continue

            elif choice == 'd':
                # Keep the first file, delete all others
                keep = group[0]
                to_delete = group[1:]
                cprint(f"Keeping: {keep}", Color.GREEN)
                for f in to_delete:
                    FileOps.delete_file(f, dry_run)

            elif choice == 'm':
                dest = input("Enter destination folder for duplicates: ").strip()
                if not dest:
                    cprint("No destination provided, skipping group.", Color.YELLOW)
                    continue
                dest_path = Path(dest).expanduser().resolve()
                if not dry_run:
                    dest_path.mkdir(parents=True, exist_ok=True)
                keep = group[0]
                to_move = group[1:]
                cprint(f"Keeping: {keep}", Color.GREEN)
                for f in to_move:
                    FileOps.move_file(f, dest_path, dry_run)

        cprint("\nDuplicate handling completed.", Color.GREEN)


# ============================================================================
# For Loop Engine
# ============================================================================

class ForLoop:
    _placeholders: Dict[str, Callable[[Path], str]] = {
        '{}': lambda p: shlex.quote(str(p)),
        '{/}': lambda p: shlex.quote(p.name),
        '{.}': lambda p: shlex.quote(p.stem),
        '{..}': lambda p: shlex.quote(p.parent.name),
        '{abs}': lambda p: shlex.quote(str(p.resolve())),
    }

    @staticmethod
    def _substitute_placeholders(command_template: str, path: Path) -> str:
        def replacer(match):
            key = match.group(0)
            if key in ForLoop._placeholders:
                return ForLoop._placeholders[key](path)
            cprint(f"[WARN] Unknown placeholder: {key}", Color.YELLOW)
            return key

        return re.sub(r'\{[^}]+\}', replacer, command_template)

    @staticmethod
    def _substitute_variable(command_template: str, var_name: str, quoted_path: str) -> str:
        return re.sub(rf'\b{re.escape(var_name)}\b', quoted_path, command_template)

    @staticmethod
    def run(var_name: str, pattern: str, command_template: str, executor: Executor):
        matches = glob.glob(pattern, recursive=True)

        if not matches:
            cprint(f"No matches found for pattern '{pattern}'", Color.YELLOW)
            return

        has_placeholder = bool(re.search(r'\{[^}]+\}', command_template))

        for match in matches:
            path = Path(match)

            if has_placeholder:
                cmd_str = ForLoop._substitute_placeholders(command_template, path)
            else:
                quoted = shlex.quote(str(path))
                cmd_str = ForLoop._substitute_variable(command_template, var_name, quoted)

            try:
                cmd_args = shlex.split(cmd_str)
            except ValueError as e:
                cprint(f"[ERROR] Invalid command: {cmd_str} ({e})", Color.RED)
                continue

            executor.run_cmd(cmd_args)


# ============================================================================
# Tree Command (Detailed Directory Tree) - MODIFIED with blank lines
# ============================================================================

class TreeDisplay:
    @staticmethod
    def _mode_to_str(mode: int) -> str:
        """Convert st_mode to permission string like 'rwxr-xr-x'."""
        perms = []
        for who in ("USR", "GRP", "OTH"):
            for what in ("R", "W", "X"):
                bit = getattr(stat, f"S_I{what}{who}", 0)
                perms.append(what.lower() if mode & bit else "-")
        return "".join(perms)

    @staticmethod
    def _get_file_info(path: Path) -> str:
        """Return a compact string with file metadata."""
        try:
            st = path.lstat()  # do not follow symlinks
            mode = st.st_mode
            size = st.st_size
            perms = TreeDisplay._mode_to_str(mode)

            # owner and group names
            try:
                owner = pwd.getpwuid(st.st_uid).pw_name
            except (KeyError, ImportError):
                owner = str(st.st_uid)
            try:
                group = grp.getgrgid(st.st_gid).gr_name
            except (KeyError, ImportError):
                group = str(st.st_gid)

            mtime = datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

            info = f"size={size}, perms={perms}, owner={owner}, group={group}, modified={mtime}"

            if path.is_symlink():
                try:
                    target = os.readlink(path)
                except OSError:
                    target = "?"
                info = f"link -> {target}, {info}"

            return f"[{info}]"
        except Exception as e:
            return f"[error: {e}]"

    @staticmethod
    def _tree_lines(path: Path, prefix: str = "", is_last: bool = True) -> List[str]:
        """Recursively build tree lines for a given path."""
        lines = []
        # current node
        node_name = path.name if path.name else str(path)  # root case
        if path.is_symlink():
            node_name += "@"
        elif path.is_dir():
            node_name += "/"

        info = TreeDisplay._get_file_info(path)
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{node_name} {info}")

        if path.is_dir() and not path.is_symlink():  # do not descend into symlink directories
            try:
                children = list(path.iterdir())
            except PermissionError:
                lines.append(f"{prefix}{'    ' if is_last else '│   '}[Permission denied]")
                return lines

            # sort: directories first (real dirs only), then symlinks, then regular files
            def sort_key(p: Path):
                if p.is_dir() and not p.is_symlink():
                    return (0, p.name.lower())
                elif p.is_symlink():
                    return (1, p.name.lower())
                else:
                    return (2, p.name.lower())

            children.sort(key=sort_key)
            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                new_prefix = prefix + ("    " if is_last else "│   ")
                lines.extend(TreeDisplay._tree_lines(child, new_prefix, is_last_child))
        return lines

    @staticmethod
    def display(root: Path):
        """Print the tree starting at root."""
        if not root.exists():
            cprint(f"[ERROR] Path does not exist: {root}", Color.RED)
            return

        # Print root line without connector
        root_name = root.name if root.name else str(root)
        if root.is_symlink():
            root_name += "@"
        elif root.is_dir():
            root_name += "/"
        info = TreeDisplay._get_file_info(root)
        print(f"{root_name} {info}")
        print()   # blank line after root for better readability

        if root.is_dir() and not root.is_symlink():
            try:
                children = list(root.iterdir())
            except PermissionError:
                cprint("[Permission denied]", Color.YELLOW)
                return

            def sort_key(p: Path):
                if p.is_dir() and not p.is_symlink():
                    return (0, p.name.lower())
                elif p.is_symlink():
                    return (1, p.name.lower())
                else:
                    return (2, p.name.lower())
            children.sort(key=sort_key)

            for i, child in enumerate(children):
                is_last = (i == len(children) - 1)
                lines = TreeDisplay._tree_lines(child, "", is_last)
                for line in lines:
                    print(line)
                    print()   # blank line after each tree entry


# ============================================================================
# Main EasyBash
# ============================================================================

class EasyBash:
    def __init__(self):
        self.executor = Executor()

    def help(self, line):
        parts = shlex.split(line)

        if len(parts) == 1:
            cprint("Available commands:", Color.CYAN)
            for cmd in HELP:
                cprint(f"  {cmd} - {HELP[cmd]['desc']}", Color.GREEN)
            cprint("Use: help <command>", Color.YELLOW)
            return

        cmd = parts[1]
        if cmd in HELP:
            info = HELP[cmd]
            cprint(f"{cmd}", Color.CYAN)
            cprint(f"Usage: {info['usage']}", Color.GREEN)
            cprint(f"Description: {info['desc']}", Color.BLUE)
            cprint(f"Example: {info['example']}", Color.YELLOW)
        else:
            cprint(f"[ERROR] No help for '{cmd}'", Color.RED)

    def copy(self, line):
        parts = shlex.split(line)
        if len(parts) < 4 or parts[2] != 'to':
            cprint("[ERROR] Usage: copy SRC to DST1|DST2", Color.RED)
            return
        FileOps.copy(parts[1], parts[3].split('|'))

    def move(self, line):
        parts = shlex.split(line)
        if len(parts) < 4 or parts[2] != 'to':
            cprint("[ERROR] Usage: move SRC to DST1|DST2", Color.RED)
            return
        FileOps.move(parts[1], parts[3].split('|'))

    def find(self, line):
        parts = shlex.split(line)
        if len(parts) < 2:
            cprint("[ERROR] Usage: find PATTERN [ROOT]", Color.RED)
            return
        Finder.find(parts[1], parts[2] if len(parts) > 2 else ".")

    def finddup(self, line):
        parts = shlex.split(line)
        root = parts[1] if len(parts) > 1 else "."
        root_path = Path(root).expanduser().resolve()
        if not root_path.is_dir():
            cprint(f"[ERROR] '{root}' is not a valid directory", Color.RED)
            return

        cprint(f"Scanning for duplicates in: {root_path}", Color.CYAN)
        duplicate_groups = DuplicateFinder.find_duplicates(root_path)
        DuplicateFinder.interactive_handle_duplicates(duplicate_groups, self.executor.dry_run)

    def tree(self, line):
        """Execute 'tree' command."""
        parts = shlex.split(line)
        root = parts[1] if len(parts) > 1 else "."
        path = Path(root).expanduser().resolve()
        TreeDisplay.display(path)

    def update(self, line):
        """Update EasyBash via git pull from the official repository."""
        if self.executor.dry_run:
            cprint("[DRY-RUN] Would run: git pull https://github.com/sonych995-byte/EasyBash.git", Color.YELLOW)
            return

        # ไดเรกทอรีที่เก็บสคริปต์ปัจจุบัน (EasyBash)
        script_dir = Path(__file__).parent.resolve()
        cprint(f"Updating EasyBash from {script_dir}...", Color.CYAN)

        try:
            # ใช้ git pull พร้อม remote URL โดยตรง (ไม่ต้องพึ่งพา origin)
            result = subprocess.run(
                ["git", "pull", "https://github.com/sonych995-byte/EasyBash.git"],
                cwd=script_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                cprint("✅ Update successful!", Color.GREEN)
                if result.stdout:
                    cprint(result.stdout, Color.CYAN)
            else:
                cprint(f"❌ Update failed with code {result.returncode}", Color.RED)
                if result.stderr:
                    cprint(result.stderr, Color.RED)
        except subprocess.TimeoutExpired:
            cprint("[ERROR] Git operation timed out", Color.RED)
        except FileNotFoundError:
            cprint("[ERROR] 'git' command not found. Please install Git.", Color.RED)
        except Exception as e:
            cprint(f"[ERROR] {e}", Color.RED)

    def run(self, raw):
        raw = raw.strip()
        if not raw:
            return

        tokens = shlex.split(raw)
        if not tokens:
            return

        cmd = tokens[0]

        if cmd == "help":
            return self.help(raw)

        if raw == "dry on":
            self.executor.dry_run = True
            cprint("[DRY RUN ON]", Color.YELLOW)
            return
        if raw == "dry off":
            self.executor.dry_run = False
            cprint("[DRY RUN OFF]", Color.YELLOW)
            return

        if cmd == "copy":
            return self.copy(raw)
        if cmd == "move":
            return self.move(raw)
        if cmd == "find":
            return self.find(raw)
        if cmd == "finddup":
            return self.finddup(raw)
        if cmd == "tree":
            return self.tree(raw)
        if cmd == "update":
            return self.update(raw)

        if cmd == "for" and "=>" in raw:
            left, right = raw.split("=>", 1)
            tokens = shlex.split(left)
            if len(tokens) != 4 or tokens[2] != "in":
                cprint("[ERROR] Usage: for VAR in PATTERN => COMMAND", Color.RED)
                return
            ForLoop.run(tokens[1], tokens[3], right.strip(), self.executor)
            return

        if '|' in cmd:
            self.executor.parallel(cmd.split('|'), tokens[1:])
        elif '>' in cmd:
            self.executor.chain(cmd.split('>'), tokens[1:])
        else:
            self.executor.single(tokens)


# ============================================================================
# ENTRY
# ============================================================================

if __name__ == "__main__":
    eb = EasyBash()

    cprint("EasyBash v6.4.1 🚀", Color.CYAN)

    while True:
        try:
            cmd = input("EasyBash> ")
            if cmd.strip() == "exit":
                break
            eb.run(cmd)
        except KeyboardInterrupt:
            print()
            break
        except Exception as e:
            cprint(f"[ERROR] {e}", Color.RED)
