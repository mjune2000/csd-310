#Connect to movies database and display 4 queries

import mysql.connector # type: ignore

connection = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "MillieBop2020",
    database= "movies"
)


cursor = connection.cursor()

cursor.execute ("SELECT studio_id, studio_name FROM studio")
studios = cursor.fetchall()
print("DISPLAYING Studio RECORDS:")
for studio_id, studio_name in studios:
    print(f"Studio ID: {studio_id}, Studio Name: {studio_name}")
print("\n")

cursor.execute ("SELECT genre_id, genre_name FROM genre")
genres = cursor.fetchall()
print("DISPLAYING Genre RECORDS:")
for genre_id, genre_name in genres:
    print(f"Genre ID: {genre_id}, Genre: {genre_name}")
print("\n")

cursor.execute("SELECT film_name FROM film WHERE film_runtime < 120")
short_films = cursor.fetchall()
print("DISPLAYING Short Film RECORDS:")
for film_name in short_films:
    print(film_name[0])
print("\n")

cursor.execute("SELECT film_director, GROUP_CONCAT(film_name) AS films FROM film GROUP BY film_director;")
directors_movies = cursor.fetchall()
print("DISPLAYING Director RECORDS:")
for film_director, film_name in directors_movies:
    print(f"Director: {film_director}, Films: {film_name}")
print("\n")

cursor.close()
connection.close()