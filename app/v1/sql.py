table_create_sql = [
    """ CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                firstname  VARCHAR(55) NOT NULL,
                lastname  VARCHAR(55) NOT NULL,
                othername  VARCHAR(55),
                email TEXT UNIQUE NOT NULL,
                phoneNumber VARCHAR(15) ,
                passportUrlString TEXT NOT NULL,
                password TEXT  NOT NULL,
                isAdmin  BOOLEAN NOT NULL DEFAULT FALSE,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
     """
    ]
drop_tables2 = """DROP TABLE
                users;"""