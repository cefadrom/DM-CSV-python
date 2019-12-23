import codecs
import csv
import re

"""
----- Tache finale sur le python : manipuler des tableaux -----

Structure :
- Les noms de fonctions sont en anglais, mais sont documentées en français avec une docstring de style Sphinx
- Le code est découpé avec des commentaires pour séparer les différentes questions.
    - Les fonctions sont écrites au fur et à mesure de leur besoin
- Des variables sont fréquemment supprimées lorsqu'elles ne sont plus utiles avec le mot clé del,
 afin de libérer de la ram
 
Vocabulaire :
- Une liste de tuples contanant les données sera appelée table
- Une ligne d'une table sera appelée row
- Une colone d'une table sera appelée column
- Une case d'une table sera appelée cell (parfois value quand il s'agit d'un traitement spécifique)

Code entièrement rédigé par Julien Wolff, aucun copié collé d'internet n'a été réalisé
"""


def print_state(title, body):
    """
    Permet d'annoncer les différents exercices dans la console plus facilement
    :param str title: le titre de l'exercice
    :param str body: le sous titre, le plus souvent un résumé de l'énoncé
    """
    print('\n\n-------------------- {} --------------------\n{}\n'
          .format(title.upper(), body))


# ---------- INTRO -----------
print_state('Intro', 'Définition des fonctions principales')


def get_table_content(file_name):
    """
    Permet d'obtenir les données d'un fichier CSV sous la forme le tuples dans une liste
    :param str file_name: l'emplacement du fichier
    :return: le contenu du fichier
    """
    file = codecs.open(file_name, encoding='UTF-8')
    content = csv.reader(file, delimiter=';')
    content = [tuple(x) for x in content]
    file.close()
    return content


def display_table(table, start=0, end=None):
    """
    Permet d'afficher le contenu d'une table proprement dans la console
    :param list[tuple] table: la table à afficher
    :param int start: l'index de la permière ligne d'ou démarrer l'affichage
    :param int end: l'index de la dernière ligne d'ou arreter l'affichage
    """
    stats = {
        'rows': len(table),
        'displayed_rows': end if end and end < len(table) else len(table) - start,
        'columns': len(table[0])
    }
    print_list = list()  # Print toutes les lignes d'un coup pour une meilleure performance

    print_list.append('{} lignes ({} affichées), {} colones, {} cellules ({} affichées)'
                      .format(stats['rows'], stats['displayed_rows'], stats['columns'],
                              stats['rows'] * stats['columns'],
                              stats['displayed_rows'] * stats['columns']))

    new_table = table[start:end]
    row_max_length = get_rows_max_length(new_table)

    for row in new_table:
        print_list.append('+' + '+'.join(['-' * (length + 2) for length in row_max_length]) + '+')
        print_list.append(
            '| ' + ' | '.join(
                [str(cell) + ' ' * (row_max_length[index] - len(str(cell))) for index, cell in enumerate(row)]
            ) + ' |')

    print_list.append('+' + '+'.join(['-' * (length + 2) for length in row_max_length]) + '+')

    print(*print_list, sep='\n')  # print toutes les lignes


def filter_table_columns(table, *columns):
    """
    Permet de ne garder que les colones spécifiées
    :param list[tuple] table: la table à filtrer
    :param int columns: numéros des colones à garder
    :return list[tuple]: la table filtrée
    """
    if not columns:
        return table
    else:
        new_table = []
        for index, row in enumerate(table):
            new_table.append([
                cell
                for cell_index, cell
                in enumerate(row)
                if cell_index in columns
            ])
        return new_table


def change_table_direction(table):
    """
    Permet de "tourner la table de 45°".
    Cette fonction convertis une liste contenant les lignes dans des tuples en une liste contenant les colones dans des
    tuples

    :param list[tuple] table: la table à convertir
    :return list[tuple]: la table convertie
    """
    new_table = [[] for x in table[0]]
    for row in table:
        for index, cell in enumerate(row):
            new_table[index].append(cell)
    new_table = [tuple(x) for x in new_table]
    return new_table


