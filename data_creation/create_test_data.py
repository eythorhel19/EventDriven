

def create_sql_insert_str(data, table):
    columns = []
    if len(data) == 0:
        Exception('Data inserted cannot be of length 0')
    else:
        columns = list(data[0].keys())

    sql_str = ""
    start_str = "INSERT INTO {} (".format(table)

    for i, col in enumerate(columns):
        if i > 0:
            start_str += ', '
        start_str += col

    start_str += ") VALUES ("

    for row in data:
        sql_str += start_str
        for i, elem in enumerate(row.values()):
            if i > 0:
                sql_str += ', '
            sql_str += elem
        sql_str += ');\n'

    return sql_str


def main():
    sql_str = ""

    # Country
    with open('data_creation/raw_data/countries.csv', 'r') as f:
        columns = []
        countries = []

        for i, line in enumerate(f):
            if i == 0:
                columns = list(line.split(','))
            else:
                data = line.split(',')
                if data[columns.index('UNTERM English Short')] == '' or data[columns.index('Dial')] == '':
                    continue
                else:
                    countries.append({
                        'iso3_code': "'{}'".format(data[columns.index('ISO3166-1-Alpha-3')]),
                        'name': "'{}'".format(
                            data[columns.index('UNTERM English Short')].replace('"', '').replace("'", "''")
                        ),
                        'phone_country_code': "'{}'".format(data[columns.index('Dial')])
                    })

        sql_str += create_sql_insert_str(countries, 'Country')

    # Cities

    #  Getting country ids
    country_id_map = {}
    f = open('data_creation/raw_data/country_id_to_iso3.csv', 'r')
    for i, line in enumerate(f):
        if i == 0:
            continue
        data = line.strip().split(';')
        country_id_map[data[1]] = data[0]
    
    print(country_id_map)

    with open('data_creation/raw_data/worldcities.csv', 'r') as f:
        columns = None
        
        cities = []
        for i, line in enumerate(f):
            data = line.replace('"', '').strip().split(",")
            if i == 0:
                columns = data
                continue

            if data[columns.index('iso3')] in country_id_map:
                cities.append({
                    'name': "'{}'".format(data[columns.index('city_ascii')].replace("'", "''")),
                    'country_id': "'{}'".format(country_id_map[data[columns.index('iso3')]])
                })

        sql_str += "\n\n\n" + create_sql_insert_str(cities, 'home_city')
        
    with open('data_creation/location_data.sql', 'w') as f:
        f.write(sql_str)


main()
