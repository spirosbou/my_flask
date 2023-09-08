from app import app 


def test_get_api():
    with app.test_client() as c:
        response = c.get('/moto')
        json_response = response.get_json()
        assert response.status_code == 200



        