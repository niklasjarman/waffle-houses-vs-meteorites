from flask import Flask, jsonify, request, render_template
import sqlite3
import math
import xml.etree.ElementTree as ET
import geocoder

app = Flask(__name__)

def acos(x):
    return math.acos(x)

def get_lat_long():
    g = geocoder.ip('me')
    lat_long = g.latlng
    return lat_long

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/closest-waffle-houses-to-meteorites-visual')
def closest_waffle_visual():
    return render_template('closest_waffle_house_to_meteorites.html')

@app.route('/closest-meteorite-to-waffle-houses-visual')
def closest_meteorite_visual():
    return render_template('closest_meteorite_to_waffle_houses.html')

@app.route('/meteorite-time-series-chart')
def meteorite_time_series_chart():
    return render_template('meteorite_time.html')

@app.route('/distance-visualizer-scatter-plot')
def distance_visualizer():
    return render_template('distance_visualizer_scatter_plot.html')

@app.route('/waffle-houses-per-state-graph')
def waffle_houses_per_state_graph():
    return render_template('waffle_house_per_state.html')

@app.route('/api/meteorite_landings', methods=['GET'])
def get_meteorite_landings():
    try:        
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM meteorite_landings")
            
        data = cursor.fetchall()
        conn.close()

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('meteorite_landings')
            for meteorite_landing in data:
                meteorite_landing_tag = ET.SubElement(root, 'meteorite_landing')
                
                name_tag = ET.SubElement(meteorite_landing_tag, 'name')
                name_tag.text = str(meteorite_landing[0])
                
                nametype_tag = ET.SubElement(meteorite_landing_tag, 'nametype')
                nametype_tag.text = str(meteorite_landing[1])
                
                recclass_tag = ET.SubElement(meteorite_landing_tag, 'recclass')
                recclass_tag.text = str(meteorite_landing[2])
                
                fall_tag = ET.SubElement(meteorite_landing_tag, 'mass')
                fall_tag.text = str(meteorite_landing[3])
                
                year_tag = ET.SubElement(meteorite_landing_tag, 'year')
                year_tag.text = str(meteorite_landing[5])
                
                latitude_tag = ET.SubElement(meteorite_landing_tag, 'latitude')
                latitude_tag.text = str(meteorite_landing[6])
                
                longitude_tag = ET.SubElement(meteorite_landing_tag, 'longitude')
                longitude_tag.text = str(meteorite_landing[7])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            response_data = {'meteorite_landings': []}
            for meteorite_landing in data:
                response_data['meteorite_landings'].append({
                    'name': meteorite_landing[0],
                    'nametype': meteorite_landing[1],
                    'recclass': meteorite_landing[2],
                    'fall': meteorite_landing[3],
                    'year': meteorite_landing[5],
                    'latitude': meteorite_landing[6],
                    'longitude': meteorite_landing[7]
                })
            return jsonify(response_data)

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500

@app.route('/api/meteorite_landings/name/<name>', methods=['GET'])
def get_meteorite_landings_by_name(name):
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meteorite_landings WHERE name=?", (name,))
        data = cursor.fetchone()
        conn.close()

        if not data:
            return jsonify({'error': 'Meteorite landing not found'}), 404

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('meteorite_landing')
            
            name_tag = ET.SubElement(root, 'name')
            name_tag.text = str(data[0])
            
            nametype_tag = ET.SubElement(root, 'nametype')
            nametype_tag.text = str(data[1])
            
            recclass_tag = ET.SubElement(root, 'recclass')
            recclass_tag.text = str(data[2])
            
            mass_tag = ET.SubElement(root, 'mass')
            mass_tag.text = str(data[3])
            
            fell_tag = ET.SubElement(root, 'fall')
            fell_tag.text = str(data[4])
            
            year_tag = ET.SubElement(root, 'year')
            year_tag.text = str(data[5])
            
            latitude_tag = ET.SubElement(root, 'latitude')
            latitude_tag.text = str(data[6])
            
            longitude_tag = ET.SubElement(root, 'longitude')
            longitude_tag.text = str(data[7])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            response_data = {
                'name': data[0],
                'nametype': data[1],
                'recclass': data[2],
                'mass': data[3],
                'year': data[5],
                'latitude': data[6],
                'longitude': data[7]
            }
            return jsonify(response_data)

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500