def get_rows_max_length(table):
    """
    Permet de calculer le nombre de caractères de la plus longue valeur de chaque colone d'une table
    :param list[tuple] table: la table source
    :return list[int]: une liste contenant la longueur maximale de chaque colone
    """
    new_table = change_table_direction(table)
    row_max_length = [0 for i in table[0]]
    for index, row in enumerate(new_table):
        row_max_length[index] = max([len(str(cell)) for cell in row])
    return row_max_length


def join_tables(table1, table2):
    """
    Permet d'effectuer le produit cartésien de deux tables
    :param list[tuple] table1: permière table
    :param list[tuple] table2: seconde table
    :return list[tuple]: le produit cartésien des deux tables
    """
    new_table = list()
    for row1 in table1:
        for row2 in table2:
            new_table.append(row1 + row2)
    new_table = [tuple(row) for row in new_table]
    return new_table


table_lang = get_table_content('langues.csv')
table_country = get_table_content('pays.csv')
table_city = get_table_content('villes.csv')

# ---------- Question 1 ----------
print_state('Question 1', 'Les villes qui commencent par "pa"')


def filter_table_by_regex(table, column_index, regex):
    """
    Permet de filter une table en regardant si les valeurs de la colone spécifiée respectent l'expression régulière
    :param list[tuple] table: la table source
    :param int column_index: l'index de la colone à filtrer
    :param str regex: l'expression régulière qui sert de filtre
    :return list[tuple]: la table filtrée
    """
    return [row for row in table if re.match(regex, row[column_index], flags=re.IGNORECASE)]


display_table(
    filter_table_by_regex(table_city, 1, '^pa'),
    0, 10
)

# ---------- Question 2 ----------
print_state('Question 2', 'Les pays d\'Amérique du Sud')

display_table(
    filter_table_by_regex(table_country, 2, '^south america$'),
    0, 10
)

# ---------- Question 3 ----------
print_state('Question 3', 'Les villes d\'Europe qui commencent par "pa"')


def filter_table_by_list(table, column_index, whitelist):
    """
    Permet de filtrer une table en regardant si les valeurs de la colone spécifiée sont dans une liste blanche
    :param list[tuple] table: la table source
    :param int column_index: l'index de la colone à filtrer
    :param tuple[str] | list[str] | set[str] whitelist: la liste blanche
    :return list[tuple]: la table filtrée
    """
    return [row for row in table if row[column_index] in whitelist]


europe_country_codes = [row[0] for row in filter_table_by_regex(table_country, 2, 'europe')]
europe_cities = filter_table_by_list(table_city, 2, europe_country_codes)

del europe_country_codes

display_table(
    filter_table_by_regex(europe_cities, 1, '^pa'),
    0, 10
)

# ---------- Question 4 ----------
print_state('Question 4', 'Villes d\'Europe de plus de 100k habitants')


def filter_table_by_comparator(table, column_index, comparator, number):
    """
    Permet de filtrer une table en regardant si les valeurs de la colone spécifiée sont supérieurs, inférieurs, ou
    égaux au nombre spécifié
    :param list[tuple] table: la table source
    :param int column_index: l'index de la colone à filtrer
    :param str comparator: le signe qui permet de comparer (>, <=, == et autres)
    :param int number: le nombre auquel les valeurs sont comparées
    :return list[tuple]: la table filtrée
    """
    return [row for row in table if row[column_index] != 'NULL' and eval(row[column_index] + comparator + str(number))]


display_table(
    filter_table_by_comparator(europe_cities, 4, '>', 100_000),
    0, 10
)

del europe_cities

# ---------- Question 5 ----------
print_state('Question 5', 'Nombre de formes de gouvernements')


