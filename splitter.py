import csv

with open('input.csv', 'r', encoding='utf-8') as infile, \
     open('output.csv', 'w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    
    writer.writeheader()  # write column names

    for row in reader:
        if float(row['price']) < 3.00:
            writer.writerow(row)
