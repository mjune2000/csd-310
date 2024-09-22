import mysql.connector # type: ignore

def show_films(cursor, title):
    cursor.execute("SELECT film_name AS Name, film_director AS Director, genre_name AS Genre, studio_name AS 'Studio Name' FROM film INNER JOIN genre ON film.genre_id = genre.genre_id INNER JOIN studio ON film.studio_id = studio.studio_id")

    films = cursor.fetchall()
    print("\n -- {} --".format (title))
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0], film[1], film[2], film[3]))

def main():
    connection = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "MillieBop2020",
    database= "movies"
)
    cursor = connection.cursor()

    show_films(cursor, "DISPLAYING FILMS")
    
    cursor.execute("""
        INSERT INTO film(film_name, film_director, film_releaseDate, film_runtime, genre_id, studio_id)
        VALUES (
            'Jurassic World', 
            'Colin Trevorrow',
            '2015',
            '161',
            (SELECT genre_id FROM genre WHERE genre_name ='SciFi'), 
            (SELECT studio_id FROM studio WHERE studio_name ='Universal Pictures')
            );
    """)
    connection.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    cursor.execute("""
        UPDATE film
        SET genre_id = (SELECT genre_id FROM genre WHERE genre_name ='Horror')
        WHERE film_name = 'Alien'
    """)
    connection.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

    cursor.execute("""
        DELETE FROM film
        WHERE film_name = 'Gladiator'
    """)
    connection.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()