@app.route('/api/meteorite_landings/type/<meteorite_type>', methods=['GET'])
def meteorite_landings_by_type(meteorite_type):
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM meteorite_landings WHERE recclass=?", (meteorite_type,))
        data = cursor.fetchall()
        conn.close()

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('meteorite_landings')
            for meteorite_landing in data:
                meteorite_landing_tag = ET.SubElement(root, 'meteorite_landing')
                
                name_tag = ET.SubElement(meteorite_landing_tag, 'name')
                name_tag.text = str(meteorite_landing[0])
                
                nametype_tag = ET.SubElement(meteorite_landing_tag, 'nametype')
                nametype_tag.text = str(meteorite_landing[1])
                
                recclass_tag = ET.SubElement(meteorite_landing_tag, 'recclass')
                recclass_tag.text = str(meteorite_landing[2])
                
                fall_tag = ET.SubElement(meteorite_landing_tag, 'mass')
                fall_tag.text = str(meteorite_landing[3])
                
                year_tag = ET.SubElement(meteorite_landing_tag, 'year')
                year_tag.text = str(meteorite_landing[5])
                
                latitude_tag = ET.SubElement(meteorite_landing_tag, 'latitude')
                latitude_tag.text = str(meteorite_landing[6])
                
                longitude_tag = ET.SubElement(meteorite_landing_tag, 'longitude')
                longitude_tag.text = str(meteorite_landing[7])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            response_data = {'meteorite_landings': []}
        for meteorite_landing in data:
            response_data['meteorite_landings'].append({
                'name': meteorite_landing[0],
                'nametype': meteorite_landing[1],
                'recclass': meteorite_landing[2],
                'mass': meteorite_landing[3],
                'fall': meteorite_landing[4],
                'year': meteorite_landing[5],
                'latitude': meteorite_landing[6],
                'longitude': meteorite_landing[7]
            })
        return jsonify(response_data)

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500
    
@app.route('/api/meteorite_landings/min_mass/<min_mass>/max_mass/<max_mass>', methods=['GET'])
def get_meteorite_landings_by_mass_range(min_mass, max_mass):
    try:
        min_mass = float(min_mass)
        max_mass = float(max_mass)

        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM meteorite_landings
            WHERE mass BETWEEN ? AND ?
            ORDER BY mass
        ''', (min_mass, max_mass))

        data = cursor.fetchall()

        conn.close()

        if len(data) == 0:
            response_format = request.args.get('response')
            if response_format == 'xml':
                return jsonify({'message': 'No meteorite landings found within the specified mass range'}), 404, {'Content-Type': 'application/xml'}
            else:
                return jsonify({'message': 'No meteorite landings found within the specified mass range'}), 404

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('meteorite_landings')
            for meteorite_landing in data:
                meteorite_landing_tag = ET.SubElement(root, 'meteorite_landing')
                
                name_tag = ET.SubElement(meteorite_landing_tag, 'name')
                name_tag.text = str(meteorite_landing[0])
                
                nametype_tag = ET.SubElement(meteorite_landing_tag, 'nametype')
                nametype_tag.text = str(meteorite_landing[1])
                
                recclass_tag = ET.SubElement(meteorite_landing_tag, 'recclass')
                recclass_tag.text = str(meteorite_landing[2])
                
                fall_tag = ET.SubElement(meteorite_landing_tag, 'mass')
                fall_tag.text = str(meteorite_landing[3])
                
                year_tag = ET.SubElement(meteorite_landing_tag, 'year')
                year_tag.text = str(meteorite_landing[5])
                
                latitude_tag = ET.SubElement(meteorite_landing_tag, 'latitude')
                latitude_tag.text = str(meteorite_landing[6])
                
                longitude_tag = ET.SubElement(meteorite_landing_tag, 'longitude')
                longitude_tag.text = str(meteorite_landing[7])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            response_data = {'meteorite_landings': []}
        for meteorite_landing in data:
            response_data['meteorite_landings'].append({
                'name': meteorite_landing[0],
                'nametype': meteorite_landing[1],
                'recclass': meteorite_landing[2],
                'mass': meteorite_landing[3],
                'fall': meteorite_landing[4],
                'year': meteorite_landing[5],
                'latitude': meteorite_landing[6],
                'longitude': meteorite_landing[7]
            })
        return jsonify(response_data)

    except (sqlite3.Error, ValueError) as e:
        return jsonify({'error': 'Invalid request'}), 400

@app.route('/api/meteorite_landings/type/<recclass>/year/<int:year>', methods=['GET'])
def meteorite_landings_by_type_and_year(recclass, year):
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM meteorite_landings
            WHERE recclass = ? AND year = ?
        ''', (recclass, year))

        data = cursor.fetchall()
        conn.close()

        if len(data) == 0:
            return jsonify({'message': 'No meteorite landings found for the specified type and year'}), 404

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('meteorite_landings')
            for meteorite_landing in data:
                meteorite_landing_tag = ET.SubElement(root, 'meteorite_landing')
                
                name_tag = ET.SubElement(meteorite_landing_tag, 'name')
                name_tag.text = str(meteorite_landing[0])
                
                nametype_tag = ET.SubElement(meteorite_landing_tag, 'nametype')
                nametype_tag.text = str(meteorite_landing[1])
                
                recclass_tag = ET.SubElement(meteorite_landing_tag, 'recclass')
                recclass_tag.text = str(meteorite_landing[2])
                
                fall_tag = ET.SubElement(meteorite_landing_tag, 'mass')
                fall_tag.text = str(meteorite_landing[3])
                
                year_tag = ET.SubElement(meteorite_landing_tag, 'year')
                year_tag.text = str(meteorite_landing[5])
                
                latitude_tag = ET.SubElement(meteorite_landing_tag, 'latitude')
                latitude_tag.text = str(meteorite_landing[6])
                
                longitude_tag = ET.SubElement(meteorite_landing_tag, 'longitude')
                longitude_tag.text = str(meteorite_landing[7])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            response_data = {'meteorite_landings': []}
            for meteorite_landing in data:
                response_data['meteorite_landings'].append({
                    'name': meteorite_landing[0],
                    'nametype': meteorite_landing[1],
                    'recclass': meteorite_landing[2],
                    'mass': meteorite_landing[3],
                    'fall': meteorite_landing[4],
                    'year': meteorite_landing[5],
                    'latitude': meteorite_landing[6],
                    'longitude': meteorite_landing[7]
                })
            return jsonify(response_data)

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500

