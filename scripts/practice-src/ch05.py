# Builds content/ch05-nomenclature/practice.json. Formulas are typed plainly ("Fe2O3") and turned into subscripts.
import json, os, re
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
def f(s):  # digits after a letter or ")" become subscripts; a hydrate's leading count stays normal
    return re.sub(r"(?<=[A-Za-z)])(\d+)", lambda m: m.group(1).translate(SUB), s).replace("*", "·")
ALT = {"Sodium bicarbonate": ["Sodium hydrogen carbonate"], "Calcium bicarbonate": ["Calcium hydrogen carbonate"],
       "Copper(II) hydrogen carbonate": ["Copper(II) bicarbonate"], "HC2H3O2": ["CH3COOH"], "Hydroiodic acid": ["Hydriodic acid"], "HI(aq)": ["HI"], "LiC2H3O2": ["LiCH3COO"]}
def answer(m):  # the answer part of a model: drop " (comments)" and anything after ":"
    return re.sub(r"\s+\([^)]*\)", "", m).split(":")[0].strip()
TYPED = {"N1","N2","N3","N4","N5","N6","N7","F1","F2","F3","F4","M1","M2","M3","M4","M5","M6","M7","M8"}
def frq(qid, topic, title, stem, parts):
    out = []
    for i, (p, m) in enumerate(parts):
        part = {"k": "abcdefghij"[i], "prompt": f(p), "model": f(m)}
        if qid in TYPED:
            main = answer(m)
            part["accept"] = [f(main)] + [f(x) for x in ALT.get(main, [])]
        out.append(part)
    return {"id": qid, "type": "frq", "topic": topic, "title": title, "stem": stem, "data": [], "parts": out}
def lab(qid, topic, stem, labels, items):
    return {"id": qid, "type": "label", "topic": topic, "stem": stem, "labels": labels,
            "items": [{"t": f(t), "ans": a, "exp": f(e)} for t, a, e in items]}
TIPS = ["Ask the key's questions first: starts with H? Two elements? Metal or not? Polyatomic ion?",
        "Metal + nonmetal (ionic): never prefixes. If the metal can have more than one charge, work it out from the anion and write it as a Roman numeral.",
        "Two nonmetals (covalent): prefixes on both elements, but never mono- on the first.",
        "Polyatomic ions: copy the name and charge from your sheet; never change the ion.",
        "Type each answer and press Check Answer: it is marked for you. If your answer is right but worded differently, use I got it."]
NAME = "Write the name of each compound."
FORM = "Write the formula of each compound."
S = []
S.append(dict(name="Name it: metal + nonmetal", mode="practice", tips=TIPS, questions=[
 frq("N1", "One-charge metals", "Main-group metal + nonmetal (Type I)", NAME, [
  ("K2S", "Potassium sulfide"), ("CaI2", "Calcium iodide"), ("Ga2O3", "Gallium oxide"),
  ("SrF2", "Strontium fluoride"), ("Li2Se", "Lithium selenide"), ("Ba3N2", "Barium nitride (no prefixes for ionic compounds)")]),
 frq("N2", "Variable-charge metals", "Variable-charge metal + nonmetal (Type II)", NAME + " Work out each metal's charge.", [
  ("CoCl2", "Cobalt(II) chloride: 2 Cl⁻ = 2−, so Co is 2+"), ("Fe2S3", "Iron(III) sulfide: 3 S²⁻ = 6−, ÷ 2 Fe = 3+"),
  ("MnO2", "Manganese(IV) oxide: 2 O²⁻ = 4−"), ("Cu3N", "Copper(I) nitride: N³⁻ ÷ 3 Cu = 1+ each"),
  ("SnBr4", "Tin(IV) bromide"), ("CrF3", "Chromium(III) fluoride"),
  ("ZnO", "Zinc oxide (zinc never gets a numeral)"), ("PbI2", "Lead(II) iodide (lead always needs one)")])]))
S.append(dict(name="Name it: two nonmetals (covalent)", mode="practice", tips=TIPS, questions=[
 frq("N3", "Covalent", "Two nonmetals (Type III)", NAME, [
  ("PBr3", "Phosphorus tribromide"), ("SiCl4", "Silicon tetrachloride"), ("N2O", "Dinitrogen monoxide"),
  ("SO2", "Sulfur dioxide"), ("Cl2O7", "Dichlorine heptoxide (hepta + oxide → heptoxide)"),
  ("P4S10", "Tetraphosphorus decasulfide"), ("CF4", "Carbon tetrafluoride"), ("N2S5", "Dinitrogen pentasulfide")])]))
