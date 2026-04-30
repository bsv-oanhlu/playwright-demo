import os
import re

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect

# =============================
# CONFIG
# =============================
BASE_URL = os.getenv("BASE_URL", "https://admin.odakyu.bravesoft.vn")
LOGIN_PATH = os.getenv("LOGIN_PATH", "/login")
REGISTER_PATH = os.getenv("REGISTER_PATH", "/account-management")
EMAIL = os.getenv("E2E_EMAIL", "kimtran@bravesoft.com.vn")
PASSWORD = os.getenv("E2E_PASSWORD", "brave0404")

LOGIN_URL = f"{BASE_URL.rstrip('/')}{LOGIN_PATH}"
REGISTER_URL = f"{BASE_URL.rstrip('/')}{REGISTER_PATH}"


def _login_then_open_register_page(page):
    page.goto(LOGIN_URL)
    email_candidates = [
        page.get_by_role("textbox", name=re.compile(r"メールアドレス|mail|email", re.I)),
        page.locator("#mail_address"),
        page.locator("input[name='mail_address']"),
        page.locator("input[type='email']"),
    ]
    password_candidates = [
        page.get_by_label(re.compile(r"パスワード|password", re.I)),
        page.locator("#password"),
        page.locator("input[name='password']"),
        page.locator("input[type='password']"),
    ]
    login_button_candidates = [
        page.get_by_role("button", name=re.compile(r"ログイン|login|サインイン", re.I)),
        page.locator("#login_button"),
        page.locator("button[type='submit']"),
        page.locator("input[type='submit']"),
    ]

    email_box = next((loc.first for loc in email_candidates if loc.count() > 0), None)
    password_box = next((loc.first for loc in password_candidates if loc.count() > 0), None)
    login_button = next((loc.first for loc in login_button_candidates if loc.count() > 0), None)

    if email_box is None or password_box is None or login_button is None:
        raise AssertionError("Cannot find login form elements on login page.")

    expect(email_box).to_be_visible(timeout=15000)
    expect(password_box).to_be_visible(timeout=15000)
    email_box.fill(EMAIL)
    password_box.fill(PASSWORD)
    login_button.click()

    # If the app keeps us on /login after click, credentials/permissions are likely invalid.
    expect(page).not_to_have_url(re.compile(r"/login(?:/|\\?|$)"), timeout=15000)
    page.goto(REGISTER_URL)
    expect(page).to_have_url(re.compile(r"/account-management"))


def _open_register_page(page):
    try:
        _login_then_open_register_page(page)
    except PlaywrightTimeoutError as exc:
        raise AssertionError(
            "Login failed or timed out. Verify BASE_URL/LOGIN_PATH and EMAIL/PASSWORD."
        ) from exc


def test_register_001(page):
    """新規アカウント追加-1: Check page title includes 新規アカウント追加."""
    _open_register_page(page)
    expect(page.get_by_role("heading", name=re.compile(r"新規アカウント追加"))).to_be_visible()


def test_register_002(page):
    """新規アカウント追加-2: Check URL contains /account-management."""
    _open_register_page(page)
    expect(page).to_have_url(re.compile(r"/account-management"))


def test_register_003(page):
    """新規アカウント追加-3: Check account name label is visible."""
    _open_register_page(page)
    expect(page.get_by_role("textbox", name=re.compile(r"アカウント名"))).to_be_visible()


def test_register_004(page):
    """新規アカウント追加-4: Check account name textbox accepts input."""
    _open_register_page(page)
    account_name = page.get_by_role("textbox", name=re.compile(r"アカウント名"))
    account_name.fill("test_account_name")
    expect(account_name).to_have_value("test_account_name")


def test_register_005(page):
    """新規アカウント追加-5: Check email label/input is visible."""
    _open_register_page(page)
    expect(page.get_by_role("textbox", name=re.compile(r"メールアドレス"))).to_be_visible()


def test_register_006(page):
    """新規アカウント追加-6: Check valid email can be entered."""
    _open_register_page(page)
    email = page.get_by_role("textbox", name=re.compile(r"メールアドレス"))
    email.fill("trucly@bravesoft-vn.com.vn")
    expect(email).to_have_value("trucly@bravesoft-vn.com.vn")


def test_register_007(page):
    """新規アカウント追加-7: Check password label/input is visible."""
    _open_register_page(page)
    expect(page.get_by_role("textbox", name=re.compile(r"パスワード"))).to_be_visible()


def test_register_008(page):
    """新規アカウント追加-8: Check password placeholder is **********."""
    _open_register_page(page)
    password = page.get_by_role("textbox", name=re.compile(r"パスワード"))
    expect(password).to_have_attribute("placeholder", "**********")


def test_register_009(page):
    """新規アカウント追加-9: Check password accepts input and stays masked."""
    _open_register_page(page)
    password = page.get_by_role("textbox", name=re.compile(r"パスワード"))
    password.fill("Secret1234")
    expect(password).to_have_value("Secret1234")
    expect(password).to_have_attribute("type", "password")


def test_register_010(page):
    """新規アカウント追加-10: Check role combobox is visible and empty by default."""
    _open_register_page(page)
    role_box = page.get_by_role("combobox", name=re.compile(r"権限"))
    expect(role_box).to_be_visible()
    expect(role_box).to_have_value("")


def test_register_011(page):
    """新規アカウント追加-11: Check selecting マスター管理者 in role combobox."""
    _open_register_page(page)
    role_box = page.get_by_role("combobox", name=re.compile(r"権限"))
    role_box.select_option(label="マスター管理者")
    expect(role_box).to_have_value(re.compile(r".+"))
    expect(page.get_by_role("option", name="マスター管理者")).to_be_visible()


def test_register_012(page):
    """新規アカウント追加-12: Check selecting テナント管理者 in role combobox."""
    _open_register_page(page)
    role_box = page.get_by_role("combobox", name=re.compile(r"権限"))
    role_box.select_option(label="テナント管理者")
    expect(role_box).to_have_value(re.compile(r".+"))
    expect(page.get_by_role("option", name="テナント管理者")).to_be_visible()


def test_register_013(page):
    """新規アカウント追加-13: Check role selection is single choice only."""
    _open_register_page(page)
    role_box = page.get_by_role("combobox", name=re.compile(r"権限"))
    role_box.select_option(label="マスター管理者")
    first_value = role_box.input_value()
    role_box.select_option(label="テナント管理者")
    second_value = role_box.input_value()
    assert first_value != second_value


def test_register_014(page):
    """新規アカウント追加-14: Check 有/無 permission radio buttons are visible."""
    _open_register_page(page)
    expect(page.get_by_role("radio", name="有")).to_be_visible()
    expect(page.get_by_role("radio", name="無")).to_be_visible()


def test_register_015(page):
    """新規アカウント追加-15: Check selecting 有 is reflected."""
    _open_register_page(page)
    yes_radio = page.get_by_role("radio", name="有")
    yes_radio.check()
    expect(yes_radio).to_be_checked()


def test_register_016(page):
    """新規アカウント追加-16: Check selecting 無 is reflected."""
    _open_register_page(page)
    no_radio = page.get_by_role("radio", name="無")
    no_radio.check()
    expect(no_radio).to_be_checked()


def test_register_017(page):
    """新規アカウント追加-17: Check 有 and 無 cannot be selected at the same time."""
    _open_register_page(page)
    yes_radio = page.get_by_role("radio", name="有")
    no_radio = page.get_by_role("radio", name="無")
    yes_radio.check()
    no_radio.check()
    expect(yes_radio).not_to_be_checked()
    expect(no_radio).to_be_checked()
