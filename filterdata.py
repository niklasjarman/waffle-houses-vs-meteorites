import csv

def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def filter_data():
    meteorite_data = read_csv("uncleaned/Meteorite_Landings.csv")

    clean_meteorite_data = [row for row in meteorite_data if row.get('reclat') and row.get('reclong')
                            and float(row['reclat']) != 0.0 and float(row['reclong']) != 0.0]

    us_latitude_bounds = (24.396308, 49.384358)
    us_longitude_bounds = (-125.0, -66.93457)

    us_data = [row for row in clean_meteorite_data if us_latitude_bounds[0] <= float(row['reclat']) <= us_latitude_bounds[1]
            and us_longitude_bounds[0] <= float(row['reclong']) <= us_longitude_bounds[1]]

    for row in us_data:
        row['mass (g)'] = row.get('mass (g)', '0')
        row['year'] = row.get('year', '0')

    for row in us_data:
        row['year'] = int(row['year'])

    def write_csv(filename, data):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    write_csv("cleaned_meteorites.csv", us_data)

def main():
    filter_data()

if __name__ == "__main__":
    main()