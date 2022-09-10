from psycopg2.sql import Identifier, SQL


class Customers:

    @staticmethod
    def create_structure(conn):
        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS customers
                        (
                            customer_id SERIAL PRIMARY KEY,
                            first_name VARCHAR(100) NOT NULL,
                            last_name VARCHAR(100),
                            email VARCHAR(100)   
                        );
                        """)

            cur.execute("""
                        CREATE TABLE IF NOT EXISTS phone_numbers
                        (
                            phone_id SERIAL PRIMARY KEY,
                            phone_number VARCHAR(30) UNIQUE NOT NULL,
                            customer_id int NOT NULL REFERENCES customers(customer_id)
                        );      
                        """)

    def add_customer(self, conn, first_name, last_name, email, phone_number=None):
        with conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO customers(first_name, last_name, email)
                        VALUES
                        (%s,%s,%s)
                        RETURNING customer_id;
                        """, (first_name, last_name, email))

            if phone_number:
                customer_id = cur.fetchone()[0]
                self.add_phone(conn, customer_id, phone_number)

    @staticmethod
    def add_phone(conn, customer_id, phone_number):
        with conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO phone_numbers(phone_number, customer_id)
                        VALUES
                        (%s,%s);
                        """, (phone_number, customer_id))

    @staticmethod
    def change_phone(cur, customer_id, phone_number):
        phone_id, new_phone_number = phone_number
        cur.execute("""
            UPDATE phone_numbers
            SET phone_number = %s
            WHERE customer_id = %s AND phone_id = %s;
            """, (new_phone_number, customer_id, phone_id))

    @staticmethod
    def __change_param(cur, customer_id, param_name, new_value):
        cur.execute(f"""
                    UPDATE customers
                    SET {param_name} = %s                       
                    WHERE customer_id = %s;
                    """, (new_value, customer_id))  # в данном случае f-строка вроде безопасна

    def change_customer(self, conn, customer_id, *, first_name=None, last_name=None, email=None, phone=None):
        with conn.cursor() as cur:
            if first_name:
                self.__change_param(cur, customer_id, 'first_name', first_name)
            if last_name:
                self.__change_param(cur, customer_id, 'last_name', last_name)
            if email:
                self.__change_param(cur, customer_id, 'email', email)
            if phone:
                self.change_phone(cur, customer_id, phone)

    @staticmethod
    def del_phone(conn, customer_id, phone_number):
        with conn.cursor() as cur:
            cur.execute(f"""
                DELETE 
                FROM phone_numbers
                WHERE customer_id = %s AND phone_number = %s;""", (customer_id, phone_number))

    @staticmethod
    def del_customer(conn, customer_id):
        with conn.cursor() as cur:
            for table in ['phone_numbers', 'customers']:
                cur.execute(
                    SQL("""
                        DELETE
                        FROM {} 
                        WHERE customer_id = %s """).format(Identifier(table)), (customer_id, ))

    @staticmethod
    def find_customer(conn, *, first_name=None, last_name=None, email=None, phone_number=None):
        with conn.cursor() as cur:
            if first_name:
                cur.execute("""
                    SELECT customer_id
                    FROM customers
                    WHERE first_name = %s;""", (first_name,))
            elif last_name:
                cur.execute("""
                    SELECT customer_id
                    FROM customers
                    WHERE last_name = %s;""", (last_name,))
            elif email:
                cur.execute("""
                    SELECT customer_id
                    FROM customers
                    WHERE email = %s;""", (email,))
            elif phone_number:
                cur.execute("""
                    SELECT customer_id
                    FROM customers
                    JOIN phone_numbers USING (customer_id)
                    WHERE phone_number = %s;""", (phone_number,))
            return cur.fetchone()[0]

    @staticmethod
    def drop_all(conn):
        with conn.cursor() as cur:
            cur.execute(f"""
                DROP TABLE IF EXISTS phone_numbers;
                DROP TABLE IF EXISTS customers;
                """)

