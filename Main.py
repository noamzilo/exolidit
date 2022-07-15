import os
from enum import Enum
import pandas as pd
from tika import parser
import re
from typing import List, Tuple, Set
# windows only
import ctypes
from ctypes.util import find_library

find_library("".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll")))


class Currency(Enum):
    nis = 0
    usd = 1
    eur = 2
    gbp = 3


currencies = {
    "₪": Currency.nis,
    "$": Currency.usd,
    "€": Currency.eur,
    "£": Currency.gbp,

}


def is_numeric(s):
    return s.replace(",", ".").replace("-", "").replace('.', '', 1).isdigit()


def parse_currency(line_split: List[str]):
    relevant_currencies = []
    for word in line_split:
        for c in currencies.keys():
            if c in word:
                relevant_currencies.append(c)

    return relevant_currencies[0]


def split_line_to_parts(line: str):
    line_split = line.split()
    # currency = parse_currency(line_split)
    currency = Currency.nis

    line_clean = [word for word in line_split if not any(c in word for c in currencies.keys())]
    date = line_clean[0]
    charge_amount = parse_numeric(line_clean[-1])
    try:
        deal_amount = parse_numeric(line_clean[-2])
    except ValueError as ex:
        deal_amount = None

    card_shown = False if line_clean[-3] == "לא" else None

    business_name = " ".join(line_clean[1:-2])
    return currency, date, business_name, charge_amount, deal_amount, card_shown


def parse_numeric(numeric_word: str) -> float:
    if "," in numeric_word:
        amount = float(numeric_word.replace(",", "")[::-1])
    else:
        amount = float(numeric_word.replace(",", ""))
    return amount


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


def filter_money_lines(money_lines: List[str]) -> List[str]:
    return money_lines


def filter_date_lines(date_lines: List[str]) -> List[str]:
    filtered = []
    for line in date_lines:
        if len(line.split()) == 1:
            continue
        filtered.append(line)
    return filtered


def is_money_line(line: str):
    return "₪" in line


def is_date_line(line: str):
    return line.split()[0].count("/") == 2


def merge_money_date_lines(all_lines: List[str]) -> List[str]:
    united = []

    r = 0
    while r < len(all_lines):
        relevant_line = all_lines[r]
        if "פירוט עסקות לחיוב עתידי" in relevant_line:
            break
        if "לא לתשלום - לידיעה בלבד" in relevant_line:
            break
        r += 1

        is_money = is_money_line(relevant_line)
        is_date = is_date_line(relevant_line)

        if is_money and is_date:
            united.append(relevant_line)
        elif is_money:
            for r2 in range(r, len(all_lines)):
                next_line = all_lines[r2]
                if is_date_line(next_line):
                    break
            else:
                raise AssertionError("Problem")

            united.append(next_line + relevant_line)
            r = r2

    return united


def main():
    pdf_folder_path = r"C:\Users\noam.s\Desktop\important\money\cal"
    pdf_names = [
        r"2020_04_.pdf",
        r"2020_05_.pdf",
        r"2020_06_.pdf",
        r"2020_07_.pdf",
        r"2020_08_.pdf",
        r"2020_09_.pdf",
        r"2020_10_.pdf",
        r"2020_11.pdf",
        r"2020_12.pdf",
        r"2021_01.pdf",
        r"2021_02.pdf",
        r"2021_03.pdf",
        r"2021_04.pdf",
        r"2021_05.pdf",
        r"2021_06.pdf",
        r"2021_07.pdf",
        r"2021_08.pdf",
        r"2021_09.pdf",
        r"2021_10.pdf",
        r"2021_11.pdf",
        r"2021_12.pdf",
        r"2022_01.pdf",
        r"2022_02.pdf",
        r"2022_03.pdf",
        ]

    dfs = []
    for pdf_ind, pdf_name in enumerate(pdf_names):

        pdf_path = os.path.join(pdf_folder_path, pdf_name)

        raw = parser.from_file(pdf_path)
        content: str = raw["content"]

        lines = list(filter(lambda s: len(s) > 0, map(lambda s: s.strip(), content.split("\n"))))

        fixed_hebrew_lines: List[str] = []
        for line_i, line in enumerate(lines):
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
            "מסגרת אשראי בתוקף עד",
            "הנתונים נכונים לתאריך",
            "מועד החיוב הבא הינו",
            "פירוט עסקות שנצברו עד",
            '-ל ישדוח בויח ףד',
        ]
        relevant_lines = []
        for line in fixed_hebrew_lines:
            for irrelevant_phrase in irrelevant_phrases:
                if irrelevant_phrase in line:
                    break
            else:
                relevant_lines.append(line)

        merged_lines = merge_money_date_lines(relevant_lines)

        split_relevant_lines = list(map(lambda s: s.split(), merged_lines))
        # clean shah sign
        # lines_clean = []
        # for line in split_relevant_lines:
        #     line_clean = list(filter(lambda w: "₪" not in w, line))
        #     lines_clean.append(line_clean)

        dates, business_names, charge_amounts, deal_amounts, currencies, card_showns = [], [], [], [], [], []
        for line_num, line, in enumerate(merged_lines):
            currency, date, business_name, charge_amount, deal_amount, card_shown = split_line_to_parts(line)

            dates.append(date)
            business_names.append(business_name)
            charge_amounts.append(charge_amount)
            deal_amounts.append(deal_amount)
            currencies.append(currency)
            card_showns.append(card_shown)

        df = pd.DataFrame({
            "date": dates,
            "business_name": business_names,
            "charge_amount": charge_amounts,
            "deal_amounts": deal_amounts,
            "currency": currencies,
            "card_shown": card_showns}
        )
        dfs.append(df)
    pass


if __name__ == "__main__":
    main()
