--In 13.sql, write a SQL query to list the names of all people who starred in a movie in which Kevin Bacon also starred.
--Your query should output a table with a single column for the name of each person.
--There may be multiple people named Kevin Bacon in the database. Be sure to only select the Kevin Bacon born in 1958.
--Kevin Bacon himself should not be included in the resulting list.


SELECT DISTINCT people.name FROM people
    JOIN stars ON people.id = stars.person_id
    JOIN movies ON stars.movie_id = movies.id
    WHERE movies.id IN
        (SELECT movies.id
        FROM movies
        JOIN stars ON stars.movie_id = movies.id
        JOIN people ON people.id = stars.person_id
        WHERE people.name = 'Kevin Bacon' AND people.birth = 1958)
EXCEPT
SELECT people.name FROM people
    WHERE people.name = 'Kevin Bacon' AND people.birth = 1958;