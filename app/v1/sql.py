table_create_sql = [
    """ CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                firstname  VARCHAR(55) NOT NULL,
                lastname  VARCHAR(55) NOT NULL,
                othername  VARCHAR(55),
                email TEXT UNIQUE NOT NULL,
                phoneNumber VARCHAR(15),
                psnumber TEXT NOT NULL,
                password TEXT  NOT NULL,
                isAdmin  BOOLEAN NOT NULL DEFAULT FALSE,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );""",
        
       """ CREATE  TABLE IF NOT EXISTS services(
            id SERIAL PRIMARY KEY,
            water BOOLEAN DEFAULT True,
            electricity  BOOLEAN DEFAULT True,
            roads  BOOLEAN DEFAULT True
        );
        """,
        """
        CREATE  TABLE IF NOT EXISTS products(
            id SERIAL PRIMARY KEY,
            services_id  INTEGER NOT NULL,
            project_name  VARCHAR(55) NOT NULL,
            project_type  VARCHAR(55) NOT NULL,
            size          VARCHAR(55),
            county        VARCHAR(55) NOT NULL,
            location      VARCHAR(55) NOT NULL,
            location_info TEXT NOT NULL,
            price         NUMERIC (9,2) NOT NULL,
            other_information TEXT NOT NULL,
            image        BYTEA NOT NULL,
            sold_out  BOOLEAN DEFAULT False,
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updatedAt  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(services_id) REFERENCES services(id) ON UPDATE CASCADE ON DELETE CASCADE
        );
     """
    ]
drop_tables2 = """DROP TABLE
                users, services, products;"""
                