import pytest
from conftest import api_client, created_menu_id, created_submenu

# Предполагаем, что API работает по этому URL
BASE_URL = "http://api_server:8000/api/v1/menus"

# Пример данных для тестирования
SAMPLE_DISHES= {
    "title": "Тестовое блюдо",
    "description": "Это тестовое блюдо.",
}
SAMPLE_SUBMENU = {
    "title": "Тестовое подменю",
    "description": "Это тестовое подменю.",
}

# Тест на создание меню, подменю и добавлении блюда
@pytest.mark.asyncio
async def test_create_dish(api_client, created_menu_id, created_submenu):
    #Создаём подменю
    submenu_id = await created_submenu
    assert submenu_id is not None

    #Создаём блюдо
    response = await api_client.post(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}/dishes", json=SAMPLE_DISHES)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == SAMPLE_DISHES["title"]
    assert data["description"] == SAMPLE_DISHES["description"]

# Тест на просмотр всех блюд
@pytest.mark.asyncio
async def test_show_all_dishes(api_client, created_menu_id, created_submenu):
    # Создаём подменю
    submenu_id = await created_submenu
    assert submenu_id is not None

    # Проверяем блюда, они должны быть пусты
    response = await api_client.get(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

    # Создаём блюдо и проверяем список ещё раз
    response = await api_client.post(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}/dishes", json=SAMPLE_DISHES)
    assert response.status_code == 201
    data = response.json()
    response = await api_client.get(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


# Тест на просмотр конкретного блюда
@pytest.mark.asyncio
async def test_show_dish(api_client, created_menu_id, created_submenu):
    #создаем новое подменю
    submenu_id = await created_submenu
    assert submenu_id is not None

    # Создаём блюдо
    response = await api_client.post(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}/dishes", json=SAMPLE_DISHES)
    assert response.status_code == 201
    data = response.json()
    dishes_id = data["id"]

    # Теперь выполняем запрос для просмотра созданного подменю
    response = await api_client.get(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}/dishes/{dishes_id}")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == SAMPLE_DISHES["title"]
    assert data["description"] == SAMPLE_DISHES["description"]


# Тест на обновление блюда
@pytest.mark.asyncio
async def test_update_dish(api_client, created_menu_id, created_submenu):
    #создаем подменю
    submenu_id = await created_submenu
    assert submenu_id is not None

    # Теперь выполняем запрос для обновления подменю
    updated_submenu_data = {
        "title": "Обновленное подменю",
        "description": "Это обновленное подменю.",
    }
    response = await api_client.patch(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}", json=updated_submenu_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == f"Информация для подменю с ID {submenu_id} успешно обновлена"
    assert data["title"] == updated_submenu_data["title"]
    assert data["description"] == updated_submenu_data["description"]

# Тест на удаление блюда
@pytest.mark.asyncio
async def test_delete_dish(api_client, created_menu_id, created_submenu):
    # создаем подменю
    submenu_id = await created_submenu
    assert submenu_id is not None

    # Создаём блюдо
    response = await api_client.post(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}/dishes", json=SAMPLE_DISHES)
    assert response.status_code == 201
    data = response.json()
    dishes_id = data["id"]

    # Теперь выполняем запрос для удаления блюда
    response = await api_client.delete(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}/dishes/{dishes_id}")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert data["message"] == "The dish has been deleted"

    # Проверяем, что подменю больше нет в базе данных
    response = await api_client.get(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}/dishes/{dishes_id}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "dish not found"

# Тест на удаление подменю
@pytest.mark.asyncio
async def test_delete_menu(api_client, created_menu_id, created_submenu):
    # создаем подменю
    submenu_id = await created_submenu
    assert submenu_id is not None

    # Создаём блюдо
    response = await api_client.post(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}/dishes", json=SAMPLE_DISHES)
    assert response.status_code == 201
    data = response.json()
    dishes_id = data["id"]

    # Теперь выполняем запрос для удаления подменю
    response = await api_client.delete(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    # Проверяем, что блюда больше нет в базе данных
    response = await api_client.get(f"{BASE_URL}/{created_menu_id}/submenus/{submenu_id}/dishes/{dishes_id}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "dish not found"