def get_unique_values_on_column(table, column_index):
    """
    Permet de récupérer une tuple contenant toutes les valeurs de la colone spécifiée, en évitant les doublons
    :param list[tuple] table: la table source
    :param column_index: l'index de la colone à récupérer
    :return tuple[str]: tuple contenant les valeurs uniques
    """
    # Mettre les valeurs désirées dans un set permet de retirer les doublons
    return tuple(set([cell[column_index] for cell in table]))


print('Il y a {} formes différentes de gouvernements'.format(len(get_unique_values_on_column(table_country, 11))))

# ----------- Question 6 ----------
print_state('Question 6', 'Nombre de pays dans la base')

print('Il y a {} pays dans la base'.format(len(get_unique_values_on_column(table_country, 1))))

# ---------- Question 7 ----------
print_state('Question 7', 'Pays on l\'on parle français')


def filter_duplicated_rows(table, column_index):
    """
    Permet retirer les lignes dupliquées en prenant pour échantillon la colone spécifiée.
    Seul la première ligne de chaque doublons sera gardée
    :param list[tuple] table: la table source
    :param int column_index: l'index de la colone servant d'échantillon
    :return list[tuple]: la liste filtrée
    """
    column_data = list()
    new_table = list()
    for row in table:
        if not row[column_index] in column_data:
            new_table.append(row)
            column_data.append(row[column_index])
    return new_table


french_lang_countries = filter_table_by_regex(table_lang, 1, '^french$')

display_table(
    filter_table_by_list(
        table_country,
        0,
        get_unique_values_on_column(
            french_lang_countries, 0
        )
    ), 0, 10
)

# ---------- Question 8 ----------
print_state('Question 8', 'Pays ou le français est la langue officielle')

french_official_lang_countries = filter_table_by_list(
    table_country,
    0,
    get_unique_values_on_column(
        filter_table_by_regex(
            french_lang_countries,
            2,
            '^T$'
        ), 0
    )
)

del french_lang_countries

display_table(french_official_lang_countries, 0, 10)

# ---------- Question 9 ----------
print_state('Question 9', 'Villes d\'Afrique de moins de 100k habitants ayant pour langue officielle le français')

display_table(
    filter_table_by_regex(
        filter_table_by_comparator(french_official_lang_countries, 6, '<', 100_000),
        2,
        'africa'
    ),
    0, 10
)

del french_official_lang_countries

# ---------- Question 10 ----------
print_state('Question 10', 'Pays d\'Amérique du Sud de plus de 10m habitants ayant un régime républicain')

display_table(
    filter_table_by_regex(  # Filtre : régime républicain
        filter_table_by_comparator(  # Filtre : plus de 10m d'habitants
            filter_table_by_regex(table_country, 2, 'South america'),  # Filtre : Amérique du Sud
            6, '>', 10_000_000
        ), 11, '^republic$'),
    0, 10
)

# ---------- Question 11 ----------
print_state('Question 11', 'Villes Nord-Américaines de plus de 100k habitants ou l\'on parle espagnol')

spanish_country_codes = get_unique_values_on_column(
    filter_table_by_regex(
        table_lang,
        1,
        'spanish'
    ), 0
)

north_american_country_codes = get_unique_values_on_column(
    filter_table_by_regex(
        table_country,
        2,
        'North America'
    ), 0
)

display_table(
    filter_table_by_list(  # Filtre : Nord-Américain
        filter_table_by_list(  # Filtre : parle espagnol
            filter_table_by_comparator(  # Filtre : plus de 100K habitants
                table_city,
                4,
                '>',
                100_000
            ), 2, spanish_country_codes
        ), 2, north_american_country_codes
    ), 0, 10
)

del spanish_country_codes, north_american_country_codes

# ---------- Question 12 ----------
print_state('Question 12', 'Surface de l\'Europe')


