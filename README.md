Art-Gallery-SQL
===================

# TO DO:
* Add semantic integrities:
1. A piece can only have a buyer if its value is not 0
2. A person can only visit an exposition if its enter time is at least 1 hour before its ending.

**Database I made for an university exam**

# Features <h1>
1. You can:
* Add entities and relations to the database.
* Remove them.
* Edit them.
* Search/Check them.

2. Dates and time will be standardized to an specific format:
* A date will always be formatted to 2-characters day/2-characaters month/4-characters year
* A time will always be formatted to 2-characters hour:2-characaters minute

3. You can check any table with any attribute, not just their keys. If multiple rows have the same field, the program will provide a list of matching rows.

4. To edit or remove rows, you MUST provide their primary keys. If a table has only foreign keys, then all of them must be provided.

5. Certain inputs, like CPF, Phone, date, time, etc., have validation functions, which means that only valid inputs will be accepted.

# Tables <h1>
Tables can be entities and relations.

# Entities <h2>
Entities are usually represented by nouns.

# Person <h3>
People can be visitors, buyers, or artists.

1. **CPF** as a string and primary key
2. **Phone** as a string
3. **Date of birth** as a string
4. **Name** as a string

# Piece <h3>
A piece can be literally any piece of art.

1. **A random ID** as an integer and primary key
2. **Title** as an optional string
3. **Description** as an optional string
4. **Value** as a float. This value will be 0 case the piece is not for sale.
5. **Creation date** as a string
6. **A person's CPF** as an optional string and foreign key, representing the buyer of such piece. This field is NULL if there is no owner. If the owner is removed from the database, the trigger will set this field to NULL.

# Exposition <h3>
Expositions last 6 hours.

1. **A random ID** as an integer and primary key
2. **Title** as a string 
3. **Date** as a string
4. **Time** as a string

# Relations <h2>
Relations are usually represented by verbs.

# Creates <h3>
This relation links the entities __Person__ and __Piece__. It represents the author(s) of a piece. Notice that the same piece might have multiple people (authors) and an person (author) might have multiple pieces (or none), therefore this relation is (1, n) <-> (0, n).

1. **A person's CPF** as a string and foreign key
2. **A piece's ID** as an integer and foreign key

If either of these table keys is deleted, the whole table will be deleted as well.

# Visits <h3>
This relation links the entities __Person__ and __Exposition__. It represents a visit of a person to an exposition. The same person might have visited multiple expositions, but, in order to even be registered in this database, such person must have visited at least one exposition. A exposition might have none or multiple people visiting it, thus this relation is (1, n) <-> (0, n).

1. **An exposition's ID** as an integer and foreign key
2. **A person's CPF** as a string and foreign key
3. **Enter time** as a string
4. **Leave time** as a string

If either of these table keys is deleted, the whole table will be deleted as well.

# Displays <h3>
This relation links the entities __Piece__ and __Exposition__. It represents the pieces displayed on an exposition. The same exposition might have multiple pices but at least one, and a piece might have been in none or multiple expositions, thus this relation is (1, n) <-> (0, n).

1. **An exposition's ID** as an integer and foreign key
2. **A piece's ID** as an integer and foreign key

If either of these table keys is deleted, the whole table will be deleted as well.

# Buys <h3>
There's a fourth relation in this database, but it is (1, 1) <-> (0, n). Since a piece can be bought by only one person. Therefore there's no need for a table specifically for this relation. Instead, the ID of the entity __Person__ is imported to __Piece__.