@app.route('/api/waffle_houses', methods=['GET'])
def get_waffle_houses():
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM waffle_houses")
        data = cursor.fetchall()
        conn.close()

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('waffle_houses')
            for waffle_house in data:
                wafflehouse_tag = ET.SubElement(root, 'waffle_house')
                
                name, address, city, state, zip_code, latitude, longitude = waffle_house
                
                name_tag = ET.SubElement(wafflehouse_tag, 'name')
                name_tag.text = str(name)
                
                address_tag = ET.SubElement(wafflehouse_tag, 'address')
                address_tag.text = str(address)
                
                city_tag = ET.SubElement(wafflehouse_tag, 'city')
                city_tag.text = str(city)
                
                state_tag = ET.SubElement(wafflehouse_tag, 'state')
                state_tag.text = str(state)
                
                zip_code_tag = ET.SubElement(wafflehouse_tag, 'zip_code')
                zip_code_tag.text = str(zip_code)
                
                latitude_tag = ET.SubElement(wafflehouse_tag, 'latitude')
                latitude_tag.text = str(latitude)
                
                longitude_tag = ET.SubElement(wafflehouse_tag, 'longitude')
                longitude_tag.text = str(longitude)

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            response_data = {'waffle_houses': []}
            for waffle_house in data:
                response_data['waffle_houses'].append({
                    'name': waffle_house[0],
                    'address': waffle_house[1],
                    'city': waffle_house[2],
                    'state': waffle_house[3],
                    'zip_code': waffle_house[4],
                    'latitude': waffle_house[5],
                    'longitude': waffle_house[6]
                })
            return jsonify(response_data)

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500
    
@app.route('/api/waffle_houses/state/<state>', methods=['GET'])
def get_waffle_houses_by_state(state=None):
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()

        if state:
            cursor.execute("SELECT * FROM waffle_houses WHERE state=?", (state,))
        else:
            cursor.execute("SELECT * FROM waffle_houses")

        data = cursor.fetchall()
        conn.close()

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('waffle_houses')
            for waffle_house in data:
                wafflehouse_tag = ET.SubElement(root, 'waffle_house')
                
                name, address, city, state, zip_code, latitude, longitude = waffle_house
                
                name_tag = ET.SubElement(wafflehouse_tag, 'name')
                name_tag.text = str(name)
                
                address_tag = ET.SubElement(wafflehouse_tag, 'address')
                address_tag.text = str(address)
                
                city_tag = ET.SubElement(wafflehouse_tag, 'city')
                city_tag.text = str(city)
                
                state_tag = ET.SubElement(wafflehouse_tag, 'state')
                state_tag.text = str(state)
                
                zip_code_tag = ET.SubElement(wafflehouse_tag, 'zip_code')
                zip_code_tag.text = str(zip_code)
                
                latitude_tag = ET.SubElement(wafflehouse_tag, 'latitude')
                latitude_tag.text = str(latitude)
                
                longitude_tag = ET.SubElement(wafflehouse_tag, 'longitude')
                longitude_tag.text = str(longitude)

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            response_data = {'waffle_houses': []}
            for waffle_house in data:
                response_data['waffle_houses'].append({
                    'name': waffle_house[0],
                    'address': waffle_house[1],
                    'city': waffle_house[2],
                    'state': waffle_house[3],
                    'zip_code': waffle_house[4],
                    'latitude': waffle_house[5],
                    'longitude': waffle_house[6]
                })
            return jsonify(response_data)

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500
    
@app.route('/api/waffle_houses/name/<name>', methods=['GET'])
def get_waffle_houses_by_name(name=None):
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()

        if name:
            cursor.execute("SELECT * FROM waffle_houses WHERE name=?", (name,))
        else:
            cursor.execute("SELECT * FROM waffle_houses")

        data = cursor.fetchall()
        conn.close()

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('waffle_houses')
            for waffle_house in data:
                wafflehouse_tag = ET.SubElement(root, 'waffle_house')
                
                name, address, city, state, zip_code, latitude, longitude = waffle_house
                
                name_tag = ET.SubElement(wafflehouse_tag, 'name')
                name_tag.text = str(name)
                
                address_tag = ET.SubElement(wafflehouse_tag, 'address')
                address_tag.text = str(address)
                
                city_tag = ET.SubElement(wafflehouse_tag, 'city')
                city_tag.text = str(city)
                
                state_tag = ET.SubElement(wafflehouse_tag, 'state')
                state_tag.text = str(state)
                
                zip_code_tag = ET.SubElement(wafflehouse_tag, 'zip_code')
                zip_code_tag.text = str(zip_code)
                
                latitude_tag = ET.SubElement(wafflehouse_tag, 'latitude')
                latitude_tag.text = str(latitude)
                
                longitude_tag = ET.SubElement(wafflehouse_tag, 'longitude')
                longitude_tag.text = str(longitude)

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            response_data = {'waffle_houses': []}
            for waffle_house in data:
                response_data['waffle_houses'].append({
                    'name': waffle_house[0],
                    'address': waffle_house[1],
                    'city': waffle_house[2],
                    'state': waffle_house[3],
                    'zip_code': waffle_house[4],
                    'latitude': waffle_house[5],
                    'longitude': waffle_house[6]
                })
            return jsonify(response_data)

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500

