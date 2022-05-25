

def create_sql_insert_str(data, table):
    columns = []
    if len(data) == 0:
        Exception('Data inserted cannot be of length 0')
    else:
        columns = list(data[0].keys())

    sql_str = "INSERT INTO {} (".format(table)

    for i, col in enumerate(columns):
        if i > 0:
            sql_str += ', '
        sql_str += col

    sql_str += ") VALUES \n"

    for row in data:
        sql_str += '('
        for i, elem in enumerate(row.values()):
            if i > 0:
                sql_str += ', '
            sql_str += elem
        sql_str += '),\n'

    return sql_str


def main():
    sql_str = ""

    # Country
    with open('data_creation/raw_data/countries.csv', "r") as f:
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
                        'name': data[columns.index('UNTERM English Short')].replace('"', ''),
                        'phone_country_code': data[columns.index('Dial')]
                    })

        sql_str += create_sql_insert_str(countries, 'Country')

        print(sql_str)


main()
