# python3 mkasks.py SRC.py CONTENT_UNIT_DIR [--write] [--per N]
# SRC defines A = [(term, q, right, [(wrong, why)]*3, exp), ...]
import json, os, re, sys, runpy, collections
src, udir = sys.argv[1], sys.argv[2]
write = "--write" in sys.argv
per = int(sys.argv[sys.argv.index("--per")+1]) if "--per" in sys.argv else 1
A = runpy.run_path(src)["A"]
if "--merge" in sys.argv:
    old = json.load(open(os.path.join(udir, "asks.json")))
    A = [(t, q["q"], q["right"], [tuple(w) for w in q["wrong"]], q.get("exp", "")) for t, v in old.items() for q in v] + A
terms = []
for line in open(os.path.join(udir, "cards.md")):
    if line.startswith("| ") and not line.startswith("| Term |"):
        terms.append(re.split(r"(?<!\\)\|", line.strip().strip("|"))[0].strip())
out, bad = {}, []
stems = collections.Counter()
for t in A:
    if len(t) != 5: bad.append("bad tuple: %r" % (t[:2],)); continue
    term, q, right, wrong, exp = t
    if term not in terms: bad.append("no such card: " + term)
    if len(wrong) != 3: bad.append(term + ": needs 3 wrong")
    ch = [right] + [w[0] for w in wrong]
    if len(set(c.lower() for c in ch)) != 4: bad.append(term + ": repeated choice")
    if any(not w[1].strip() for w in wrong): bad.append(term + ": missing why")
    if len(right) > max(len(w[0]) for w in wrong): bad.append("%s: right longest (%d vs %d) :: %s" % (term, len(right), max(len(w[0]) for w in wrong), q[:60]))
    if re.search(r"\b(choice|option) [A-D]\b|\b[A-D] and [A-D]\b|all of the above|none of the above", " ".join(ch+[exp]), re.I): bad.append(term + ": letter/all-of-above reference")
    stems[q] += 1
    out.setdefault(term, []).append({"q": q, "right": right, "wrong": [list(w) for w in wrong], "exp": exp})
for s, n in stems.items():
    if n > 1: bad.append("duplicate stem: " + s[:70])
few = [t for t in terms if len(out.get(t, [])) < per]
for b in bad: print("  " + b)
print("%d questions, %d cards, %d with fewer than %d%s" % (len(A), len(terms), len(few), per, (": " + "; ".join(few)) if few else ""))
if write and not bad:
    json.dump(out, open(os.path.join(udir, "asks.json"), "w"), indent=1, ensure_ascii=False); print("wrote asks.json")
