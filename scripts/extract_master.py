#!/usr/bin/env python3
"""Sync the capability-inventory markdown from your master docx.

Run from repo root:  python scripts/extract_master.py [--profile profile/tailor.json]

Reads the docx matched by extract_docx_glob (profile/tailor.json) and writes
extract_out with a fixed header. Converts tables into markdown pipe-lines,
preserving paragraph/row order. Non-breaking spaces are normalized so
markdown rendering stays clean.

The output is the exhaustive capability list the agent MUST read before any
tailoring, gap call, or keyword check (alongside profile/context.md).
"""
import argparse
import glob
import json
import os

import docx
from docx.oxml.ns import qn

HEADER = """# Capability inventory (exhaustive master mirror)

> Machine-readable mirror of `{source}`.
> This IS the full skills/experience inventory - the exhaustive list of
> everything you have done, including raw detail that is NOT CV-suitable but
> tells the agent what you can honestly claim.
>
> **Mandatory read** before any tailoring, gap call, or compare (alongside
> `profile/context.md` and `profile/truthfulness.md`). If a JD term is not
> here AND not on the tailoring-base CV -> ASK the user; never assume a gap.
>
> **Sync rule:** when the source docx changes, re-run
> `python scripts/extract_master.py`. Do NOT hand-edit this file out of sync.

---
"""


def para_text(p):
    txt = "".join(t.text or "" for t in p.iter() if t.tag.endswith("}t"))
    return txt.replace("\xa0", " ").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default=os.path.join("profile", "tailor.json"))
    args = ap.parse_args()
    with open(args.profile, encoding="utf-8") as f:
        prof = json.load(f)

    pattern = prof.get("extract_docx_glob", "profile/cv/*MASTER*.docx")
    out_path = prof.get("extract_out", "profile/cv-master.md")
    docx_paths = sorted(glob.glob(pattern))
    if not docx_paths:
        raise SystemExit(f"No docx matched extract_docx_glob: {pattern}")
    source = docx_paths[0]
    doc = docx.Document(source)

    lines = []
    for el in doc.element.body:
        if el.tag.endswith("}p"):
            t = para_text(el)
            if t:
                lines.append(t)
        elif el.tag.endswith("}tbl"):
            for tr in el.findall(qn("w:tr")):
                cells = [
                    " ".join(para_text(tc).split())
                    for tc in tr.findall(qn("w:tc"))
                ]
                line = " | ".join(c for c in cells if c)
                if line:
                    lines.append(line)

    body = "\n".join(lines).strip()
    header = HEADER.format(source=source)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header + body + "\n")
    print(f"Wrote {out_path} ({len(lines)} lines) from {source}")


if __name__ == "__main__":
    main()