def summarize_column(table, column_index):
    """
    Permet de faire le total des nombres de la colone d'un tableau
    :param list[tuple] table: la table source
    :param int column_index: l'index de la colone à traiter
    :return : un objet dans lequel se trouve le nombre total (clé sum) et le nombre de valeurs traitées (clé count)
    """
    total = float()
    matches = 0
    for row in table:
        if re.match('^\\d+(\\.\\d+)?$', row[column_index]):  # On teste si c'est un nombre pour éviter les erreurs
            total += float(row[column_index])
            matches += 1
    return {'sum': total, 'count': matches}


europe_countries = filter_table_by_regex(table_country, 2, 'Europe')

print('L\'Europe a une surface de {} km².'.format(summarize_column(europe_countries, 4)['sum']))

# del europe_countries

# ---------- Question 13 ----------
print_state('Question 13', 'Surface de la polynésie')

polynesia_countries = filter_table_by_regex(table_country, 3, 'Polynesia')

print('La polynésie a une surface de {} km².'.format(summarize_column(polynesia_countries, 4)['sum']))

del polynesia_countries

# ---------- Question 14 ----------
print_state('Question 14', 'Pays en Océanie de plus de 10k km²')

oceania_countries = filter_table_by_regex(table_country, 2, 'oceania')
large_oceania_coutries = filter_table_by_comparator(oceania_countries, 8, '>', 10_000)

print('En Océanie, il y a {} pays qui font plus de 10.000 km².'
      .format(len(large_oceania_coutries)))

del oceania_countries, large_oceania_coutries

# ---------- Question 15 ----------
print_state('Question 15', "Langues officielles des pays de l'Europe de l'Est")

est_europe_country_codes = get_unique_values_on_column(  # On récupère les codes des pays
    filter_table_by_regex(table_country, 3, 'Eastern Europe'),  # On récupère les pays
    0
)

est_europe_langs = get_unique_values_on_column(  # On récupère les langues
    filter_table_by_list(  # On filtre les langues en fonction des codes des pays
        table_lang,
        0,
        est_europe_country_codes
    ),
    1
)

print("Langues des pays d'Europe de l'Est :", (', '.join(est_europe_langs)))

del est_europe_langs, est_europe_country_codes

# ---------- Question 16 ----------
print_state('Question 16', 'Population moyenne des pays d\'Asie')

asia_countries = filter_table_by_regex(  # On filtre la table en ne gardant que les pays d'Asie
    table_country,
    2,
    'asia'
)

asia_population = summarize_column(asia_countries, 6)

print('En Asie, la population moyenne dans les {} pays est de {} habitants'
      .format(asia_population['count'], round(asia_population['sum'] / asia_population['count'], 1)))

del asia_population

# ---------- Question 17 ----------
print_state('Question 17', 'Population moyenne des villes d\'Asie')

asia_country_codes = get_unique_values_on_column(asia_countries, 0)  # On récupère les codes des pays d'Asie

asia_cities = filter_table_by_list(  # On filtre la table en ne gardant que les villes d'Asie
    table_city,
    2,
    asia_country_codes
)

asia_cities_pop = summarize_column(asia_cities, 4)

print('En Asie, la population moyenne dans les {} villes est de {} habitants'
      .format(asia_cities_pop['count'], round(asia_cities_pop['sum'] / asia_cities_pop['count'], 1)))

del asia_cities, asia_country_codes, asia_cities_pop

# ---------- Question 18 ----------
print_state('Question 18', 'Capitales d\'Europe ordonnées par ordre alphabétique')


def order_table_by_column(table, column_index, reverse=False):
    """
    Permet de trier une table à partir de la colone spécifiée
    :param list[tuple] table: la table à trier
    :param int column_index: l'index de la colone qui sert de référence
    :param boolean reverse: true si on doit trier la table dans le sens inverse
    :return list[tuple]: la table triée
    """
    return sorted(table, key=lambda x: x[column_index], reverse=reverse)


europe_capitales_ids = get_unique_values_on_column(
    europe_countries,
    13
)

