import pytest
from lib.db import delete_customer, get_customer


@pytest.mark.usefixtures("connection")
def test_delete_customer(connection):
    customer_id = 1

    success = delete_customer(connection, customer_id)
    assert success, "Удаление клиента не удалось"

    customer = get_customer(connection, customer_id)
    assert customer is None, "Клиент не был удален из базы данных"
