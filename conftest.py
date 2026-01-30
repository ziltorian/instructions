import pytest


@pytest.fixture(autouse=True)
def noop_fixture():
    """Минимальная фикстура pytest, выполняемая автоматически."""
    yield