@app.route('/api/waffle_houses/state/<state>/zipcode/<zipcode>', methods=['GET'])
def get_waffle_houses_by_state_and_zipcode(state=None, zipcode=None):
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()

        if state and zipcode:
            cursor.execute("SELECT * FROM waffle_houses WHERE state=? AND zip_code=?", (state, zipcode))
        elif state:
            cursor.execute("SELECT * FROM waffle_houses WHERE state=?", (state,))
        else:
            cursor.execute("SELECT * FROM waffle_houses")

        data = cursor.fetchall()
        conn.close()

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('waffle_houses')
            for waffle_house in data:
                wafflehouse_tag = ET.SubElement(root, 'waffle_house')
                
                name, address, city, state, zip_code, latitude, longitude = waffle_house
                
                name_tag = ET.SubElement(wafflehouse_tag, 'name')
                name_tag.text = str(name)
                
                address_tag = ET.SubElement(wafflehouse_tag, 'address')
                address_tag.text = str(address)
                
                city_tag = ET.SubElement(wafflehouse_tag, 'city')
                city_tag.text = str(city)
                
                state_tag = ET.SubElement(wafflehouse_tag, 'state')
                state_tag.text = str(state)
                
                zip_code_tag = ET.SubElement(wafflehouse_tag, 'zip_code')
                zip_code_tag.text = str(zip_code)
                
                latitude_tag = ET.SubElement(wafflehouse_tag, 'latitude')
                latitude_tag.text = str(latitude)
                
                longitude_tag = ET.SubElement(wafflehouse_tag, 'longitude')
                longitude_tag.text = str(longitude)

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            response_data = {'waffle_houses': []}
            for waffle_house in data:
                response_data['waffle_houses'].append({
                    'name': waffle_house[0],
                    'address': waffle_house[1],
                    'city': waffle_house[2],
                    'state': waffle_house[3],
                    'zip_code': waffle_house[4],
                    'latitude': waffle_house[5],
                    'longitude': waffle_house[6]
                })
            return jsonify(response_data)

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500


    



@app.route('/api/closest_waffle_house_to_meteorites', methods=['GET'])
def closest_waffle_house_to_meteorites():
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                m.name AS meteorite_name,
                w.name AS closest_waffle_house,
                MIN(
                    6371 * acos(
                        cos(radians(w.latitude)) * cos(radians(m.latitude)) *
                        cos(radians(m.longitude) - radians(w.longitude)) +
                        sin(radians(w.latitude)) * sin(radians(m.latitude))
                    )
                ) AS distance
            FROM
                meteorite_landings m
            CROSS JOIN
                waffle_houses w
            GROUP BY
                m.name;
        ''')
        data = cursor.fetchall()
        conn.close()

        response_format = request.args.get('response', 'json')

        if response_format == 'xml':
            root = ET.Element('pairings')
            for row in data:
                pairing_tag = ET.SubElement(root, 'pairing')

                meteorite_name_tag = ET.SubElement(pairing_tag, 'meteorite_name')
                meteorite_name_tag.text = str(row[0])

                closest_waffle_house_tag = ET.SubElement(pairing_tag, 'closest_waffle_house')
                closest_waffle_house_tag.text = str(row[1])

                distance_tag = ET.SubElement(pairing_tag, 'distance')
                distance_tag.text = str(row[2])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            response_data = {'closest_waffle_houses_to_meteorites': []}
            for row in data:
                if row[2] is not None:
                    response_data['closest_waffle_houses_to_meteorites'].append({'meteorite_name': row[0], 'closest_waffle_house': row[1], 'distance': row[2]})
            return jsonify(response_data)

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500


@app.route('/api/average_distance', methods=['GET'])
def average_distance():
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT AVG(distance) AS average_distance
            FROM (
                SELECT
                    6371 * acos(
                        cos(radians(w.latitude)) * cos(radians(m.latitude)) *
                        cos(radians(m.longitude) - radians(w.longitude)) +
                        sin(radians(w.latitude)) * sin(radians(m.latitude))
                    ) AS distance
                FROM
                    waffle_houses w
                JOIN
                    meteorite_landings m
            );
        ''')
        average_distance = cursor.fetchone()[0]
        conn.close()

        response_format = request.args.get('response', 'json')

        if response_format == 'xml':
            root = ET.Element('data')
            average_distance_tag = ET.SubElement(root, 'average_distance')
            average_distance_tag.text = str(average_distance)

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            return jsonify({'average_distance': average_distance})

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500
    
