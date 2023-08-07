import pytest

# Предполагаем, что API работает по этому URL
BASE_URL = 'http://api_server:8000/api/v1/menus'

# Пример данных для тестирования
SAMPLE_SUBMENU = {
    'title': 'Тестовое подменю',
    'description': 'Это тестовое подменю.',
}

# Тест на создание меню и добавление подменю


@pytest.mark.asyncio
async def test_create_submenu(api_client, created_menu_id):
    response = await api_client.post(
        f'{BASE_URL}/{created_menu_id}/submenus', json=SAMPLE_SUBMENU
    )
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['title'] == SAMPLE_SUBMENU['title']
    assert data['description'] == SAMPLE_SUBMENU['description']


# Тест на просмотр всех подменю


@pytest.mark.asyncio
async def test_show_all_submenus(api_client, created_menu_id):
    response = await api_client.get(f'{BASE_URL}/{created_menu_id}/submenus')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

    # Создаём подменю и проверяем список ещё раз
    response = await api_client.post(
        f'{BASE_URL}/{created_menu_id}/submenus', json=SAMPLE_SUBMENU
    )
    assert response.status_code == 201
    data = response.json()
    response = await api_client.get(f'{BASE_URL}/{created_menu_id}/submenus')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


# Тест на просмотр конкретного подменю


@pytest.mark.asyncio
async def test_show_submenu(api_client, created_menu_id):
    # создаем новое подменю для тестирования
    response = await api_client.post(
        f'{BASE_URL}/{created_menu_id}/submenus', json=SAMPLE_SUBMENU
    )
    assert response.status_code == 201
    data = response.json()
    submenu_id = data['id']

    # Теперь выполняем запрос для просмотра созданного подменю
    response = await api_client.get(
        f'{BASE_URL}/{created_menu_id}/submenus/{submenu_id}'
    )
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data
    assert data['title'] == SAMPLE_SUBMENU['title']
    assert data['description'] == SAMPLE_SUBMENU['description']


# Тест на обновление подменю


@pytest.mark.asyncio
async def test_update_submenu(api_client, created_menu_id):
    # Сначала создаем новое подменю для тестирования
    response = await api_client.post(
        f'{BASE_URL}/{created_menu_id}/submenus', json=SAMPLE_SUBMENU
    )
    assert response.status_code == 201
    data = response.json()
    submenu_id = data['id']

    # Теперь выполняем запрос для обновления подменю
    updated_submenu_data = {
        'title': 'Обновленное подменю',
        'description': 'Это обновленное подменю.',
    }
    response = await api_client.patch(
        f'{BASE_URL}/{created_menu_id}/submenus/{submenu_id}', json=updated_submenu_data
    )
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert (
        data['message'] == f'Информация для подменю с ID {submenu_id} успешно обновлена'
    )
    assert data['title'] == updated_submenu_data['title']
    assert data['description'] == updated_submenu_data['description']


# Тест на удаление подменю


@pytest.mark.asyncio
async def test_delete_submenu(api_client, created_menu_id):
    # Сначала создаем новое подменю для тестирования
    response = await api_client.post(
        f'{BASE_URL}/{created_menu_id}/submenus', json=SAMPLE_SUBMENU
    )
    assert response.status_code == 201
    data = response.json()
    submenu_id = data['id']

    # Теперь выполняем запрос для удаления подменю
    response = await api_client.delete(
        f'{BASE_URL}/{created_menu_id}/submenus/{submenu_id}'
    )
    assert response.status_code == 200
    data = response.json()
    assert 'status' in data
    assert 'message' in data
    assert data['message'] == 'The submenu has been deleted'

    # Проверяем, что подменю больше нет в базе данных
    response = await api_client.get(
        f'{BASE_URL}/{created_menu_id}/submenus/{submenu_id}'
    )
    assert response.status_code == 404
    data = response.json()
    assert 'detail' in data
    assert data['detail'] == 'submenu not found'


# Тест на удаление меню


@pytest.mark.asyncio
async def test_delete_menu(api_client, created_menu_id):
    # Сначала создаем новое подменю для тестирования
    response = await api_client.post(
        f'{BASE_URL}/{created_menu_id}/submenus', json=SAMPLE_SUBMENU
    )
    assert response.status_code == 201
    data = response.json()
    submenu_id = data['id']

    # Теперь выполняем запрос для удаления меню
    response = await api_client.delete(f'{BASE_URL}/{created_menu_id}')
    assert response.status_code == 200
    data = response.json()
    assert 'status' in data
    assert 'message' in data
    assert data['message'] == 'The menu has been deleted'

    # Проверяем, что подменю больше нет в базе данных
    response = await api_client.get(
        f'{BASE_URL}/{created_menu_id}/submenus/{submenu_id}'
    )
    assert response.status_code == 404
    data = response.json()
    assert 'detail' in data
    assert data['detail'] == 'submenu not found'
