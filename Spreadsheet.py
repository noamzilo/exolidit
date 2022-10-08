from typing import Tuple
import gspread
from requests.models import Response
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe


class Spreadsheet(object):
    def __init__(self, spreadsheet_name):
        self._spreadsheet_name = spreadsheet_name
        gc = gspread.service_account()
        gc.login()
        self._client = gc.open(spreadsheet_name)

    @staticmethod
    def sheet_rows_from_df(input_df: pd.DataFrame):
        work_sheet_rows = []
        for row_ind, row in enumerate(input_df.iterrows()):
            row_ = [row_ind]
            for cell in row[1]:
                row_.append(str(cell))
            work_sheet_rows.append(row_)

        return work_sheet_rows

    def overwrite_sheet(self, input_df: pd.DataFrame, sheet_name: str):
        # work_sheet_rows = [["index", *input_df.columns]]
        # work_sheet_rows += Spreadsheet.sheet_rows_from_df(input_df)
        #
        # self._client.values_update(
        #     sheet_name,
        #     params={'valueInputOption': 'USER_ENTERED'},
        #     body={'values': work_sheet_rows}
        # )
        worksheet = self._client.worksheet(sheet_name)
        set_with_dataframe(worksheet, input_df, include_index=False, include_column_header=True)

    def append_to_sheet(self, df_to_append: pd.DataFrame, sheet_name):
        # work_sheet_rows = Spreadsheet.sheet_rows_from_df(append_df)
        # self._client.values_append(
        #     sheet_name,
        #     params={'valueInputOption': 'USER_ENTERED'},
        #     body={'values': work_sheet_rows}
        # )
        df = self.df_by_sheet(sheet_name)
        if len(df) == 0:
            df = df_to_append
        else:
            df = df.append(df_to_append)
        self.overwrite_sheet(df, sheet_name)

    def df_by_sheet(self, sheet_name):
        worksheet = self._client.worksheet(sheet_name)
        df = get_as_dataframe(worksheet)
        return df

    def create_sheet(self, sheet_name):
        try:
            self._client.add_worksheet(title=sheet_name, rows=100, cols=20)
        except gspread.exceptions.APIError as ex:
            if ex.response.status_code == 400:  # already exists
                pass
            else:
                raise
