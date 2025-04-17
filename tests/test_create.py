import pytest
from lib.db import create_customer, get_customer


@pytest.mark.usefixtures("connection")
def test_create_customer(connection):
    customer_data = {
        "customer_group_id": 1,
        "firstname": "John",
        "lastname": "Connor",
        "email": "connor@example.com",
        "password": "12345",
    }

    customer_id = create_customer(connection, customer_data)
    assert customer_id is not None, "Клиент не был создан, customer_id равен None"

    customer = get_customer(connection, customer_id)
    assert customer is not None, "Клиент не найден в базе данных"
    assert (
        customer["firstname"] == customer_data["firstname"]
    ), "Имя клиента не совпадает"
    assert (
        customer["lastname"] == customer_data["lastname"]
    ), "Фамилия клиента не совпадает"
    assert customer["email"] == customer_data["email"], "Email клиента не совпадает"
    assert (
        customer["password"] == customer_data["password"]
    ), "Пароль клиента не совпадает"
    assert (
        customer["customer_group_id"] == customer_data["customer_group_id"]
    ), "ID_group не совпадает"
