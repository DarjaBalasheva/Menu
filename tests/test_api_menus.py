import pytest

# Предполагаем, что API работает по этому URL
BASE_URL = 'http://api_server:8000/api/v1/menus'

# Пример данных для тестирования
SAMPLE_MENU = {
    'title': 'Тестовое меню',
    'description': 'Это тестовое меню.',
}

# Тест на создание меню


@pytest.mark.asyncio
async def test_create_menu(api_client):
    response = await api_client.post(BASE_URL, json=SAMPLE_MENU)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['title'] == SAMPLE_MENU['title']
    assert data['description'] == SAMPLE_MENU['description']


@pytest.mark.asyncio
async def test_show_all_menus(api_client):
    response = await api_client.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


# Тест на просмотр созданного меню


@pytest.mark.asyncio
async def test_get_created_menu(api_client):
    response = await api_client.post(BASE_URL, json=SAMPLE_MENU)
    # assert response.status_code == 201
    data = response.json()
    created_menu_id = data['id']
    response = await api_client.get(f'{BASE_URL}/{created_menu_id}')
    assert response.status_code == 200
    # data = response.json()
    # assert "id" in data
    assert data['title'] == SAMPLE_MENU['title']
    assert data['description'] == SAMPLE_MENU['description']


# Тест на обновление меню


@pytest.mark.asyncio
async def test_update_menu(api_client, created_menu_id):
    updated_data = {
        'title': 'Обновленное меню',
        'description': 'Это обновленное меню.',
    }
    response = await api_client.patch(
        f'{BASE_URL}/{created_menu_id}', json=updated_data
    )
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data
    assert data['title'] == updated_data['title']
    assert data['description'] == updated_data['description']


# Тест на просмотр обновленного меню


@pytest.mark.asyncio
async def test_get_updated_menu(api_client, created_menu_id):
    updated_data = {
        'title': 'Обновленное меню',
        'description': 'Это обновленное меню.',
    }
    # Обновляем данные перед выполнением запроса для просмотра обновленного меню
    await api_client.patch(f'{BASE_URL}/{created_menu_id}', json=updated_data)

    # Теперь делаем запрос для получения обновленных данных
    response = await api_client.get(f'{BASE_URL}/{created_menu_id}')
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data
    assert data['title'] == updated_data['title']
    assert data['description'] == updated_data['description']


# Тест на удаление меню


@pytest.mark.asyncio
async def test_delete_menu(api_client, created_menu_id):
    # Сначала создаем меню для удаления, чтобы убедиться, что оно существует
    response = await api_client.get(f'{BASE_URL}/{created_menu_id}')
    assert response.status_code == 200

    # Теперь удаляем меню
    response = await api_client.delete(f'{BASE_URL}/{created_menu_id}')
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert data['message'] == 'The menu has been deleted'

    # Проверяем, что меню больше нет в базе данных
    response = await api_client.get(f'{BASE_URL}/{created_menu_id}')
    assert response.status_code == 404
    data = response.json()
    assert 'detail' in data
    assert data['detail'] == 'menu not found'
