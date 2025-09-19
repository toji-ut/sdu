#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
import argparse
from rich.console import Console
from rich.tree import Tree
from rich.table import Table
from rich import box

console = Console()

def human_readable(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"

def get_size(path: Path, max_depth: int = -1, current_depth: int = 0) -> int:
    if path.is_file():
        return path.stat().st_size
    elif path.is_dir():
        if max_depth != -1 and current_depth >= max_depth:
            return 0
        total = 0
        try:
            for child in path.iterdir():
                total += get_size(child, max_depth, current_depth + 1)
        except PermissionError:
            return total
        return total
    return 0

def scan_tree(path: Path, max_depth: int = -1, current_depth: int = 0, top_n: int = None) -> (Tree, dict):
    tree = Tree(f"[bold]{path.name}[/bold]", guide_style="bright_blue")
    type_summary = defaultdict(int)

    if path.is_dir():
        try:
            children = sorted(path.iterdir(), key=lambda c: c.stat().st_size, reverse=True)
        except PermissionError:
            return tree, type_summary

        if top_n:
            children = children[:top_n]

        for child in children:
            size = get_size(child, max_depth, current_depth)
            if size >= 1_000_000_000:
                color = "red"
            elif size >= 100_000_000:
                color = "yellow"
            else:
                color = "green"

            if child.is_file():
                tree.add(f"[{color}]{child.name}[/] ({human_readable(size)})")
                type_summary[child.suffix] += size
            elif child.is_dir():
                if max_depth == -1 or current_depth < max_depth:
                    subtree, sub_summary = scan_tree(child, max_depth, current_depth + 1, top_n)
                    tree.add(subtree)
                    for ext, s in sub_summary.items():
                        type_summary[ext] += s
    return tree, type_summary

def print_summary(type_summary: dict):
    table = Table(title="\nDisk Usage by File Type", box=box.SIMPLE_HEAVY)
    table.add_column("Extension")
    table.add_column("Size", justify="right")
    for ext, size in sorted(type_summary.items(), key=lambda x: x[1], reverse=True):
        table.add_row(ext or "[no ext]", human_readable(size))
    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="sdu - Smart Disk Usage")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("--top", type=int, default=None, help="Show top N items per folder")
    parser.add_argument("--depth", type=int, default=-1, help="Max directory depth (-1 = unlimited)")
    parser.add_argument("--summary", action="store_true", help="Show summary by file type")
    args = parser.parse_args()

    path = Path(args.directory)
    tree, type_summary = scan_tree(path, args.depth, top_n=args.top)
    console.print(tree)
    if args.summary:
        print_summary(type_summary)

if __name__ == "__main__":
    main()