@app.route('/api/average_distance/year/<int:year>', methods=['GET'])
def average_distance_by_year(year):
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT AVG(distance) AS average_distance
            FROM (
                SELECT
                    6371 * acos(
                        cos(radians(w.latitude)) * cos(radians(m.latitude)) *
                        cos(radians(m.longitude) - radians(w.longitude)) +
                        sin(radians(w.latitude)) * sin(radians(m.latitude))
                    ) AS distance
                FROM
                    waffle_houses w
                JOIN
                    meteorite_landings m
                WHERE
                    m.year = ?
            );
        ''', (year,))
        average_distance = cursor.fetchone()[0]
        conn.close()

        response_format = request.args.get('response', 'json')

        if response_format == 'xml':
            root = ET.Element('data')
            average_distance_tag = ET.SubElement(root, 'average_distance')
            average_distance_tag.text = str(average_distance)

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            return jsonify({'average_distance': average_distance})

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500


@app.route('/api/waffle_houses/count_by_state', methods=['GET'])
def count_waffle_houses_by_state():
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT state, COUNT(*) AS num_waffle_houses
            FROM waffle_houses
            GROUP BY state
            ORDER BY num_waffle_houses DESC
        ''')
        data = cursor.fetchall()
        conn.close()

        response_format = request.args.get('response', 'json')

        if response_format == 'xml':
            root = ET.Element('states')
            for row in data:
                pairing_tag = ET.SubElement(root, 'pairing')

                state_tag = ET.SubElement(pairing_tag, 'state')
                state_tag.text = str(row[0])

                num_waffle_houses_tag = ET.SubElement(pairing_tag, 'num_waffle_houses')
                num_waffle_houses_tag.text = str(row[1])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            result = {'states':[{'state': row[0], 'num_waffle_houses': row[1]} for row in data]}
            return jsonify(result), 200

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500

@app.route('/api/average_distance/year/<int:year>/waffle_house_state/<state>', methods=['GET'])
def average_distance_by_year_and_state(year, state):
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT AVG(distance) AS average_distance
            FROM (
                SELECT
                    6371 * acos(
                        cos(radians(w.latitude)) * cos(radians(m.latitude)) *
                        cos(radians(m.longitude) - radians(w.longitude)) +
                        sin(radians(w.latitude)) * sin(radians(m.latitude))
                    ) AS distance
                FROM
                    waffle_houses w
                JOIN
                    meteorite_landings m
                WHERE
                    m.year = ? AND w.state = ?
            );
        ''', (year, state))
        average_distance = cursor.fetchone()[0]
        conn.close()

        response_format = request.args.get('response', 'json')

        if response_format == 'xml':
            root = ET.Element('data')
            average_distance_tag = ET.SubElement(root, 'average_distance')
            average_distance_tag.text = str(average_distance)

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            return jsonify({'average_distance': average_distance})

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500


@app.route('/api/waffle_houses/count_by_state/state/<state>', methods=['GET'])
def count_waffle_houses_by_state_by_state(state):
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) AS num_waffle_houses
            FROM waffle_houses
            WHERE state = ?
        ''', (state,))
        count = cursor.fetchone()[0]
        conn.close()

        response_format = request.args.get('response', 'json')

        if response_format == 'xml':
            root = ET.Element('pairing')
            count_tag = ET.SubElement(root, 'count')
            count_tag.text = str(count)
            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            return jsonify({'count': count}), 200

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500


