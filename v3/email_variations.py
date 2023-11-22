import pandas as pd


#
class EmailVariation:
    def __init__(self, data):
        self.data = data
        self.emails = {}

    def create_variations(self):
        for index, row in self.data.iterrows():
            if pd.isna(row['domain']):
                continue
            if pd.isna(row['surname']):
                continue
            if pd.isna(row['name']):
                continue
            self.emails[index] = [
                    f'{row["name"]}.{row["surname"]}@{row["domain"]}'.lower(),
                    f'{row["name"]}.{row["surname"][0]}@{row["domain"]}'.lower(),
                    f'{row["name"]}{row["surname"][0]}@{row["domain"]}'.lower(),
                    f'{row["name"][0]}{row["surname"]}@{row["domain"]}'.lower(),
                    f'{row["name"]}@{row["domain"]}'.lower(),
                    f'{row["surname"]}@{row["domain"]}'.lower(),
                    f'{row["name"][0]}.{row["surname"][0]}@{row["domain"]}'.lower(),
                    f'{row["name"]}{row["surname"]}@{row["domain"]}'.lower(),
                    f'{row["name"][0]}.{row["surname"]}@{row["domain"]}'.lower()
                ]
        return self.emails