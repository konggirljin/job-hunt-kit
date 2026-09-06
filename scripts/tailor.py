#!/usr/bin/env python3
"""Config-driven CV tailor: copies your master CV and applies per-job edits.

Run:  python scripts/tailor.py <jobid> [--profile profile/tailor.json]
Config lives in <config_dir>/<jobid>.json (see template/tailoring-configs/).

Lessons baked in (see docs/one-page-cv-playbook.md):
- New runs MUST copy rPr from a real body run, else they inherit the doc
  default font (e.g. Calibri 12pt instead of Times New Roman 11pt) -> taller
  lines -> the one-page budget breaks even at the same paragraph count.
- Any CV has an exact line budget = 1 page. Verify with Word doc-level
  ComputeStatistics(2) pages / ComputeStatistics(1) lines (or
  scripts/verify_one_page.py). Per-paragraph stats DISAGREE with doc-level
  stats (they skip table lines) - only trust doc-level.
- Bullet edits: set_text() preserves run formatting; keep replacement text
  short enough that the paragraph wraps to the SAME number of lines.
"""
import argparse
import copy
import json
import os
import sys

import docx
from docx.oxml.ns import qn

ANCHORS = {
    "contact_line": "Email:",
    "section_header": "EDUCATION",
    "body_line": "Bachelor of",
    "personal_projects_header": "PERSONAL PROJECTS",
    "job_header_table": "",
    "project_title_prefix": "Project 1",
    "project_prefix": "Project ",
}

SRC = None
OUT_DIR = "tailored"
CONFIG_DIR = "tailoring-configs"

INVALID_CHARS = '\\/:*?"<>|'


def sanitize_filename(name):
    return "".join(" " if c in INVALID_CHARS else c for c in name).strip()


def output_name(name, config):
    company = config.get("company", "").strip()
    position = config.get("position", "").strip()
    if company and position:
        return f"{sanitize_filename(name)}_{sanitize_filename(company)} {sanitize_filename(position)}.docx"
    return "tailored.docx"


