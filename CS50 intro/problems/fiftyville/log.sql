-- Keep a log of any SQL queries you execute as you solve the mystery.

-- looking at the crime scene report

SELECT *
    FROM crime_scene_reports
    WHERE (month = 07 AND day = 28);

-- at 10.15am, 3 witnesses, each mention the bakery- happened at the bakery then


SELECT *
    FROM bakery_security_logs
    WHERE (day = 28 AND month = 07 AND hour = 10 AND activity = 'exit');
-- ^^^ licensce plates for the people who entered the shop

SELECT * FROM people
    WHERE license_plate IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE (day = 28 AND month = 07 AND hour = 10 AND activity = 'exit'));
--^names/ids/phone numbers/passport numbers

SELECT name, year, month, day, transcript
    FROM interviews
    WHERE name IN
        (SELECT name FROM people
    WHERE license_plate IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE (day = 28 AND month = 07 AND hour = 10 AND activity = 'exit')));
-- ^^^^^ interviews from anyone who had a license plate in the bakery at the time
-- ^^^^ guy called bruce, references Merryweather a bank manager, and a Jones

SELECT name, year, month, day, transcript
    FROM interviews
    WHERE (day = 28 AND month = 07);

--^^^^ within 10 minutes, one of the cars left, check the licensces
-- ^^^^ earlier, before the theft, the theif was at the atm at Leggett Street
-- ^^^ the thief is taking the earliest flight on the 29th of July with the accomplice and the accomplice is buying the ticket


SELECT *
FROM atm_transactions
WHERE (year = 2021 AND month = 07 and day = 28 and atm_location = "Leggett Street");
-- ^^^ info about the atm transacitons

SELECT person_id
FROM bank_accounts
WHERE account_number IN
    (SELECT account_number
    FROM atm_transactions
    WHERE (year = 2021 AND month = 07 and day = 28 and atm_location = "Leggett Street"));
-- ^^^^ person id and account number



---#########
SELECT id
FROM people
WHERE license_plate IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE (day = 28 AND month = 07 AND hour = 10 AND minute < 30 AND activity = 'exit'))
INTERSECT
SELECT person_id
FROM bank_accounts
WHERE account_number IN
    (SELECT account_number
    FROM atm_transactions
    WHERE (year = 2021 AND month = 07 AND day = 28 AND atm_location = "Leggett Street" and transaction_type = "withdraw"));

-- ^^^^^^^^ A list of 4 people ID's, 1 is the robber


SELECT *
FROM flights
WHERE (year =2021 AND month = 07 AND day = 29 AND hour <9);
-- flying to destination number 4 at 8.20am - flight id 36

SELECT *
FROM airports
WHERE id IN
    (SELECT destination_airport_id
    FROM flights
    WHERE (year =2021 AND month = 07 AND day = 29 AND hour <9));
-- flying to LaGuardia Airport

SELECT *
FROM passengers
WHERE flight_id = 36;

---^^^ passport numbers of the above - 8 of them

SELECT id
FROM people
WHERE passport_number IN
    (SELECT passport_number
    FROM passengers
    WHERE flight_id = 36)
INTERSECT
SELECT id
FROM people
WHERE license_plate IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE (day = 28 AND month = 07 AND hour = 10 AND minute < 30 AND activity = 'exit'))
INTERSECT
SELECT person_id
FROM bank_accounts
WHERE account_number IN
    (SELECT account_number
    FROM atm_transactions
    WHERE (year = 2021 AND month = 07 AND day = 28 AND atm_location = "Leggett Street" and transaction_type = "withdraw"));

---- 2 people, 467400, 686048


SELECT *
FROM phone_calls
WHERE (year = 2021 AND month = 07 AND day = 28 and duration <60)
ORDER BY duration;

--- ^^^^^^ A list of phone numbers


SELECT *
FROM people
WHERE phone_number IN
    (SELECT phone_number
    FROM phone_calls
    WHERE (year = 2021 AND month = 07 AND day = 28 and duration <60)
    ORDER BY duration);

-- the IDs + list of people on the phone

SELECT id
FROM people
WHERE passport_number IN
    (SELECT passport_number
    FROM passengers
    WHERE flight_id = 36)
INTERSECT
SELECT id
FROM people
WHERE license_plate IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE (day = 28 AND month = 07 AND hour = 10 AND minute < 30 AND activity = 'exit'))
INTERSECT
SELECT person_id
FROM bank_accounts
WHERE account_number IN
    (SELECT account_number
    FROM atm_transactions
    WHERE (year = 2021 AND month = 07 AND day = 28 AND atm_location = "Leggett Street" and transaction_type = "withdraw"))
INTERSECT
SELECT id
FROM people
WHERE phone_number IN
    (SELECT phone_number
    FROM phone_calls
    WHERE (year = 2021 AND month = 07 AND day = 28 and duration <60)
    ORDER BY duration);


SELECT passport_number
FROM passengers
WHERE flight_id = 36
INTERSECT
SELECT passport_number
FROM passengers
WHERE passport_number IN
    (SELECT passport_number
    FROM people
    WHERE (id = 467400 or id = 686048));



-- finally, the 2 passport numbers  ^^^^^



SELECT *
FROM people
WHERE passport_number IN
    (SELECT passport_number
    FROM passengers
    WHERE flight_id = 36
    INTERSECT
    SELECT passport_number
    FROM passengers
    WHERE passport_number IN
    (SELECT passport_number
    FROM people
    WHERE (id = 467400 or id = 686048)));


----------------------------------------

SELECT *
FROM phone_calls
JOIN people ON phone_calls.caller = people.phone_number
WHERE people.id = 686048;

SELECT *
FROM people
WHERE phone_number = '(375) 555-8161';