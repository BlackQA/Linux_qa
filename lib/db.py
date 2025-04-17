import pymysql


def create_customer(connection, customer_data: dict) -> int:
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO oc_customer (
                    customer_group_id,
                    store_id,
                    language_id,
                    firstname,
                    lastname,
                    email,
                    telephone,
                    password,
                    custom_field,
                    newsletter,
                    ip,
                    status,
                    safe,
                    token,
                    code,
                    date_added
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
                )
            """
            cursor.execute(
                sql,
                (
                    customer_data.get("customer_group_id", 1),
                    customer_data.get("store_id", 0),
                    customer_data.get("language_id", 1),
                    customer_data.get("firstname", ""),
                    customer_data.get("lastname", ""),
                    customer_data.get("email", ""),
                    customer_data.get("telephone", ""),
                    customer_data.get("password", ""),
                    customer_data.get("custom_field", ""),
                    customer_data.get("newsletter", 0),
                    customer_data.get("ip", ""),
                    customer_data.get("status", 1),
                    customer_data.get("safe", 1),
                    customer_data.get("token", ""),
                    customer_data.get("code", ""),
                ),
            )
            customer_id = cursor.lastrowid
            return customer_id
    except pymysql.MySQLError as e:
        return None


def update_customer(connection, customer_id: int, customer_data: dict) -> bool:
    try:
        with connection.cursor() as cursor:
            fields = []
            values = []
            if "firstname" in customer_data:
                fields.append("firstname = %s")
                values.append(customer_data["firstname"])
            if "lastname" in customer_data:
                fields.append("lastname = %s")
                values.append(customer_data["lastname"])
            if "email" in customer_data:
                fields.append("email = %s")
                values.append(customer_data["email"])
            if "telephone" in customer_data:
                fields.append("telephone = %s")
                values.append(customer_data["telephone"])
            if "password" in customer_data:
                fields.append("password = %s")
                values.append(customer_data["password"])
            if "custom_field" in customer_data:
                fields.append("custom_field = %s")
                values.append(customer_data["custom_field"])
            if "newsletter" in customer_data:
                fields.append("newsletter = %s")
                values.append(customer_data["newsletter"])
            if "ip" in customer_data:
                fields.append("ip = %s")
                values.append(customer_data["ip"])
            if "status" in customer_data:
                fields.append("status = %s")
                values.append(customer_data["status"])
            if "safe" in customer_data:
                fields.append("safe = %s")
                values.append(customer_data["safe"])
            if "token" in customer_data:
                fields.append("token = %s")
                values.append(customer_data["token"])
            if "code" in customer_data:
                fields.append("code = %s")
                values.append(customer_data["code"])

            if not fields:
                return False

            values.append(customer_id)
            sql = f"""
                UPDATE oc_customer
                SET {', '.join(fields)}
                WHERE customer_id = %s
            """
            cursor.execute(sql, tuple(values))
            if cursor.rowcount == 0:
                return False
            return True
    except pymysql.MySQLError as e:
        return False


def delete_customer(connection, customer_id: int) -> bool:
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM oc_customer WHERE customer_id = %s"
            cursor.execute(sql, (customer_id,))
            if cursor.rowcount == 0:
                return False
            return True
    except pymysql.MySQLError as e:
        return False


def get_customer(connection, customer_id: int) -> dict:
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM oc_customer WHERE customer_id = %s"
            cursor.execute(sql, (customer_id,))
            result = cursor.fetchone()
            return result
    except pymysql.MySQLError as e:
        return None
