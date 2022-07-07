import csv

def read_rows(filename):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # skip first (header) row
        for row in csv_reader:
            if len(row)>0:
                yield row
