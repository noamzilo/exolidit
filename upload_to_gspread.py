import pandas as pd
import gspread


def upload_to_gspread(df: pd.DataFrame):
    gc = gspread.service_account()
    gc.login()
    spreadsheet = gc.open("Exolidit_automation")
    sheet_name = "bank"
    # work_sheet = spreadsheet.worksheet("bank")
    work_sheet_rows = [["index", *df.columns]]

    for row_ind, row in enumerate(df.iterrows()):
        row_ = [row_ind]
        for cell in row[1]:
            row_.append(str(cell))
        work_sheet_rows.append(row_)
    # work_sheet.append_rows(work_sheet_rows, value_input_option="USER_ENTERED")

    spreadsheet.values_update(
        sheet_name,
        params={'valueInputOption': 'USER_ENTERED'},
        body={'values': work_sheet_rows}
    )

    pass
    # print(sheet.sheet1.get('A:A'))
