import csv
from os.path import exists

class csv_access:

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def check_file_exist(self):
        return exists(self.csv_path)

    def create_csv_file(self):
        o_file = open(self.csv_path, "x").close()

        csv_writer = csv.DictWriter(self.csv_path, fieldnames=['Article name', 'authors', 'year', 'citation number', 'link'])
        csv_writer.writeheader()

        csv.DictWriter.writeheader()

    def write_to_csv(self):
        if not self.check_file_exist():
            self.create_csv_file()

        self.append_file()

    def append_file(self):
        pass