@app.route('/api/closest_pairs', methods=['GET'])
def closest_pairs():
    try:
        limit = request.args.get('limit')
        if limit is None:
            return jsonify({'error': 'Limit parameter is required'}), 400
        try:
            limit = int(limit)
            if limit <= 0:
                raise ValueError("Limit must be a positive integer")
        except ValueError:
            return jsonify({'error': 'Invalid limit value'}), 400

        conn = sqlite3.connect('project.db')
        conn.create_function("acos", 1, acos)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                w.name AS waffle_house_name,
                m.name AS meteorite_name,
                w.latitude AS waffle_house_latitude,
                w.longitude AS waffle_house_longitude,
                m.latitude AS meteorite_latitude,
                m.longitude AS meteorite_longitude,
                6371 * acos(
                    cos(radians(w.latitude)) * cos(radians(m.latitude)) *
                    cos(radians(m.longitude) - radians(w.longitude)) +
                    sin(radians(w.latitude)) * sin(radians(m.latitude))
                ) AS distance
            FROM
                waffle_houses w
            JOIN
                meteorite_landings m
            ORDER BY
                distance
            LIMIT ?
        ''', (limit,))

        results = cursor.fetchall()
        conn.close()

        data = []
        for row in results:
            pairing = {
                'waffle_house_name': row[0],
                'meteorite_name': row[1],
                'waffle_house_latitude': row[2],
                'waffle_house_longitude': row[3],
                'meteorite_latitude': row[4],
                'meteorite_longitude': row[5]
            }
            data.append(pairing)

        root = ET.Element('closest_pairs')
        for pairing in data:
            pairing_tag = ET.SubElement(root, 'closest_pair')
            for key, value in pairing.items():
                ET.SubElement(pairing_tag, key).text = str(value)

        response_format = request.args.get('response')
        if response_format == 'xml':
            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            data = {'closest_pairs': data}
            return jsonify(data)

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500
    
@app.route('/api/closest_pairs/distance/<float:distance>', methods=['GET'])
def closest_pairs_within_distance(distance):
    try:
        conn = sqlite3.connect('project.db')
        conn.create_function("acos", 1, acos)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                w.name AS waffle_house_name,
                m.name AS meteorite_name,
                w.latitude AS waffle_house_latitude,
                w.longitude AS waffle_house_longitude,
                m.latitude AS meteorite_latitude,
                m.longitude AS meteorite_longitude,
                6371 * acos(
                    cos(radians(w.latitude)) * cos(radians(m.latitude)) *
                    cos(radians(m.longitude) - radians(w.longitude)) +
                    sin(radians(w.latitude)) * sin(radians(m.latitude))
                ) AS distance
            FROM
                waffle_houses w
            JOIN
                meteorite_landings m
            WHERE
                distance <= ?
            ORDER BY
                distance;
        ''', (distance,))

        results = cursor.fetchall()
        conn.close()

        data = []
        for row in results:
            pairing = {
                'waffle_house_name': row[0],
                'meteorite_name': row[1],
                'waffle_house_latitude': row[2],
                'waffle_house_longitude': row[3],
                'meteorite_latitude': row[4],
                'meteorite_longitude': row[5]
            }
            data.append(pairing)

        root = ET.Element('data')
        for pairing in data:
            pairing_tag = ET.SubElement(root, 'pairing')
            for key, value in pairing.items():
                ET.SubElement(pairing_tag, key).text = str(value)

        response_format = request.args.get('response')
        if response_format == 'xml':
            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            data = {'closest_pairs': data}
            return jsonify(data)

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500

    
@app.route('/api/closest_meteorites/waffle_house_name/<name>', methods=['GET'])
def closest_meteorites_by_waffle_house(name):
    try:
        waffle_house_name = name

        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute("SELECT latitude, longitude FROM waffle_houses WHERE name=?", (waffle_house_name,))
        waffle_house_location = cursor.fetchone()
        conn.close()

        if not waffle_house_location:
            response_format = request.args.get('response', 'json')
            if response_format == 'xml':
                return jsonify({'error': 'Waffle house not found'}), 404
            else:
                return jsonify({'error': 'Waffle house not found'}), 404

        waffle_house_latitude, waffle_house_longitude = waffle_house_location

        conn = sqlite3.connect('project.db')
        conn.create_function("acos", 1, acos)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                m.name AS meteorite_name,
                m.latitude AS meteorite_latitude,
                m.longitude AS meteorite_longitude,
                6371 * acos(
                    cos(radians(?)) * cos(radians(m.latitude)) *
                    cos(radians(m.longitude) - radians(?)) +
                    sin(radians(?)) * sin(radians(m.latitude))
                ) AS distance
            FROM
                meteorite_landings m
            ORDER BY
                distance
            LIMIT 5
        ''', (waffle_house_latitude, waffle_house_longitude, waffle_house_latitude))

        results = cursor.fetchall()
        conn.close()

        response_format = request.args.get('response', 'json')

        if response_format == 'xml':
            root = ET.Element('meteorites')
            for row in results:
                meteorite_tag = ET.SubElement(root, 'meteorite')

                name_tag = ET.SubElement(meteorite_tag, 'name')
                name_tag.text = str(row[0])

                latitude_tag = ET.SubElement(meteorite_tag, 'latitude')
                latitude_tag.text = str(row[1])

                longitude_tag = ET.SubElement(meteorite_tag, 'longitude')
                longitude_tag.text = str(row[2])

                distance_tag = ET.SubElement(meteorite_tag, 'distance')
                distance_tag.text = str(row[3])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            result = {'meteorites': [{'meteorite_name': row[0], 'latitude': row[1], 'longitude': row[2], 'distance': row[3]} for row in results]}
            return jsonify(result)

    except (sqlite3.Error, ValueError) as e:
        return jsonify({'error': 'Invalid request'}), 400

@app.route('/api/closest_waffle_house_to_meteorites/meteorite_name/<meteorite_name>', methods=['GET'])
def closest_waffle_house_to_meteorites_by_name(meteorite_name):
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                m.name AS meteorite_name,
                m.latitude AS meteorite_latitude,
                m.longitude AS meteorite_longitude,
                w.name AS closest_waffle_house,
                w.latitude AS wh_latitude,
                w.longitude AS wh_longitude,
                MIN(
                    6371 * acos(
                        cos(radians(w.latitude)) * cos(radians(m.latitude)) *
                        cos(radians(m.longitude) - radians(w.longitude)) +
                        sin(radians(w.latitude)) * sin(radians(m.latitude))
                    )
                ) AS distance
            FROM
                meteorite_landings m
            CROSS JOIN
                waffle_houses w
            WHERE
                m.name = ?
            GROUP BY
                m.name;
        ''', (meteorite_name,))
        data = cursor.fetchall()
        conn.close()

        response_format = request.args.get('response', 'json')

        if response_format == 'xml':
            root = ET.Element('data')
            for row in data:
                pairing_tag = ET.SubElement(root, 'waffle_house')

                meteorite_name_tag = ET.SubElement(pairing_tag, 'meteorite_name')
                meteorite_name_tag.text = str(row[0])

                meteorite_latitude_tag = ET.SubElement(pairing_tag, 'meteorite_latitude')
                meteorite_latitude_tag.text = str(row[1])

                meteorite_longitude_tag = ET.SubElement(pairing_tag, 'meteorite_longitude')
                meteorite_longitude_tag.text = str(row[2])

                closest_waffle_house_tag = ET.SubElement(pairing_tag, 'closest_waffle_house')
                closest_waffle_house_tag.text = str(row[3])

                wh_latitude_tag = ET.SubElement(pairing_tag, 'wh_latitude')
                wh_latitude_tag.text = str(row[4])

                wh_longitude_tag = ET.SubElement(pairing_tag, 'wh_longitude')
                wh_longitude_tag.text = str(row[5])

                distance_tag = ET.SubElement(pairing_tag, 'distance')
                distance_tag.text = str(row[6])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            result = {'waffle_house': [{'meteorite_name': row[0], 'meteorite_latitude': row[1], 'meteorite_longitude': row[2],
                       'closest_waffle_house': row[3], 'wh_latitude': row[4], 'wh_longitude': row[5],
                       'distance': row[6]} for row in data]}
            return jsonify(result)

    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500


