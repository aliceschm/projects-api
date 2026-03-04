from src.main import create_app
import pytest


@pytest.mark.app
def test_public_app_has_no_admin_routes():
    """Test that the public app does not include admin routes in its OpenAPI schema."""
    app = create_app(include_admin=False)
    schema = app.openapi()

    paths = schema["paths"].keys()

    assert not any(p.startswith("/admin") for p in paths)
