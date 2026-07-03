#!/usr/bin/env python3
"""
Bygg hela kunskapsbasen till en enda PDF.

Slår ihop alla markdown-dokument i logisk ordning, konverterar interna
[[wikilänkar]] till läsbara referenser, gör bildsökvägar absoluta, och
renderar till PDF via pandoc + weasyprint.

Krav:  pandoc  och  weasyprint  (bägge på PATH).
Kör:   python3 verktyg/build_pdf.py
Ut:    Illuminatiorden-kunskapsbas.pdf  (i repo-roten)
"""
import re, subprocess, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
COMBINED = HERE / "combined.md"
STYLE = HERE / "style.css"
OUTPUT = ROOT / "Illuminatiorden-kunskapsbas.pdf"

ORDER = [
    "README.md",
    "01-oversikt.md", "02-adam-weishaupt.md", "03-ideologi-och-mal.md",
    "04-organisation-och-grader.md", "05-medlemmar.md", "06-frimureriet.md",
    "07-spridning.md", "08-forbud-och-fall.md", "09-eftermale-och-arv.md",
    "10-historia-vs-myt.md", "11-kallor.md", "12-originaldokument.md",
    "13-emblem-och-symboler.md", "14-religion.md",
    "primarkallor/README.md",
    "primarkallor/01-einige-originalschriften.md", "primarkallor/02-verbesserte-system.md",
    "primarkallor/03-grader-och-ritualer.md", "primarkallor/04-stadgarna-fullstandiga.md",
    "primarkallor/05-spartacus-breven.md", "primarkallor/06-nachtrag.md",
    "primarkallor/07-ritualer-hogupplost.md",
    "facsimiler/README.md",
    "bilder/reproduktioner/README.md",
]

def wikilink(m):
    tgt = m.group(1).split("|")[0].strip()
    label = tgt.split("/")[-1].replace("../", "")
    return f"»{label}«"                       # plain text, no markdown-special chars

def process(path):
    txt = path.read_text(encoding="utf-8")
    txt = "\n".join(l for l in txt.splitlines() if not l.startswith("←"))
    txt = re.sub(r"\[\[([^\]]+)\]\]", wikilink, txt)          # wikilinks -> »label«
    # absolutize local images (markdown ![]() and HTML <img src="">) to repo root
    txt = re.sub(r"\]\((?:\.\./)*(bilder/[^)]+)\)", lambda m: "](" + str(ROOT / m.group(1)) + ")", txt)
    txt = re.sub(r'src="(?:\.\./)*((?:bilder/|logo)[^"]+)"', lambda m: 'src="' + str(ROOT / m.group(1)) + '"', txt)
    return txt.strip()

def main():
    parts = []
    for rel in ORDER:
        p = ROOT / rel
        if p.exists():
            parts.append(process(p))
        else:
            print("SAKNAS:", rel, file=sys.stderr)
    COMBINED.write_text("\n\n\n".join(parts) + "\n", encoding="utf-8")

    cmd = [
        "pandoc", str(COMBINED),
        "-f", "markdown-yaml_metadata_block-simple_tables-multiline_tables",
        "-o", str(OUTPUT), "--pdf-engine=weasyprint",
        "--standalone", "--toc", "--toc-depth=2", "-c", str(STYLE),
        "--metadata", "title=Illuminatiorden i Bayern",
        "--metadata", "subtitle=En källbelagd svensk kunskapsbas med översatta primärkällor (1776–1787)",
        "--metadata", "author=Grundad på ordens egna beslagtagna och publicerade skrifter",
        "--metadata", "lang=sv",
    ]
    print("Kör:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("Klart ->", OUTPUT)

if __name__ == "__main__":
    main()
