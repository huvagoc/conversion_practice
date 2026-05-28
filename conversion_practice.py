"""
Mértékegység-átváltó feladatgenerátor – 5. osztály
Unit conversion exercise generator for Hungarian 5th graders

Usage:
  python conversion_practice.py              # 20-feladatos feladatlap
  python conversion_practice.py --answers    # feladatlap megoldásokkal
  python conversion_practice.py --quiz       # interaktív kvíz
  python conversion_practice.py --n=15       # 15 feladat
  python conversion_practice.py --seed=42    # reprodukálható feladatsor
  python conversion_practice.py --cat=Hosszúság,Tömeg  # csak ezek

Kategóriák: Hosszúság, Terület, Térfogat, Tömeg, Idő
"""

import random
from fractions import Fraction

# ---------------------------------------------------------------------------
# Unit maps  – value = how many base units fit in 1 of this unit
# ---------------------------------------------------------------------------

LENGTH = {"mm": 1, "cm": 10, "dm": 100, "m": 1_000, "km": 1_000_000}

AREA = {
    "mm²": 1, "cm²": 100, "dm²": 10_000, "m²": 1_000_000,
    "a":   100_000_000,          # 1 a  = 100 m²
    "ha":  10_000_000_000,       # 1 ha = 10 000 m²
    "km²": 1_000_000_000_000,
}

VOLUME = {
    "ml": 1, "cl": 10, "dl": 100, "l": 1_000,
    "cm³": 1, "dm³": 1_000, "m³": 1_000_000,
}

MASS = {"mg": 1, "g": 1_000, "dkg": 10_000, "kg": 1_000_000, "t": 1_000_000_000}

TIME = {"s": 1, "perc": 60, "óra": 3_600, "nap": 86_400}

CATEGORIES = {
    "Hosszúság": LENGTH,
    "Terület":   AREA,
    "Térfogat":  VOLUME,
    "Tömeg":     MASS,
    "Idő":       TIME,
}

# Unit pairs + flip flag.  Only pedagogically sensible pairs are listed.
# The generator may flip the direction randomly.
PAIRS = {
    "Hosszúság": [
        ("mm", "cm"), ("cm", "dm"), ("dm", "m"), ("m", "km"),
        ("mm", "dm"), ("cm", "m"), ("dm", "km"), ("mm", "m"),
    ],
    "Terület": [
        ("mm²", "cm²"), ("cm²", "dm²"), ("dm²", "m²"),
        ("m²", "a"), ("a", "ha"), ("m²", "ha"), ("ha", "km²"),
    ],
    "Térfogat": [
        ("ml", "dl"), ("dl", "l"), ("l", "dm³"), ("dm³", "m³"),
        ("ml", "l"), ("cm³", "dl"), ("cm³", "dm³"), ("dl", "dm³"),
    ],
    "Tömeg": [
        ("mg", "g"), ("g", "dkg"), ("dkg", "kg"), ("kg", "t"),
        ("g", "kg"), ("mg", "kg"), ("g", "t"),
    ],
    "Idő": [
        ("s", "perc"), ("perc", "óra"), ("óra", "nap"),
        ("s", "óra"), ("perc", "nap"),
    ],
}

# Sensible range for the SOURCE value (so exercises look realistic)
SRC_RANGE = {
    "mm": (1, 5000),  "cm": (1, 5000),  "dm": (1, 5000),
    "m":  (1, 5000),  "km": (1, 500),
    "mm²":(1, 5000),  "cm²":(1, 5000),  "dm²":(1, 5000),
    "m²": (1, 5000),  "a":  (1, 5000),  "ha": (1, 5000),  "km²":(1, 500),
    "ml": (1, 5000),  "cl": (1, 5000),  "dl": (1, 5000),
    "l":  (1, 5000),  "cm³":(1, 5000),  "dm³":(1, 5000),  "m³": (1, 500),
    "mg": (1, 5000),  "g":  (1, 5000),  "dkg":(1, 5000),
    "kg": (1, 5000),  "t":  (1, 500),
    "s":  (1, 5000),  "perc":(1, 5000), "óra":(1, 500),   "nap":(1, 500),
}

# Answers bigger than this are rejected (too unwieldy for 5th grade)
MAX_ANSWER = 50_000


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def is_nice(frac, max_dp=2):
    """True if frac is an integer or a terminating decimal with ≤ max_dp places."""
    if frac.denominator == 1:
        return True
    f = float(frac)
    return abs(f - round(f, max_dp)) < 1e-9


def nice_str(frac):
    """Format: integer or shortest decimal string."""
    if frac.denominator == 1:
        return str(int(frac))
    f = float(frac)
    for dp in (1, 2):
        if abs(f - round(f, dp)) < 1e-9:
            return str(round(f, dp))
    return f"{frac}"   # fallback (shouldn't reach here after filtering)


