import pytest

from project import create_app, db 
    
@pytest.fixture(scope="session")
def app():
    app = create_app("mysql://root:@localhost/escala_rosenberg")

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()