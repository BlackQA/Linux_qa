import pytest
import pymysql
import os
from pymysql.cursors import DictCursor


def pytest_addoption(parser):
    parser.addoption(
        "--host",
        default=os.getenv("DB_HOST", "192.168.0.119"),
        help="Host for MariaDB connection",
    )
    parser.addoption(
        "--port",
        default=os.getenv("DB_PORT", "3306"),
        help="Port for MariaDB connection",
    )
    parser.addoption(
        "--database",
        default=os.getenv("DB_NAME", "bitnami_opencart"),
        help="Database name for OpenCart",
    )
    parser.addoption(
        "--user",
        default=os.getenv("DB_USER", "bn_opencart"),
        help="Username for MariaDB connection",
    )
    parser.addoption(
        "--password",
        default=os.getenv("DB_PASSWORD", ""),
        help="Password for MariaDB connection",
    )


@pytest.fixture(scope="session")
def connection(request):
    try:
        host = request.config.getoption("--host")
        port = int(request.config.getoption("--port"))
        database = request.config.getoption("--database")
        user = request.config.getoption("--user")
        password = request.config.getoption("--password")

        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=DictCursor,
            autocommit=True,
        )

        yield connection
    except pymysql.MySQLError as e:
        pytest.exit(f"Ошибка подключения к базе данных: {e}")
