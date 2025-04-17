import pytest
from lib.db import update_customer, get_customer


@pytest.mark.usefixtures("connection")
def test_update_customer(connection):
    customer_id = 1
    updated_data = {
        "firstname": "Tony",
        "lastname": "Stark",
        "email": "stark@example.com",
        "telephone": "987654777",
    }

    success = update_customer(connection, customer_id, updated_data)
    assert success, "Обновление данных клиента не удалось"

    customer = get_customer(connection, customer_id)
    assert customer is not None, "Клиент не найден в базе данных после обновления"
    assert (
        customer["firstname"] == updated_data["firstname"]
    ), "Имя клиента не обновлено"
    assert (
        customer["lastname"] == updated_data["lastname"]
    ), "Фамилия клиента не обновлена"
    assert customer["email"] == updated_data["email"], "Email клиента не обновлен"
    assert (
        customer["telephone"] == updated_data["telephone"]
    ), "Телефон клиента не обновлен"
