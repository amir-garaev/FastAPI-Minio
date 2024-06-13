import pytest
import requests

@pytest.fixture
def api_url():
    return "http://0.0.0.0:9999/memes/"

@pytest.fixture
def uploaded_meme_id(api_url):
    img_path_meme = "test_meme_img/pepe_meme.jpg"
    text_meme = "pepe"

    with open(img_path_meme, 'rb') as file:
        files = {'img_meme': (img_path_meme, file, 'image/jpeg')}
        params = {'title_meme': text_meme}
        headers = {'admin-token': 'admin meme'}

        response = requests.post(api_url, files=files, params=params, headers=headers)

        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "meme_id" in data

        return data["meme_id"]

def test_get_meme_id(api_url,uploaded_meme_id):
    url = f"{api_url}{uploaded_meme_id}"
    response = requests.get(url)

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert "title" in data
    assert "image_url" in data


def test_get_all_memes(api_url):
    url = f"{api_url}?skip=0&limit=10"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    for meme in data:
        assert "id" in meme
        assert "title" in meme
        assert "image_url" in meme

def test_update_meme(api_url,uploaded_meme_id):
    url = f"{api_url}{uploaded_meme_id}"
    img_path_meme = "test_meme_img/new_pepe_meme.jpg"
    new_text_meme = "pepe2edition"
    headers = {'admin-token': 'admin meme'}
    with open(img_path_meme, 'rb') as file:
        file = {'img_meme': (img_path_meme, file, 'image/jpeg')}
        params = {'title_meme': new_text_meme}
        response = requests.put(url, files=file, params=params, headers=headers)

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert data["message"] == "Мем успешно обновлен :)"


def test_delete_meme(api_url, uploaded_meme_id):
    url = f"{api_url}{uploaded_meme_id}"
    headers = {'admin-token': 'admin meme'}

    response = requests.delete(url, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Мем успешно удален :)"

def test_no_admin_meme(api_url,uploaded_meme_id):
    img_path_meme = "test_meme_img/pepe_meme.jpg"
    text_meme = "admin pepe"

    with open(img_path_meme, 'rb') as file:
        files = {'img_meme': (img_path_meme, file, 'image/jpeg')}
        params = {'title_meme': text_meme}

        response = requests.post(api_url, files=files, params=params)

        assert response.status_code == 403
