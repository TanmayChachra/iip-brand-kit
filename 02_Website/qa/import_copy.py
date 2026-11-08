"""Import 06_Content/website-copy/*.md into the Astro site content (02_Website/site/src/content).
Keeps the site's own structural frontmatter (pageType, place, cta, schema), takes words from the copy files.
Phones become tokens ({{phone1}} etc.) so one file (src/lib/phones.mjs) swaps a number everywhere.
Owner placeholders are resolved (answered ones) or removed (open ones) and logged to qa/import-log.md.
Run: python 02_Website/qa/import_copy.py"""
import pathlib, re, yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
COPY = ROOT / "06_Content/website-copy"
SITE = ROOT / "02_Website/site/src/content"
LOG = []

HOURS = "Open 8 am to 8 pm every day except Tuesday."
ANSWERS = [  # (regex on the placeholder text, replacement) for questions the owner has answered
    (r"price|rate|contact for price|starting price", "Contact for price"),
    (r"hours|time|visiting", HOURS),
    (r"whatsapp", "{{phone1}}"),
]


def tokens(t):
    t = t.replace("+919837057800", "{{phone1_tel}}").replace("+919219549800", "{{phone2_tel}}").replace("+919837764222", "{{phone2_tel}}")
    t = t.replace("919837057800", "{{wa}}").replace("98370 57800", "{{phone1}}").replace("9837057800", "{{phone1}}")
    t = t.replace("92195 49800", "{{phone2}}").replace("9219549800", "{{phone2}}").replace("98377 64222", "{{phone2}}").replace("9837764222", "{{phone2}}")
    return t


PH = re.compile(r"\[OWNER TO CONFIRM[^\]]*\]")


def resolve(text, name):
    out = []
    for line in text.split("\n"):
        if not PH.search(line):
            out.append(line); continue
        if line.lstrip().startswith("|"):
            LOG.append(f"{name}: dropped table row: {line[:100]}"); continue
        def sub(m):
            inner = m.group(0)
            for rx, rep in ANSWERS:
                if re.search(rx, inner, re.I):
                    LOG.append(f"{name}: answered '{inner[:60]}' -> {rep[:40]}"); return rep
            LOG.append(f"{name}: removed '{inner[:70]}'"); return ""
        new = PH.sub(sub, line)
        new = re.sub(r"\s+([.,;:])", r"\1", new); new = re.sub(r"  +", " ", new).rstrip()
        # a list item or label left empty after removal is dropped
        if re.match(r"^(\s*[-*]|\s*\d+\.)?\s*(\*\*[^*]+\*\*)?:?\s*[.:]?$", new):
            LOG.append(f"{name}: dropped empty line: {line[:90]}"); continue
        out.append(new)
    return "\n".join(out)


def split(path):
    s = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", s, re.S)
    return yaml.safe_load(m.group(1)), m.group(2).strip()


def first_para(body):
    for blk in re.split(r"\n\s*\n", body):
        b = blk.strip()
        if b and not b.startswith(("#", "[", "|", "-", "*", "1.")): return b, body.replace(blk, "", 1).strip()
    return "", body


def faq_from(body):
    qs = re.findall(r"^### (.+?)\n(.*?)(?=^### |^## |\Z)", body, re.S | re.M)
    return [{"q": q.strip(), "a": re.sub(r"\s+", " ", a).strip()} for q, a in qs]


def fm(d): return "---\n" + yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=1000) + "---\n\n"


def target_for(stem):
    if stem == "index": return SITE / "pages/home.md"
    if stem.startswith("blog__"): return SITE / f"posts/{stem[6:]}.md"
    if stem.startswith("location__"): return SITE / f"pages/location/{stem[10:]}.md"
    return SITE / f"pages/{stem}.md"


def main():
    n = 0
    for f in sorted(COPY.glob("*.md")):
        stem = f.stem
        if stem in ("placeholders", "blog", "404", "neighbours"): continue  # neighbours is hand written from verified Maps data
        tgt = target_for(stem)
        if not tgt.exists() and not stem.startswith("blog__"): continue
        cfm, body = split(f)
        body = resolve(tokens(body), stem)
        title, desc, h1 = (tokens(str(cfm[k])) for k in ("title", "description", "h1"))
        title, desc, h1 = (PH.sub("", x).strip() for x in (title, desc, h1))
        if tgt.parent.name == "posts":
            d = {"title": title, "description": desc, "h1": h1, "date": str(cfm.get("date", "2026-11-08"))}
            faq = faq_from(body)
            if faq: d["faq"] = faq
            tgt.write_text(fm(d) + body + "\n", encoding="utf-8"); n += 1; continue
        old, _ = split(tgt)
        d = {k: old[k] for k in ("pageType", "draft", "schema", "place", "cta") if k in old}
        d.update(title=title, description=desc, h1=h1)
        lead, body2 = first_para(body)
        if lead: d["lead"] = lead
        if old.get("pageType") == "faq":
            d["faq"] = faq_from(body); body2 = ""
        elif "faq" in old and old.get("pageType") != "faq":
            f2 = faq_from(body)
            if f2: d["faq"] = f2
        if stem in ("neighbours", "approvals", "gallery"): d["draft"] = True
        order = ["title", "description", "h1", "lead", "pageType", "draft", "schema", "faq", "place", "cta"]
        d = {k: d[k] for k in order if k in d} | {k: v for k, v in d.items() if k not in order}
        tgt.write_text(fm(d) + (body2 if old.get("pageType") != "home" else "") + "\n", encoding="utf-8"); n += 1
    (ROOT / "02_Website/qa/import-log.md").write_text("# Copy import log\n\n" + "\n".join(f"- {x}" for x in LOG) + "\n", encoding="utf-8")
    left = [str(p) for p in SITE.rglob("*.md") if "OWNER TO CONFIRM" in p.read_text(encoding="utf-8")]
    print("imported", n, "files; log lines", len(LOG), "; leftovers:", left)


if __name__ == "__main__":
    main()
