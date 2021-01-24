import csv


def get_new_id(file):
    max_id = 0
    try:
        with open('./'+file, newline='') as csvfile:
            items = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in items:
                if row[0].isdigit():
                    if int(row[0]) > max_id:
                        max_id = int(row[0])
        csvfile.close()
    except:
        None
    max_id = max_id+1
    return max_id