def try_make_exercise(from_unit, to_unit, unit_map):
    """
    Attempt to build one exercise with a nice source value AND a nice answer.
    Returns (value_str, answer_str) or None if not achievable in limited tries.

    Strategy: fix a random nice integer *answer*, back-calculate source value,
    then check both are nice and in range.
    factor_fwd = unit_map[from] / unit_map[to]   →   answer = source * factor_fwd
    """
    factor_fwd = Fraction(unit_map[from_unit], unit_map[to_unit])
    lo, hi = SRC_RANGE.get(from_unit, (1, 5000))

    for _ in range(500):
        answer_int = random.randint(1, 999)
        # source = answer / factor_fwd
        src_frac = Fraction(answer_int) / factor_fwd
        sv = float(src_frac)
        if not (lo <= sv <= hi):
            continue
        if not is_nice(src_frac):
            continue
        ans_frac = Fraction(answer_int)
        if ans_frac > MAX_ANSWER:
            continue
        # Format source value
        src_str = (str(int(src_frac)) if src_frac.denominator == 1
                   else str(round(float(src_frac), 2)))
        return src_str, nice_str(ans_frac)

    return None  # give up on this pair/direction


def generate_exercise(category=None):
    """
    Generate one exercise dict, retrying pair selection until a nice one is found.
    """
    if category is None:
        category = random.choice(list(CATEGORIES.keys()))

    unit_map = CATEGORIES[category]
    pairs = PAIRS[category][:]

    random.shuffle(pairs)
    for base_pair in pairs:
        for from_unit, to_unit in [base_pair, (base_pair[1], base_pair[0])]:
            result = try_make_exercise(from_unit, to_unit, unit_map)
            if result:
                src_str, ans_str = result
                return {
                    "category": category,
                    "from_unit": from_unit,
                    "to_unit":   to_unit,
                    "value":     src_str,
                    "answer":    ans_str,
                    "question":  f"{src_str} {from_unit} = _______ {to_unit}",
                }

    raise RuntimeError(f"Could not generate a nice exercise for category '{category}'")


# ---------------------------------------------------------------------------
# Worksheet
# ---------------------------------------------------------------------------

def generate_worksheet(n=20, show_answers=False, seed=None, category_filter=None):
    if seed is not None:
        random.seed(seed)

    allowed = list(CATEGORIES.keys())
    if category_filter:
        allowed = [c for c in allowed if c in category_filter]

    exercises = [generate_exercise(random.choice(allowed)) for _ in range(n)]

    W = 64
    print("=" * W)
    print("   MÉRTÉKEGYSÉG-ÁTVÁLTÁS – Feladatlap")
    print("   Név: ________________________  Dátum: ___________")
    print("=" * W)

    grouped: dict[str, list] = {}
    for ex in exercises:
        grouped.setdefault(ex["category"], []).append(ex)

    idx = 1
    for cat, exs in grouped.items():
        print(f"\n  [{cat}]")
        for ex in exs:
            ans_part = f"   →  {ex['answer']} {ex['to_unit']}" if show_answers else ""
            print(f"  {idx:>2}. {ex['question']}{ans_part}")
            idx += 1

    print()
    print("=" * W)
    if show_answers:
        print("  (Megoldások fent láthatók)")
    else:
        print("  Megoldások: futtasd --answers kapcsolóval")
    print("=" * W)
    return exercises


# ---------------------------------------------------------------------------
# Interactive quiz
# ---------------------------------------------------------------------------

def quiz_mode(n=10, category_filter=None):
    allowed = list(CATEGORIES.keys())
    if category_filter:
        allowed = [c for c in allowed if c in category_filter]

    correct = 0
    print("\n🎓 Átváltás-kvíz!  Írj be egy számot, majd nyomj Entert.\n")
    for i in range(1, n + 1):
        ex = generate_exercise(random.choice(allowed))
        print(f"  {i}/{n}  [{ex['category']}]  {ex['question']}")
        try:
            user = input("       Válaszod: ").strip().replace(",", ".")
        except (EOFError, KeyboardInterrupt):
            print("\nKilépés.")
            break
        if user == ex["answer"]:
            print("       ✅ Helyes!\n")
            correct += 1
        else:
            print(f"       ❌ Helytelen. Helyes: {ex['answer']} {ex['to_unit']}\n")

    print(f"Eredmény: {correct}/{n} pont")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    args       = sys.argv[1:]
    mode       = "worksheet"
    n          = 20
    show_ans   = False
    seed       = None
    cat_filter = None

    for arg in args:
        if arg == "--quiz":              mode = "quiz"
        elif arg == "--answers":         show_ans = True
        elif arg.startswith("--n="):     n = int(arg.split("=")[1])
        elif arg.startswith("--seed="):  seed = int(arg.split("=")[1])
        elif arg.startswith("--cat="):   cat_filter = arg.split("=")[1].split(",")
        elif arg == "--help":
            print(__doc__)
            sys.exit(0)

    if mode == "quiz":
        quiz_mode(n=n, category_filter=cat_filter)
    else:
        generate_worksheet(n=n, show_answers=show_ans, seed=seed, category_filter=cat_filter)