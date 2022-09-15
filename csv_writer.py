import csv
from constants import FILE_HEADERS


class csv_access:

    def __init__(self, csv_path, rows: list):
        self.csv_path = csv_path
        self.rows = rows

    def check_is_header_exist(self):
        with open(self.csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            readed_rows = list(csv_reader)

            if readed_rows[0] == FILE_HEADERS:
                return True
            else:
                return False

    def write_to_csv(self):
        header_necessity = self.check_is_header_exist()

        with open(self.csv_path, 'a', newline='') as file:
            writer = csv.writer(file)

            if header_necessity is False: writer.writerow(FILE_HEADERS)

            parsed_list = list(self.rows)

            for set_row in parsed_list:
                row = dict(set_row)
                writer.writerow([row[FILE_HEADERS[0]],
                                 row[FILE_HEADERS[1]],
                                 row[FILE_HEADERS[2]],
                                 row[FILE_HEADERS[3]],
                                 row[FILE_HEADERS[4]]])
