from CalParser import CalParser


class CreditCardParser(object):
    def __init__(self, ):
        self.required_df_columns = {
            "date",
            "business_name",
            "charge_amount",
            "deal_amounts",
            "currency",
            "card_shown",
        }
        self._cal_parser = CalParser()

    def from_cal(self, pdf_path: str):
        df = self._cal_parser.parse_cal(pdf_path)
        assert all(c in df.columns for c in self.required_df_columns)
        assert all(c in self.required_df_columns for c in df.columns)
        return df
