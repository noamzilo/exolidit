import os.path

from CreditCardParser import CreditCardParser
from Spreadsheet import Spreadsheet


def main():
    parser = CreditCardParser()
    spreadsheet_name = "Exolidit_automation"
    sheet_name = "bank3"
    spreadsheet = Spreadsheet(spreadsheet_name)

    pdf_folder_path = r"C:\Users\noam.s\Desktop\important\money\cal"
    pdf_names = (
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
    )

    spreadsheet.create_sheet(sheet_name)
    for pdf_ind, pdf_name in enumerate(pdf_names):
        pdf_path = os.path.join(pdf_folder_path, pdf_name)
        assert os.path.isfile(pdf_path)
        df = parser.from_cal(pdf_path)
        spreadsheet.append_to_sheet(df, sheet_name=sheet_name)


if __name__ == "__main__":
    main()