europe_capitales_cities = filter_table_by_list(
    table_city,
    0,
    europe_capitales_ids
)

display_table(
    order_table_by_column(europe_capitales_cities, 1),
    0, 10
)

del europe_capitales_ids, europe_countries, europe_capitales_cities

# ---------- Question 19 ----------
print_state('Question 19', 'Villes d\'Afrique ou la capitale a plus de 3m habitants')

africa_capitales_ids = get_unique_values_on_column(  # On récupère les identifiants des capitales
    filter_table_by_regex(  # On récupère les pays d'Afrique
        table_country,
        2,
        'Africa'
    ),
    13
)

africa_big_population_countries_codes = get_unique_values_on_column(  # On récupère les codes des pays
    filter_table_by_comparator(  # On filtre celles qui ont moins de 3m habitants
        filter_table_by_list(  # On récupère les capitales d'Afrique
            table_city,
            0,
            africa_capitales_ids
        ),
        4, '>', 3_000_000
    ),
    2
)

display_table(
    filter_table_by_list(  # On récupère les villes d'après les codes trouvés au dessus
        table_city,
        2,
        africa_big_population_countries_codes
    ), 0, 10
)

del africa_capitales_ids, africa_big_population_countries_codes

# ---------- Question 20 ----------
print_state('Question 20',
            'Pays d\'Amérique du Nord avec indépendance avant 1912, on parle Portugais et ou il y a plus de 49 villes')

na_countries_independance_1912 = filter_table_by_comparator(  # Filtre : indépendance avant 1912
    filter_table_by_regex(table_country, 2, 'North America'),  # Filtre : pays d'Amérique du Nord
    5, '<', 1912
)

portugese_speaking_country_codes = get_unique_values_on_column(  # On récupère les codes des pays
    filter_table_by_regex(table_lang, 1, 'Portuguese'),  # Filtre : pays ou l'on parle portugais
    0
)

portugese_and_more_49_cities_country_code = list()

for country_code in portugese_speaking_country_codes:
    # On ne garde que les pays qui parlent espagnol et ou il y a plus de 49 états
    if len(
            filter_table_by_list(
                table_city,
                2,
                country_code
            )
    ) > 49:
        portugese_and_more_49_cities_country_code.append(country_code)

display_table(
    filter_table_by_list(  # Filtre : on ne garde que les pays ou l'on parle portugais et ou il y a plus de 49 états
        na_countries_independance_1912,
        0,
        portugese_and_more_49_cities_country_code
    ),
    0, 10
)

del na_countries_independance_1912, portugese_speaking_country_codes, portugese_and_more_49_cities_country_code

# ---------- Question 21 ----------
print_state('Question 21', 'Pays ou toutes le villes ont plus de 100k habitants')

more_100k_country_codes = list()
for country_code in get_unique_values_on_column(table_city, 2):  # Pour chaque code de ville différent
    if min(  # On regarde la plus petite valeur
            # On récupère le nombre d'habitant de chaque ville d'un code de pays
            [int(row[4]) for row in filter_table_by_list(table_city, 2, [country_code])]
    ) > 100_000:
        more_100k_country_codes.append(country_code)

display_table(
    filter_table_by_list(table_country, 0, more_100k_country_codes),
    0, 10
)

del more_100k_country_codes

# ---------- Question 22 ----------
print_state('Question 22', 'Pays dont toutes les villes ont plus d\'habitants que le ville la plus peuplée du Népal')

nepal_max_pop = max(  # Population de la plus grande ville au nepal
    [int(value) for value in  # Convertir chaque str en int
     get_unique_values_on_column(  # On recupère le nombre d'habitants
         filter_table_by_list(table_city, 2, ['NPL']),  # On récupère les villes du népal
         4
     )]
)

