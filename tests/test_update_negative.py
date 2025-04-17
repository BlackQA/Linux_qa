import pytest
from lib.db import update_customer


@pytest.mark.usefixtures("connection")
def test_update_nonexistent_customer(connection):
    customer_id = 9999999

    updated_data = {
        "firstname": "Несуществующий",
        "lastname": "Клиент",
        "email": "nonexistent@example.com",
        "telephone": "000000000",
    }

    success = update_customer(connection, customer_id, updated_data)
    assert not success, "Обновление данных несуществующего клиента должно вернуть False"