def load_config(jobid):
    path = os.path.join(CONFIG_DIR, f"{jobid}.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_doc(config):
    doc = docx.Document(SRC)
    body = doc.element.body
    return doc, body


def el_text(el):
    return "".join(t.text or "" for t in el.iter() if t.tag.endswith("}t"))


def find_para_el(body, prefix):
    for el in body:
        if el.tag.endswith("}p") and el_text(el).startswith(prefix):
            return el
    raise RuntimeError(f"paragraph not found starting with: {prefix!r} "
                       f"(check the 'anchors' in your profile/tailor.json)")


def make_para(template_el, text):
    """New paragraph with a single run carrying the template's run formatting."""
    new = copy.deepcopy(template_el)
    for r in list(new):
        if r.tag.endswith("}r") or r.tag.endswith("}hyperlink"):
            new.remove(r)
    run = new.makeelement(qn("w:r"), {})
    t = new.makeelement(qn("w:t"), {})
    t.text = text
    t.set(qn("xml:space"), "preserve")
    run.append(t)
    for r in template_el.iter(qn("w:r")):
        rpr = r.find(qn("w:rPr"))
        if rpr is not None:
            run.insert(0, copy.deepcopy(rpr))
            break
    new.append(run)
    return new


def set_text(el, text):
    """Replace a paragraph's text, keeping its run formatting."""
    rpr_tpl = None
    for r in el.iter(qn("w:r")):
        rpr = r.find(qn("w:rPr"))
        if rpr is not None:
            rpr_tpl = copy.deepcopy(rpr)
            break
    for r in list(el):
        if r.tag.endswith("}r") or r.tag.endswith("}hyperlink"):
            el.remove(r)
    run = el.makeelement(qn("w:r"), {})
    t = el.makeelement(qn("w:t"), {})
    t.text = text
    t.set(qn("xml:space"), "preserve")
    run.append(t)
    if rpr_tpl is not None:
        run.insert(0, rpr_tpl)
    el.append(run)


def get_block(start_el):
    """Sibling elements from start_el until the next project title or the
    personal-projects header."""
    els = []
    cur = start_el
    while cur is not None:
        tag = cur.tag
        if cur is not start_el and tag.endswith("}p"):
            txt = el_text(cur)
            if txt.startswith(ANCHORS["project_prefix"]) or txt.startswith(
                ANCHORS["personal_projects_header"]
            ):
                break
        els.append(cur)
        cur = cur.getnext()
        if cur is not None and cur.tag.endswith("}sectPr"):
            break
    return els


def find_body_template(body):
    """First paragraph starting with the configured body_line anchor."""
    for el in body:
        if el.tag.endswith("}p") and el_text(el).strip().startswith(ANCHORS["body_line"]):
            return el
    raise RuntimeError(f"body template not found (body_line anchor: {ANCHORS['body_line']!r})")


def apply_summary_skills(doc, body, config):
    contact = find_para_el(body, ANCHORS["contact_line"])
    header_tpl = find_para_el(body, ANCHORS["section_header"])
    body_tpl = find_body_template(body)
    header = make_para(header_tpl, "PROFESSIONAL SUMMARY")
    text = make_para(body_tpl, config["summary"])
    sk_header = make_para(header_tpl, "SKILLS")
    sk_text = make_para(body_tpl, config["skills"])
    # addnext reverses order, so insert text-then-header per section
    contact.addnext(sk_text)
    contact.addnext(sk_header)
    contact.addnext(text)
    contact.addnext(header)


def apply_reorder(doc, body, config):
    """Reorder projects by the desired order in config['project_order'].
    Each entry is {find: <current title prefix>, title: <new title>}."""
    pairs = []
    for item in config["project_order"]:
        start = find_para_el(body, item["find"])
        pairs.append((get_block(start), item["title"]))
    for blk, title in pairs:
        set_text(blk[0], title)
    for blk, _ in pairs:
        for el in blk:
            body.remove(el)
    personal = find_para_el(body, ANCHORS["personal_projects_header"])
    for blk, _ in pairs:
        for el in blk:
            personal.addprevious(el)


def apply_bullet_reword(doc, body, config):
    """config['reword']: list of {find: <para prefix>, text: <new text>}"""
    for item in config.get("reword", []):
        el = find_para_el(body, item["find"])
        set_text(el, item["text"])


def apply_first_bullet(doc, body, config):
    """config['first_bullet']: {title: <project title prefix>, text: <new text>}
    Replaces the first content bullet after the project's Role line (stays
    within the block - stops at the next project title)."""
    for item in config.get("first_bullet", []):
        title = find_para_el(body, item["title"])
        role_seen = False
        for el in title.itersiblings():
            if el.tag.endswith("}p"):
                txt = el_text(el).strip()
                if txt.startswith(ANCHORS["project_prefix"]):
                    break
                if txt.startswith("Role:"):
                    role_seen = True
                    continue
                if role_seen and txt:
                    repl = make_para(el, item["text"])
                    el.getparent().replace(el, repl)
                    break


def apply_remove_paras(doc, body, config):
    """config['remove_paras']: list of {find: <para prefix>}
    Removes every paragraph whose text starts with the prefix."""
    for item in config.get("remove_paras", []):
        for el in list(body):
            if el.tag.endswith("}p") and el_text(el).startswith(item["find"]):
                body.remove(el)


def apply_remove_personal_blocks(doc, body, config):
    """config['remove_personal_blocks']: list of <table title prefix>
    Removes a personal-project block: the title table + its bullet paragraphs
    (until the next table / sectPr), plus any trailing blank spacer."""
    def tbl_cells(tbl):
        out = []
        for tr in tbl.findall(qn("w:tr")):
            for tc in tr.findall(qn("w:tc")):
                txt = " ".join(
                    "".join(x.text or "" for x in tc.iter() if x.tag.endswith("}t")).split()
                )
                out.append(txt)
        return " | ".join(out)

    for prefix in config.get("remove_personal_blocks", []):
        for tbl in list(body):
            if not tbl.tag.endswith("}tbl"):
                continue
            if prefix not in tbl_cells(tbl):
                continue
            nxt = tbl.getnext()
            tbl.getparent().remove(tbl)
            while nxt is not None and not nxt.tag.endswith("}tbl") and not nxt.tag.endswith("}sectPr"):
                nn = nxt.getnext()
                nxt.getparent().remove(nxt)
                nxt = nn
            break


def apply_insert(doc, body, config):
    """config['insert_after']: list of {find: <para prefix>, text: <new text>}
    Inserts a new paragraph (body formatting) directly after the matched paragraph."""
    body_tpl = find_body_template(body)
    for item in config.get("insert_after", []):
        el = find_para_el(body, item["find"])
        new_para = make_para(body_tpl, item["text"])
        el.addnext(new_para)


def apply_insert_block(doc, body, config):
    """config['insert_block_before']: list of
    {find: <prefix of para to insert before>, title: <block title>,
     bullets: [<bullet texts>]}
    Inserts a titled block of body bullets immediately before the matched para."""
    title_tpl = None
    for el in body:
        if el.tag.endswith("}p") and el_text(el).strip().startswith(ANCHORS["project_title_prefix"]):
            title_tpl = el
            break
    if title_tpl is None:
        raise RuntimeError(
            f"insert_block title template not found "
            f"(project_title_prefix anchor: {ANCHORS['project_title_prefix']!r})"
        )
    body_tpl = find_body_template(body)
    bullet_tpl = find_bullet_template(body)
    for item in config.get("insert_block_before", []):
        target = find_para_el(body, item["find"])
        paras = [make_para(title_tpl, item["title"])]
        paras += [make_para(bullet_tpl, b) for b in item.get("bullets", [])]
        for p in paras:
            target.addprevious(p)


def find_bullet_template(body):
    """First body paragraph that carries a bullet numPr. Used whenever we
    CREATE a bulleted line from scratch. A plain body template has NO numPr ->
    new lines built from it render WITHOUT bullet glyphs."""
    for el in body:
        if el.tag.endswith("}p"):
            ppr = el.find(qn("w:pPr"))
            if ppr is not None and ppr.find(qn("w:numPr")) is not None:
                return el
    raise RuntimeError("no bullet template paragraph found")


def find_table_el(body, contains):
    """First table whose cell text contains a substring (like a job-header
    table). Empty substring -> first table in the body."""
    for el in body:
        if el.tag.endswith("}tbl"):
            if not contains:
                return el
            text = " ".join(
                "".join(t.text or "" for t in el.iter() if t.tag.endswith("}t")).split()
            )
            if contains in text:
                return el
    raise RuntimeError(f"table not found containing: {contains!r}")


def set_table_cell_text(table_el, cell_index, text):
    """Replace the text of the first paragraph in a table cell, keeping the
    cell paragraph's run formatting (e.g. bold navy job headers)."""
    tr = table_el.findall(qn("w:tr"))[0]
    tc = tr.findall(qn("w:tc"))[cell_index]
    p = tc.findall(qn("w:p"))[0]
    set_text(p, text)


def apply_insert_job(doc, body, config):
    """config['insert_job_before']: list of
    {find: <para prefix to insert before>, title: <company, role>, date: <date>,
     bullets: [<bullet texts>]}
    Inserts a SEPARATE JOB ENTRY styled like an existing company header table
    (job_header_table anchor; empty -> first table), followed by REAL bulleted
    paragraphs."""
    job_tbl = find_table_el(body, ANCHORS["job_header_table"])
    bullet_tpl = find_bullet_template(body)
    for item in config.get("insert_job_before", []):
        target = find_para_el(body, item["find"])
        new_tbl = copy.deepcopy(job_tbl)
        set_table_cell_text(new_tbl, 0, item["title"])
        set_table_cell_text(new_tbl, 1, item.get("date", ""))
        target.addprevious(new_tbl)
        for b in item.get("bullets", []):
            target.addprevious(make_para(bullet_tpl, b))


def apply_insert_bullet(doc, body, config):
    """config['insert_bullet_after']: list of {find: <para prefix>, text: <new bullet>}
    Inserts a BULLETED paragraph directly after the matched paragraph (uses a
    real bullet as formatting template so the glyph survives)."""
    bullet_tpl = find_bullet_template(body)
    for item in config.get("insert_bullet_after", []):
        el = find_para_el(body, item["find"])
        new_para = make_para(bullet_tpl, item["text"])
        el.addnext(new_para)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jobid")
    parser.add_argument("--profile", default=os.path.join("profile", "tailor.json"))
    args = parser.parse_args()

    global CONFIG_DIR, OUT_DIR, SRC
    with open(args.profile, encoding="utf-8") as f:
        prof = json.load(f)
    ANCHORS.update(prof.get("anchors", {}))
    CONFIG_DIR = prof.get("config_dir", CONFIG_DIR)
    OUT_DIR = prof.get("out_dir", OUT_DIR)
    SRC = prof["source_cv"]

    config = load_config(args.jobid)
    doc, body = build_doc(config)
    apply_summary_skills(doc, body, config)
    apply_reorder(doc, body, config)
    apply_bullet_reword(doc, body, config)
    apply_first_bullet(doc, body, config)
    apply_insert(doc, body, config)
    apply_insert_bullet(doc, body, config)
    apply_insert_job(doc, body, config)
    apply_insert_block(doc, body, config)
    apply_remove_paras(doc, body, config)
    apply_remove_personal_blocks(doc, body, config)
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, output_name(prof.get("name", ""), config))
    doc.save(out)
    print(f"saved {out}")
    budget = prof.get("line_budget", 52)
    print(
        "NEXT: verify one page -> "
        f'python scripts/verify_one_page.py "{out}" --budget {budget} '
        "(or scripts/verify_one_page.ps1). See docs/one-page-cv-playbook.md"
    )


if __name__ == "__main__":
    main()
