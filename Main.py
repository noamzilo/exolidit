import os
from tika import parser
import re
from typing import List, Tuple, Set
# windows only
import ctypes
from ctypes.util import find_library
find_library("".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll")))


def is_numeric(s):
    return s.replace(",", ".").replace("-", "").replace('.', '', 1).isdigit()


def should_be_inverted(line: str):
    should = True
    shouldnt_invert_exprs = [
        'סה"כ לתאריך'
    ]
    if any(e in line for e in shouldnt_invert_exprs):
        should = False

    return should

def find_hebrew_phrase_in_raw(phrase: str, raw: str):
    inverted_phrase = phrase[::-1]
    wheres = [m.start() for m in re.finditer(inverted_phrase, raw)]
    return wheres


def main():
    pdf_folder_path = r"C:\Users\noam.s\Desktop\important\money\cal"
    pdf_name = r"2020_10_.pdf"
    pdf_path = os.path.join(pdf_folder_path, pdf_name)

    raw = parser.from_file(pdf_path)
    content: str = raw["content"]

    lines = list(filter(lambda s: len(s) > 0, map(lambda s: s.strip(), content.split("\n"))))

    a = find_hebrew_phrase_in_raw("17/09/2020", content)

    money_lines: List[str] = list(filter(lambda s: "₪" in s, lines))

    b = find_hebrew_phrase_in_raw("17/09/2020", " ".join(money_lines))
    c = re.findall(r"^(\d+/\d+/\d+).*$", content, re.U & re.I)

    fixed_hebrew_lines = []
    for line_i, line in enumerate(money_lines):
        if should_be_inverted(line):
            fixed_hebrew_line = []
            for word in line.split():
                is_numeric_ = is_numeric(word)
                fixed_hebrew_word = word[::-1] if not is_numeric_ else word
                fixed_hebrew_line.append(fixed_hebrew_word)
            fixed_hebrew_line_str = " ".join(reversed(fixed_hebrew_line))
        else:
            fixed_hebrew_line_str = line
        fixed_hebrew_lines.append(fixed_hebrew_line_str)

    irrelevant_phrases = [
        "מסגרת אשראי לחשבון",
        "ניצלתם בפועל",
        "סך התחייבויות באשראי לכרטיס",
        'סך החיובים הצפויים למועד החיוב הבא בש"ח',
        # 'הוראת קבע',
        'סה"כ לתאריך',
    ]

    relevant_lines = list(filter(lambda s: not any(p in s for p in irrelevant_phrases), fixed_hebrew_lines))
    split_relevant_lines = list(map(lambda s: s.split(), relevant_lines))
    # clean shah sign
    lines_clean = []
    for line in split_relevant_lines:
        line_clean = list(filter(lambda w: "₪" not in w, line))
        lines_clean.append(line_clean)

    dates, business_names, amounts = [], [], []
    for line in lines_clean:
        date = line[0]
        business = line[1]
        amount = float(line[-1])

        dates.append(date)
        business_names.append(business)
        amounts.append(amount)

    pass



if __name__ == "__main__":
    main()