S.append(dict(name="Name it: polyatomic ions", mode="practice", tips=TIPS, questions=[
 frq("N4", "Polyatomic ions", "Polyatomic ion with a one-charge metal (Type IV)", NAME + " Use your ion sheet.", [
  ("NaHCO3", "Sodium bicarbonate (or sodium hydrogen carbonate)"), ("Al(NO3)3", "Aluminum nitrate"),
  ("(NH4)3PO4", "Ammonium phosphate"), ("Mg(ClO4)2", "Magnesium perchlorate"),
  ("K2CrO4", "Potassium chromate"), ("LiC2H3O2", "Lithium acetate")]),
 frq("N5", "Polyatomic ions", "Polyatomic ion with a variable-charge metal (Type IV)", NAME + " Work out each metal's charge from the polyatomic ion.", [
  ("Fe(OH)3", "Iron(III) hydroxide: 3 OH⁻ = 3−"), ("CuSO4", "Copper(II) sulfate: SO₄²⁻ = 2−"),
  ("Pb(C2H3O2)4", "Lead(IV) acetate: 4 acetate = 4−"), ("Ni3(PO4)2", "Nickel(II) phosphate: 2 PO₄³⁻ = 6−, ÷ 3 Ni = 2+"),
  ("Sn(NO2)2", "Tin(II) nitrite"), ("Co(ClO3)3", "Cobalt(III) chlorate")])]))
S.append(dict(name="Name it: acids and hydrates", mode="practice", tips=TIPS, questions=[
 frq("N6", "Acids", "Acid names", NAME, [
  ("HI(aq)", "Hydroiodic acid (no oxygen: hydro-…-ic)"), ("HNO3", "Nitric acid (nitrate → -ic)"),
  ("H2CO3", "Carbonic acid (carbonate → -ic)"), ("HClO2", "Chlorous acid (chlorite → -ous)"),
  ("H3PO4", "Phosphoric acid"), ("HF(aq)", "Hydrofluoric acid"),
  ("HC2H3O2", "Acetic acid (acetate → -ic)"), ("HClO", "Hypochlorous acid (hypochlorite → hypo-…-ous)")]),
 frq("N7", "Hydrates", "Hydrate names", NAME, [
  ("CuSO4*5H2O", "Copper(II) sulfate pentahydrate"), ("CaCl2*2H2O", "Calcium chloride dihydrate"),
  ("Na2CO3*10H2O", "Sodium carbonate decahydrate"), ("CoCl2*6H2O", "Cobalt(II) chloride hexahydrate")])]))
S.append(dict(name="Write the formula", mode="practice", tips=TIPS, questions=[
 frq("F1", "Binary ionic", "Metal + nonmetal (Types I and II)", FORM + " Balance the charges, then reduce.", [
  ("magnesium iodide", "MgI2"), ("potassium nitride", "K3N"), ("aluminum sulfide", "Al2S3: Al³⁺ and S²⁻ crisscross"),
  ("iron(II) chloride", "FeCl2"), ("copper(II) oxide", "CuO: Cu²⁺ and O²⁻ cancel 1:1"), ("chromium(III) bromide", "CrBr3")]),
 frq("F2", "Covalent", "Two nonmetals (Type III)", FORM + " The prefixes are the subscripts.", [
  ("sulfur tetrafluoride", "SF4"), ("diboron trioxide", "B2O3"), ("carbon disulfide", "CS2"),
  ("tetraphosphorus heptasulfide", "P4S7"), ("nitrogen triiodide", "NI3"), ("dichlorine monoxide", "Cl2O")]),
 frq("F3", "Polyatomic ions", "Polyatomic ions (Type IV)", FORM + " Use parentheses for more than one polyatomic ion.", [
  ("calcium phosphate", "Ca3(PO4)2: 3 Ca²⁺ = 6+, 2 PO₄³⁻ = 6−"), ("ammonium nitrate", "NH4NO3"),
  ("iron(III) sulfate", "Fe2(SO4)3"), ("zinc carbonate", "ZnCO3"), ("lead(II) chromate", "PbCrO4"),
  ("copper(I) sulfite", "Cu2SO3")]),
 frq("F4", "Acids and hydrates", "Acid and hydrate formulas", FORM, [
  ("hydrochloric acid", "HCl(aq)"), ("sulfuric acid", "H2SO4"), ("nitrous acid", "HNO2"),
  ("perchloric acid", "HClO4"), ("hydrocyanic acid", "HCN(aq)"), ("barium chloride dihydrate", "BaCl2*2H2O")])]))