@app.route('/api/closest_waffle_houses_to_me', methods=['GET'])
def closest_waffle_houses_to_me():
    try:
        user_latitude, user_longitude = get_lat_long()

        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, latitude, longitude,
                6371 * acos(
                    cos(radians(?)) * cos(radians(latitude)) *
                    cos(radians(longitude) - radians(?)) +
                    sin(radians(?)) * sin(radians(latitude))
                ) AS distance
            FROM waffle_houses
            ORDER BY distance
            LIMIT 5
        ''', (user_latitude, user_longitude, user_latitude))
        closest_waffle_houses = cursor.fetchall()
        conn.close()

        result = [{'name': row[0], 'latitude': row[1], 'longitude': row[2], 'distance': row[3]} for row in closest_waffle_houses]

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('waffle_houses')
            for row in closest_waffle_houses:
                waffle_house_tag = ET.SubElement(root, 'waffle_house')

                name_tag = ET.SubElement(waffle_house_tag, 'name')
                name_tag.text = str(row[0])

                latitude_tag = ET.SubElement(waffle_house_tag, 'latitude')
                latitude_tag.text = str(row[1])

                longitude_tag = ET.SubElement(waffle_house_tag, 'longitude')
                longitude_tag.text = str(row[2])

                distance_tag = ET.SubElement(waffle_house_tag, 'distance')
                distance_tag.text = str(row[3])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            return jsonify({'closest_waffle_houses': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/closest_waffle_houses_to_me/max_distance/<distance>', methods=['GET'])
def closest_waffle_houses_to_me_max_distance(distance):
    try:
        user_latitude, user_longitude = get_lat_long()
        distance = float(distance)

        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, latitude, longitude,
                6371 * acos(
                    cos(radians(?)) * cos(radians(latitude)) *
                    cos(radians(longitude) - radians(?)) +
                    sin(radians(?)) * sin(radians(latitude))
                ) AS distance
            FROM waffle_houses
            WHERE distance <= ?
            ORDER BY distance
        ''', (user_latitude, user_longitude, user_latitude, distance))
        closest_waffle_houses = cursor.fetchall()
        conn.close()

        result = [{'name': row[0], 'latitude': row[1], 'longitude': row[2], 'distance': row[3]} for row in closest_waffle_houses]

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('waffle_houses')
            for row in closest_waffle_houses:
                waffle_house_tag = ET.SubElement(root, 'waffle_house')

                name_tag = ET.SubElement(waffle_house_tag, 'name')
                name_tag.text = str(row[0])

                latitude_tag = ET.SubElement(waffle_house_tag, 'latitude')
                latitude_tag.text = str(row[1])

                longitude_tag = ET.SubElement(waffle_house_tag, 'longitude')
                longitude_tag.text = str(row[2])

                distance_tag = ET.SubElement(waffle_house_tag, 'distance')
                distance_tag.text = str(row[3])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            return jsonify({'closest_waffle_houses': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/closest_meteorites_to_me', methods=['GET'])
def closest_meteorites_to_me():
    try:
        user_latitude, user_longitude = get_lat_long()

        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, latitude, longitude,
                6371 * acos(
                    cos(radians(?)) * cos(radians(latitude)) *
                    cos(radians(longitude) - radians(?)) +
                    sin(radians(?)) * sin(radians(latitude))
                ) AS distance
            FROM meteorite_landings
            ORDER BY distance
            LIMIT 5
        ''', (user_latitude, user_longitude, user_latitude))
        closest_meteorites = cursor.fetchall()
        conn.close()

        result = [{'name': row[0], 'latitude': row[1], 'longitude': row[2], 'distance': row[3]} for row in closest_meteorites]

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('meteorites')
            for row in closest_meteorites:
                meteorite_tag = ET.SubElement(root, 'meteorite')

                name_tag = ET.SubElement(meteorite_tag, 'name')
                name_tag.text = str(row[0])

                latitude_tag = ET.SubElement(meteorite_tag, 'latitude')
                latitude_tag.text = str(row[1])

                longitude_tag = ET.SubElement(meteorite_tag, 'longitude')
                longitude_tag.text = str(row[2])

                distance_tag = ET.SubElement(meteorite_tag, 'distance')
                distance_tag.text = str(row[3])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            return jsonify({'closest_meteorites': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/closest_meteorites_to_me/max_distance/<distance>', methods=['GET'])
def closest_meteorites_to_me_max_distance(distance):
    try:
        user_latitude, user_longitude = get_lat_long()
        distance = float(distance)

        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, latitude, longitude,
                6371 * acos(
                    cos(radians(?)) * cos(radians(latitude)) *
                    cos(radians(longitude) - radians(?)) +
                    sin(radians(?)) * sin(radians(latitude))
                ) AS distance
            FROM meteorite_landings
            WHERE distance <= ?
            ORDER BY distance
        ''', (user_latitude, user_longitude, user_latitude, distance))
        closest_meteorites = cursor.fetchall()
        conn.close()

        result = [{'name': row[0], 'latitude': row[1], 'longitude': row[2], 'distance': row[3]} for row in closest_meteorites]

        response_format = request.args.get('response')
        if response_format == 'xml':
            root = ET.Element('meteorites')
            for row in closest_meteorites:
                meteorite_tag = ET.SubElement(root, 'meteorite')

                name_tag = ET.SubElement(meteorite_tag, 'name')
                name_tag.text = str(row[0])

                latitude_tag = ET.SubElement(meteorite_tag, 'latitude')
                latitude_tag.text = str(row[1])

                longitude_tag = ET.SubElement(meteorite_tag, 'longitude')
                longitude_tag.text = str(row[2])

                distance_tag = ET.SubElement(meteorite_tag, 'distance')
                distance_tag.text = str(row[3])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            return jsonify({'closest_meteorites': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/nearby_locations/latitude/<latitude>/longitude/<longitude>', methods=['GET'])
def nearby_locations(latitude, longitude):
    try:
        if latitude.startswith("neg_"):
            latitude = "-" + latitude[4:]
        if longitude.startswith("neg_"):
            longitude = "-" + longitude[4:]

        latitude = float(latitude)
        longitude = float(longitude)

        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()

        range_km = 10  
        min_latitude = latitude - (180 / math.pi) * (range_km / 6371)
        max_latitude = latitude + (180 / math.pi) * (range_km / 6371)
        min_longitude = longitude - (180 / math.pi) * (range_km / 6371) / math.cos(math.radians(latitude))
        max_longitude = longitude + (180 / math.pi) * (range_km / 6371) / math.cos(math.radians(latitude))

        cursor.execute('''
            SELECT *
            FROM meteorite_landings
            WHERE latitude BETWEEN ? AND ?
            AND longitude BETWEEN ? AND ?
        ''', (min_latitude, max_latitude, min_longitude, max_longitude))
        nearby_meteorites = cursor.fetchall()

        cursor.execute('''
            SELECT *
            FROM waffle_houses
            WHERE latitude BETWEEN ? AND ?
            AND longitude BETWEEN ? AND ?
        ''', (min_latitude, max_latitude, min_longitude, max_longitude))
        nearby_waffle_houses = cursor.fetchall()

        conn.close()

        response_format = request.args.get('response', 'json')

        if response_format == 'xml':
            root = ET.Element('data')
            meteorites_tag = ET.SubElement(root, 'nearby_meteorites')
            for row in nearby_meteorites:
                meteorite_tag = ET.SubElement(meteorites_tag, 'meteorite')
                name_tag = ET.SubElement(meteorite_tag, 'name')
                name_tag.text = str(row[0])
                latitude_tag = ET.SubElement(meteorite_tag, 'latitude')
                latitude_tag.text = str(row[6])
                longitude_tag = ET.SubElement(meteorite_tag, 'longitude')
                longitude_tag.text = str(row[7])

            waffle_houses_tag = ET.SubElement(root, 'nearby_waffle_houses')
            for row in nearby_waffle_houses:
                waffle_house_tag = ET.SubElement(waffle_houses_tag, 'waffle_house')
                name_tag = ET.SubElement(waffle_house_tag, 'name')
                name_tag.text = str(row[0])
                latitude_tag = ET.SubElement(waffle_house_tag, 'latitude')
                latitude_tag.text = str(row[5])
                longitude_tag = ET.SubElement(waffle_house_tag, 'longitude')
                longitude_tag.text = str(row[6])

            response = ET.tostring(root)
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            response_data = {
                'nearby_meteorites': [{'name': row[0], 'latitude': row[6], 'longitude': row[7]} for row in nearby_meteorites],
                'nearby_waffle_houses': [{'name': row[0], 'latitude': row[5], 'longitude': row[6]} for row in nearby_waffle_houses]
            }
            return jsonify(response_data), 200

    except (sqlite3.Error, ValueError) as e:
        return jsonify({'error': 'Invalid request'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=4000)
