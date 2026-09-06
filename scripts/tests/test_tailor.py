#!/usr/bin/env python3
"""End-to-end smoke test for scripts/tailor.py.

Builds the fixture docx, assembles a temp workspace (profile + config),
runs tailor.py as a subprocess, and asserts the output docx content.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(HERE))  # kit root
sys.path.insert(0, HERE)

import make_fixture_docx  # noqa: E402

import docx  # noqa: E402

PROFILE = {
    "name": "Test User",
    "source_cv": "profile/cv/master.docx",
    "config_dir": "tailoring-configs",
    "out_dir": "tailored",
    "line_budget": 52,
    "anchors": {
        "contact_line": "Email:",
        "section_header": "EDUCATION",
        "body_line": "Bachelor of",
        "personal_projects_header": "PERSONAL PROJECTS",
        "job_header_table": "ACME Corp",
        "project_title_prefix": "Project 1",
        "project_prefix": "Project ",
    },
    "extract_docx_glob": "profile/cv/*MASTER*.docx",
    "extract_out": "profile/cv-master.md",
}

CONFIG = {
    "company": "Test Corp",
    "position": "QA Analyst",
    "summary": "QA analyst with fixture-grade experience.",
    "skills": "Testing, Python, Attention to detail",
    "project_order": [
        {"find": "Project 2 - Bar", "title": "Project 1 - Bar"},
        {"find": "Project 1 - Foo", "title": "Project 2 - Foo"},
    ],
    "reword": [{"find": "did a thing", "text": "did a REWRITTEN thing"}],
    "first_bullet": [{"title": "Project 1 - Bar", "text": "rewritten lead bullet"}],
}


def para_texts(doc):
    return [
        "".join(t.text or "" for t in p._element.iter() if t.tag.endswith("}t"))
        for p in doc.paragraphs
    ]


def main():
    make_fixture_docx.build()
    tmp = tempfile.mkdtemp(prefix="kit-tailor-test-")
    try:
        os.makedirs(os.path.join(tmp, "profile", "cv"))
        os.makedirs(os.path.join(tmp, "tailoring-configs"))
        shutil.copy(
            os.path.join(HERE, "fixture-master.docx"),
            os.path.join(tmp, "profile", "cv", "master.docx"),
        )
        prof = dict(PROFILE)
        prof["anchors"] = dict(PROFILE["anchors"], job_header_table="ACME Corp")
        with open(os.path.join(tmp, "profile", "tailor.json"), "w", encoding="utf-8") as f:
            json.dump(prof, f)
        with open(os.path.join(tmp, "tailoring-configs", "test-job.json"), "w", encoding="utf-8") as f:
            json.dump(CONFIG, f)

        r = subprocess.run(
            [sys.executable, os.path.join(KIT, "scripts", "tailor.py"), "test-job"],
            cwd=tmp, capture_output=True, text=True,
        )
        assert r.returncode == 0, f"tailor.py failed:\n{r.stdout}\n{r.stderr}"
        print(r.stdout.strip())

        out = os.path.join(tmp, "tailored", "Test User_Test Corp QA Analyst.docx")
        assert os.path.exists(out), f"output missing: {out}"
        doc = docx.Document(out)
        texts = para_texts(doc)
        assert any(t.startswith("PROFESSIONAL SUMMARY") for t in texts), "summary header missing"
        assert any("SKILLS" in t for t in texts), "skills header missing"
        assert any("did a REWRITTEN thing" in t for t in texts), "reword not applied"
        assert any("rewritten lead bullet" in t for t in texts), "first_bullet not applied"
        # reorder: Project 1 - Bar block must come before Project 2 - Foo
        i_bar = next(i for i, t in enumerate(texts) if t.startswith("Project 1 - Bar"))
        i_foo = next(i for i, t in enumerate(texts) if t.startswith("Project 2 - Foo"))
        assert i_bar < i_foo, "project order not applied"
        print("PASS: tailor.py end-to-end")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
