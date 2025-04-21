# tests/test_customer_delete_negative.py

import pytest
from lib.db import delete_customer


@pytest.mark.usefixtures("connection")
def test_delete_nonexistent_customer(connection):

    customer_id = 999999

    success = delete_customer(connection, customer_id)
    assert not success, "Удаление несуществующего клиента должно вернуть False"
