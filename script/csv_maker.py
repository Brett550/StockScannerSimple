import pandas

class CsvMaker:
    def __init__(self):
       pass

    def get_df(self, data):
        return pandas.DataFrame(data)

    def make_csv(self, data, filename):
        df = self.get_df(data)
        df.to_csv(filename, index=False)

    def print_csv(self, data):
        df = self.get_df(data)
        print(df)