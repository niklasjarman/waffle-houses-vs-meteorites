import csv
import sqlite3


def load_data():
    with open("cleaned/cleaned_waffle_houses.csv", 'r', newline='', encoding='utf-8') as file:
        waffle_house_data = csv.DictReader(file)
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        
        for row in waffle_house_data:
            cursor.execute('''INSERT INTO waffle_houses (name, address, city, state, zip_code, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (row['name'], row['address'], row['city'], row['state'], row['zip_code'], row['latitude'], row['longitude']))
        
        conn.commit()
        conn.close()
    
    with open("cleaned/cleaned_meteorites.csv", 'r', newline='', encoding='utf-8') as file:
        meteorite_data = csv.DictReader(file)
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        
        for row in meteorite_data:
            cursor.execute('''INSERT INTO meteorite_landings (name, nametype, recclass, mass, fall, year, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (row['name'], row['nametype'], row['recclass'], row['mass (g)'], row['fall'], row['year'], row['reclat'], row['reclong']))
        
        conn.commit()
        conn.close()

def main():
    load_data()

if __name__ == "__main__":
    main()