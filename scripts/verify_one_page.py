#!/usr/bin/env python3
"""Verify a docx fits one page, using Word doc-level statistics.

Run:  python scripts/verify_one_page.py <file.docx> [--budget 52]
Exit 0 = 1 page within budget; exit 1 = over. Windows + Word required.
Requires pywin32 (pip install pywin32). PowerShell alternative without any
dependency: scripts/verify_one_page.ps1
"""
import argparse
import os
import sys

try:
    import win32com.client as win32
except ImportError:
    sys.exit("pywin32 not installed: pip install pywin32 (Windows + Word required). "
             "Or use scripts/verify_one_page.ps1")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--budget", type=int, default=52,
                    help="max lines for one page (your profile line_budget)")
    a = ap.parse_args()

    path = os.path.abspath(a.docx)
    if not os.path.exists(path):
        sys.exit(f"file not found: {path}")

    word = win32.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(path, ReadOnly=True)
        # Doc-level stats are the only trustworthy ones: per-paragraph
        # ComputeStatistics skips table lines, doc-level includes them.
        lines = doc.Range().ComputeStatistics(1)   # wdStatisticLines
        pages = doc.ComputeStatistics(2)           # wdStatisticPages
        doc.Close(False)
    finally:
        word.Quit()

    print(f"pages={pages} lines={lines} budget={a.budget}")
    if pages == 1 and lines <= a.budget:
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
