import pandas

class CsvMaker:
    def __init__(self):
       pass

    def make_csv(self, data, filename):
        df = pandas.DataFrame(data)
        df.to_csv(filename, index=False)

    def print_csv(self, data):
        df = pandas.DataFrame(data)
        print(df)