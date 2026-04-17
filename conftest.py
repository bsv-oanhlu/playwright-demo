import os

import pytest

from pages.login_page import LoginPage

URL = "https://playwright-demo.eventos.work/web/portal/529/event/3988/users/login"


@pytest.fixture
def access_to_login_page(page):
    login_page = LoginPage(page)
    login_page.navigate(URL)
    return login_page


@pytest.fixture
def e2e_registered_credentials():
    """ログイン-30〜32: 登録済みアカウント（未設定時は該当テストをスキップ）"""
    email = os.getenv("E2E_REGISTERED_EMAIL")
    password = os.getenv("E2E_REGISTERED_PASSWORD")
    if not email or not password:
        pytest.skip("E2E_REGISTERED_EMAIL と E2E_REGISTERED_PASSWORD を設定してください")
    return {"email": email, "password": password}