more_nepal_country_codes = list()
for country_code in get_unique_values_on_column(table_city, 2):  # Pour chaque code de ville différent
    if min(  # On regarde la plus petite valeur
            # On récupère le nombre d'habitant de chaque ville d'un code de pays
            [int(row[4]) for row in filter_table_by_list(table_city, 2, [country_code])]
    ) > nepal_max_pop:
        more_nepal_country_codes.append(country_code)

display_table(
    filter_table_by_list(table_country, 0, more_nepal_country_codes),
    0, 10
)

del nepal_max_pop, more_nepal_country_codes

# ---------- Question 23 ----------
print_state('Question 23', 'Pays ou l\'on parle français mais pas anglais')

french_speaking_country_codes = set(get_unique_values_on_column(
    filter_table_by_regex(table_lang, 1, 'French'),
    0
))

english_speaking_country_codes = set(get_unique_values_on_column(
    filter_table_by_regex(table_lang, 1, 'english'),
    0
))

display_table(
    filter_table_by_list(
        table_country,
        0,
        french_speaking_country_codes - english_speaking_country_codes
    ),
    0, 10
)

del french_speaking_country_codes, english_speaking_country_codes

# ---------- Question 24 ----------
print_state('Question 24', 'Pays pour lequels au moins une ville est dans la base')

cities_country_codes = get_unique_values_on_column(table_city, 2)  # Codes des pays dans la base "villes.csv"

# Pays qui ont leur code dans la variable cities_country_codes
countries_in_cities_table = [row for row in table_country if row[0] in cities_country_codes]

print('{} pays ont au moins une ville dans la base villes.csv'.format(len(countries_in_cities_table)))

del cities_country_codes, countries_in_cities_table

# ---------- Question 25 ----------
print_state('Question 25', 'Pays pour lesquels aucune langue n\'est répertoriée')

lang_country_codes = get_unique_values_on_column(table_lang, 0)  # Codes des pays dans la base "villes.csv"

# Pays qui n'ont pas leur code dans la variable lang_country_codes
countries_not_in_lang_table = [row for row in table_country if row[0] not in lang_country_codes]

print('{} pays n\'ont aucune langue répertoriée dans la base langues.csv'.format(len(countries_not_in_lang_table)))

del lang_country_codes, countries_not_in_lang_table

# ---------- Question 26 ----------
print_state('Question 26', 'Pays pour lesquels la somme du nombre d\'habitants de ses villes est supérieur à 10m')

filtered_countries_codes = list()
for row in table_country:
    country_code = row[0]
    cities_with_country_code = filter_table_by_list(table_city, 2, [country_code])
    if len(cities_with_country_code) > 0:
        pop_sum = summarize_column(cities_with_country_code, 4)
        if pop_sum['sum'] > 10_000_000:
            filtered_countries_codes.append(country_code)

display_table(
    filter_table_by_list(
        table_country,
        0,
        filtered_countries_codes
    ),
    0, 10
)

if 'FRA' in filtered_countries_codes:
    print('La france est dans le liste')
else:
    print('La france n\'est pas dans la liste')

del filtered_countries_codes

# ---------- Question 27 ----------
print_state('Question 27', 'Le pays asiatique ayant l\'espérance de vie la plus courte')


def convert_column_to_float(table, colomn_index):
    """
    Convertis une colone de strings dans une table en une colone de floats
    :param list[tuple] table: la table source
    :param int colomn_index:
    :return list[tuple]: la table avec la colone convertie
    """
    return [
        tuple(
            list(row[:colomn_index]) + [float(row[colomn_index])] + list(row[colomn_index + 1:])
        )
        for row in table
    ]


asia_countries = convert_column_to_float(asia_countries, 7)
shortest_life_asia = order_table_by_column(asia_countries, 7)[0]

print('Le pays d\'Asie avec l\'espérance de vie la plus courte : {} ({} ans)'
      .format(shortest_life_asia[1], shortest_life_asia[7]))

del asia_countries, shortest_life_asia
