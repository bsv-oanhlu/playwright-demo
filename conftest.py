import os

import pytest

from pages.login_page import LoginPage

BASE_URL = os.getenv("BASE_URL", "https://playwright-demo.eventos.work")
LOGIN_PATH = os.getenv("LOGIN_PATH", "/web/portal/529/event/3988/users/login")
LOGIN_URL = f"{BASE_URL.rstrip('/')}{LOGIN_PATH}"


@pytest.fixture
def access_to_login_page(page):
    login_page = LoginPage(page)
    login_page.navigate(LOGIN_URL)
    return login_page


@pytest.fixture
def e2e_registered_credentials():
    """ログイン-30〜32: 登録済みアカウント（未設定時は該当テストをスキップ）"""
    email = os.getenv("E2E_REGISTERED_EMAIL")
    password = os.getenv("E2E_REGISTERED_PASSWORD")
    if not email or not password:
        pytest.skip("E2E_REGISTERED_EMAIL と E2E_REGISTERED_PASSWORD を設定してください")
    return {"email": email, "password": password}


@pytest.fixture
def admin_credentials():
    """Optional admin credentials for tests that require login."""
    email = os.getenv("E2E_EMAIL")
    password = os.getenv("E2E_PASSWORD")
    if not email or not password:
        pytest.skip("E2E_EMAIL と E2E_PASSWORD を設定してください")
    return {"email": email, "password": password}