S.append(dict(name="Fix the error", mode="practice", tips=TIPS, questions=[
 frq("E1", "Errors", "Find and fix the mistake", "Each name or formula has a mistake. Write the correct version and say what was wrong.", [
  ("NaCl named \"sodium(I) chloride\"", "Sodium chloride: sodium has only one charge, so no numeral"),
  ("CuCl named \"copper chloride\"", "Copper(I) chloride: copper can be 1+ or 2+, so it needs a numeral"),
  ("MgBr2 named \"magnesium dibromide\"", "Magnesium bromide: no prefixes on ionic names"),
  ("CO2 named \"carbon oxide\"", "Carbon dioxide: covalent names need prefixes"),
  ("aluminum oxide written Al3O2", "Al2O3: Al³⁺ and O²⁻ crisscross to Al₂O₃"),
  ("barium hydroxide written Ba(OH)", "Ba(OH)2: Ba²⁺ needs two OH⁻"),
  ("chromium(II) oxide written Cr(II)O", "CrO: Roman numerals go in names, not formulas"),
  ("H2SO3 named \"sulfuric acid\"", "Sulfurous acid: H₂SO₃ comes from sulfite (-ite → -ous)")])]))
S.append(dict(name="What kind of compound?", mode="practice", tips=TIPS, questions=[
 lab("L1", "Kinds of compounds", "What kind of compound is each one? (The type number your notes use is in parentheses.)", ["Main-group metal + nonmetal (Type I)", "Variable-charge metal + nonmetal (Type II)", "Two nonmetals (Type III)", "Has a polyatomic ion (Type IV)", "Acid, starts with H (Type V)"], [
  ("NaBr", 0, "Sodium has one charge."), ("Fe2O3", 1, "Iron needs a numeral."), ("N2O4", 2, "Two nonmetals."),
  ("KNO3", 3, "Nitrate is polyatomic."), ("HBr(aq)", 4, "Starts with H."), ("MgS", 0, "Mg has one charge."),
  ("SnCl2", 1, "Tin needs a numeral."), ("CCl4", 2, "Two nonmetals."), ("NH4Cl", 3, "Ammonium is polyatomic."),
  ("HNO2", 4, "Starts with H."), ("Al2O3", 0, "Al has one charge."), ("PbO", 1, "Lead needs a numeral.")]),
 lab("L2", "Roman numerals", "Does the name need a Roman numeral?", ["Needs a numeral", "No numeral"], [
  ("CoS", 0, "Cobalt(II) sulfide."), ("AgCl", 1, "Silver is always 1+."), ("ZnSO4", 1, "Zinc is always 2+."),
  ("PbCl4", 0, "Lead(IV) chloride."), ("CdS", 1, "Cadmium is always 2+."), ("SnO", 0, "Tin(II) oxide."),
  ("BaO", 1, "Barium is always 2+."), ("Fe(NO3)3", 0, "Iron(III) nitrate."), ("AlPO4", 1, "Aluminum is always 3+."),
  ("CuBr", 0, "Copper(I) bromide.")]),
 lab("L3", "Bond type", "Ionic or covalent?", ["Ionic", "Covalent"], [
  ("CaBr2", 0, "Metal + nonmetal."), ("NO2", 1, "Two nonmetals."), ("Fe2O3", 0, "Metal + nonmetal."),
  ("PCl3", 1, "Two nonmetals."), ("K2SO4", 0, "Metal + polyatomic ion."), ("H2O", 1, "Two nonmetals."),
  ("CS2", 1, "Two nonmetals."), ("PbO2", 0, "Metal + nonmetal.")])]))
MT = ["Like your review packet: write names and formulas. There's no multiple choice.",
      "Turn the Timer on and use only your polyatomic ion sheet (the table in the Study guide).",
      "Finish every part, then compare with the model answers."]
S.append(dict(name="Mock test: names", mode="exam", exam="Mock test", examTips=MT, tips=TIPS, questions=[
 frq("M1", "Binary ionic", "Part 1A: binary ionic", NAME, [
  ("Na3P", "Sodium phosphide"), ("BaBr2", "Barium bromide"), ("Ni2O3", "Nickel(III) oxide"),
  ("V2O5", "Vanadium(V) oxide"), ("AgI", "Silver iodide"), ("SnS2", "Tin(IV) sulfide")]),
 frq("M2", "Covalent", "Part 1B: covalent", NAME, [
  ("S2Cl2", "Disulfur dichloride"), ("SeO2", "Selenium dioxide"), ("PF5", "Phosphorus pentafluoride"),
  ("B2H6", "Diboron hexahydride")]),
 frq("M3", "Polyatomic", "Part 1C: polyatomic ions", NAME, [
  ("Ca(HCO3)2", "Calcium bicarbonate (calcium hydrogen carbonate)"), ("(NH4)2Cr2O7", "Ammonium dichromate"),
  ("Fe(C2H3O2)2", "Iron(II) acetate"), ("Al2(SO3)3", "Aluminum sulfite"), ("Cu(ClO4)2", "Copper(II) perchlorate"),
  ("Pb3(PO4)4", "Lead(IV) phosphate: 4 PO₄³⁻ = 12−, ÷ 3 Pb = 4+"), ("CoCO3", "Cobalt(II) carbonate")]),
 frq("M4", "Acids and hydrates", "Part 1D: acids and hydrates", NAME, [
  ("H3PO3", "Phosphorous acid (phosphite → -ous)"), ("H2C2O4", "Oxalic acid (oxalate → -ic)"),
  ("NiSO4*7H2O", "Nickel(II) sulfate heptahydrate")])]))
S.append(dict(name="Mock test: formulas", mode="exam", exam="Mock test", examTips=MT, tips=TIPS, questions=[
 frq("M5", "Binary ionic", "Part 2A: binary ionic", FORM, [
  ("strontium chloride", "SrCl2"), ("aluminum nitride", "AlN: Al³⁺ and N³⁻ cancel 1:1"), ("rubidium sulfide", "Rb2S"),
  ("iron(II) phosphide", "Fe3P2: 3 Fe²⁺ = 6+, 2 P³⁻ = 6−"), ("chromium(VI) oxide", "CrO3"),
  ("copper(II) nitride", "Cu3N2"), ("tin(II) fluoride", "SnF2")]),
 frq("M6", "Covalent", "Part 2B: covalent", FORM, [
  ("dinitrogen monoxide", "N2O"), ("tetrasulfur tetranitride", "S4N4 (covalent: don't reduce)"), ("iodine heptafluoride", "IF7")]),
 frq("M7", "Polyatomic", "Part 2C: polyatomic ions", FORM, [
  ("sodium phosphate", "Na3PO4"), ("magnesium nitrite", "Mg(NO2)2"), ("ammonium sulfide", "(NH4)2S"),
  ("iron(III) nitrate", "Fe(NO3)3"), ("lead(II) carbonate", "PbCO3"), ("copper(II) hydrogen carbonate", "Cu(HCO3)2")]),
 frq("M8", "Acids and hydrates", "Part 2D: acids and hydrates", FORM, [
  ("hydroiodic acid", "HI(aq)"), ("chlorous acid", "HClO2"), ("acetic acid", "HC2H3O2"),
  ("zinc sulfate heptahydrate", "ZnSO4*7H2O")])]))
S.append(dict(name="Mock test: fix and classify", mode="exam", exam="Mock test", examTips=MT, tips=TIPS, questions=[
 frq("M9", "Errors", "Part 3: fix the error", "Write the correct version and say what was wrong.", [
  ("FeO named \"iron oxide\"", "Iron(II) oxide: iron needs its charge"),
  ("CaCl2 named \"calcium dichloride\"", "Calcium chloride: no prefixes on ionic names"),
  ("AgNO3 named \"silver(I) nitrate\"", "Silver nitrate: silver never gets a numeral"),
  ("sodium sulfate written NaSO4", "Na2SO4: two Na⁺ balance SO₄²⁻"),
  ("magnesium chloride written Mg(Cl)2", "MgCl2: parentheses are only for polyatomic ions"),
  ("HNO3 named \"nitrous acid\"", "Nitric acid: nitrate → -ic")]),
 frq("M10", "Bond type", "Part 4: ionic or covalent? Then name it.", "Decide the bond type, then name the compound.", [
  ("CS2", "Covalent: carbon disulfide"), ("MnCl2", "Ionic: manganese(II) chloride"),
  ("PCl3", "Covalent: phosphorus trichloride"), ("BaO", "Ionic: barium oxide"),
  ("CuS", "Ionic: copper(II) sulfide"), ("Cl2O", "Covalent: dichlorine monoxide")])]))
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../content/ch05-nomenclature/practice.json")
json.dump({"sections": S}, open(p, "w"), indent=1, ensure_ascii=False); print("wrote", sum(len(s["questions"]) for s in S), "questions")
