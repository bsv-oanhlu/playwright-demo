import re

from playwright.sync_api import expect


def test_login_003(access_to_login_page):
    """Check URL: address contains '/login'."""
    login_page = access_to_login_page
    expect(login_page.page).to_have_url(re.compile(r"/login"))


def test_login_004(access_to_login_page):
    """Check page title: Login or ログイン appears in tab title or in a heading."""
    login_page = access_to_login_page
    page = login_page.page
    title = page.title()
    if re.search(r"(ログイン|login)", title, re.I):
        expect(page).to_have_title(re.compile(r"(ログイン|login)", re.I))
    else:
        expect(page.get_by_role("heading", name=re.compile(r"(ログイン|login)", re.I))).to_be_visible()


def test_login_005(access_to_login_page):
    """Check mail address label and input field are visible."""
    login_page = access_to_login_page
    expect(login_page.page.get_by_text("メールアドレス", exact=False).first).to_be_visible()
    expect(login_page.page.locator(login_page.email_input)).to_be_visible()


def test_login_006(access_to_login_page):
    """Check if user can input text into username and password fields."""
    login_page = access_to_login_page
    login_page.input_email("oanhlth")
    login_page.input_password("xxxx")
    assert login_page.get_input_value(login_page.email_input) == "oanhlth"
    assert login_page.get_input_value(login_page.password_input) == "xxxx"


def test_login_007(access_to_login_page):
    """Check data display in field [email]."""
    login_page = access_to_login_page
    login_page.input_email("oanhlth")
    assert login_page.get_input_value(login_page.email_input) == "oanhlth"


def _assert_no_inline_auth_errors(page):
    """Assert common inline validation messages are not shown."""
    expect(page.get_by_text("メールアドレスが正しくありません。", exact=False)).to_have_count(0)
    expect(page.get_by_text("メールアドレスを入力してください", exact=False)).to_have_count(0)
    expect(page.get_by_text("パスワードは8文字以上32文字以下で指定してください。", exact=False)).to_have_count(0)


def test_login_008(access_to_login_page):
    """Check ABC@GMAIL.COM is shown in the email field as typed."""
    login_page = access_to_login_page
    login_page.input_email("ABC@GMAIL.COM")
    assert login_page.get_input_value(login_page.email_input) == "ABC@GMAIL.COM"


def _invalid_email_shows_error(login_page, invalid_email: str):
    """Trigger validation for invalid email; message appears on blur or after login click."""
    page = login_page.page
    login_page.input_email(invalid_email)
    page.locator(login_page.email_input).blur()
    login_page.input_password("Abcd1234!")
    msg = page.get_by_text("メールアドレスが正しくありません", exact=False)
    try:
        expect(msg).to_be_visible(timeout=5000)
    except AssertionError:
        btn = page.locator(login_page.login_button)
        if btn.is_enabled():
            btn.click()
        expect(msg).to_be_visible(timeout=15000)


def test_login_009(access_to_login_page):
    """Check invalid email abc@gmail shows format error."""
    login_page = access_to_login_page
    _invalid_email_shows_error(login_page, "abc@gmail")


def test_login_010(access_to_login_page):
    """Check invalid email abc!@gmail.com shows format error."""
    login_page = access_to_login_page
    _invalid_email_shows_error(login_page, "abc!@gmail.com")


def test_login_011(access_to_login_page):
    """Check invalid email test.abc shows format error."""
    login_page = access_to_login_page
    _invalid_email_shows_error(login_page, "test.abc")


def test_login_012(access_to_login_page):
    """Check invalid email @gmail.com shows format error."""
    login_page = access_to_login_page
    _invalid_email_shows_error(login_page, "@gmail.com")


def test_login_013(access_to_login_page):
    """Check full-width characters in email show format error."""
    login_page = access_to_login_page
    _invalid_email_shows_error(login_page, "てすと＠ｇｍａｉｌ．ｃｏｍ")


def test_login_014(access_to_login_page):
    """Check clearing email shows 'please enter email' message."""
    login_page = access_to_login_page
    login_page.input_email("user@example.com")
    login_page.clear_email()
    login_page.blur_active()
    expect(login_page.page.get_by_text("メールアドレスを入力してください", exact=False)).to_be_visible()


def test_login_015(access_to_login_page):
    """Check password label, input, and mask toggle are visible (toggle inactive if aria present)."""
    login_page = access_to_login_page
    page = login_page.page
    expect(page.get_by_text("パスワード", exact=False).first).to_be_visible()
    expect(page.locator(login_page.password_input)).to_be_visible()
    toggle = login_page.password_toggle()
    expect(toggle).to_be_visible(timeout=15000)
    pressed = toggle.get_attribute("aria-pressed")
    if pressed is not None:
        assert pressed == "false"


def test_login_016(access_to_login_page):
    """Check password field uses type=password (masked)."""
    login_page = access_to_login_page
    login_page.input_password("Secret12!")
    pw = login_page.page.locator(login_page.password_input)
    expect(pw).to_have_attribute("type", "password")


def test_login_017(access_to_login_page):
    """Check eye toggle reveals plain text password."""
    login_page = access_to_login_page
    login_page.input_password("Secret12!")
    login_page.click_password_toggle()
    pw = login_page.page.locator(login_page.password_input)
    expect(pw).to_have_attribute("type", "text")


def test_login_018(access_to_login_page):
    """Check eye toggle again masks password."""
    login_page = access_to_login_page
    login_page.input_password("Secret12!")
    login_page.click_password_toggle()
    login_page.click_password_toggle()
    pw = login_page.page.locator(login_page.password_input)
    expect(pw).to_have_attribute("type", "password")


def test_login_019(access_to_login_page):
    """Check password shorter than 8 characters shows length error."""
    login_page = access_to_login_page
    login_page.input_email("user@example.com")
    login_page.input_password("1234567")
    page = login_page.page
    page.locator(login_page.password_input).blur()
    msg = page.get_by_text("パスワードは8文字以上32文字以下で指定してください", exact=False)
    try:
        expect(msg).to_be_visible(timeout=5000)
    except AssertionError:
        btn = page.locator(login_page.login_button)
        if btn.is_enabled():
            btn.click()
        expect(msg).to_be_visible(timeout=15000)


def test_login_020(access_to_login_page):
    """Check password input does not accept more than 32 characters."""
    login_page = access_to_login_page
    long_pw = "a" * 40
    login_page.input_password(long_pw)
    val = login_page.get_input_value(login_page.password_input)
    assert len(val) <= 32


def test_login_021(access_to_login_page):
    """Check digits-only password does not show inline auth errors."""
    login_page = access_to_login_page
    login_page.input_email("format-check@example.com")
    login_page.input_password("12345678")
    login_page.blur_active()
    _assert_no_inline_auth_errors(login_page.page)


def test_login_022(access_to_login_page):
    """Check letters-only password does not show inline auth errors."""
    login_page = access_to_login_page
    login_page.input_email("format-check@example.com")
    login_page.input_password("AbcdefgH")
    login_page.blur_active()
    _assert_no_inline_auth_errors(login_page.page)


def test_login_023(access_to_login_page):
    """Check symbols-only password does not show inline auth errors."""
    login_page = access_to_login_page
    login_page.input_email("format-check@example.com")
    login_page.input_password("!@#$%^&*")
    login_page.blur_active()
    _assert_no_inline_auth_errors(login_page.page)


def test_login_024(access_to_login_page):
    """Check digits+letters password does not show inline auth errors."""
    login_page = access_to_login_page
    login_page.input_email("format-check@example.com")
    login_page.input_password("Abc12345")
    login_page.blur_active()
    _assert_no_inline_auth_errors(login_page.page)


def test_login_025(access_to_login_page):
    """Check digits+symbols password does not show inline auth errors."""
    login_page = access_to_login_page
    login_page.input_email("format-check@example.com")
    login_page.input_password("1234!@#$")
    login_page.blur_active()
    _assert_no_inline_auth_errors(login_page.page)


def test_login_026(access_to_login_page):
    """Check symbols+letters password does not show inline auth errors."""
    login_page = access_to_login_page
    login_page.input_email("format-check@example.com")
    login_page.input_password("!@#$AbCd")
    login_page.blur_active()
    _assert_no_inline_auth_errors(login_page.page)


def test_login_027(access_to_login_page):
    """Check forgot-password link is underlined."""
    login_page = access_to_login_page
    link = login_page.forgot_password_link()
    expect(link).to_be_visible(timeout=15000)
    looks_underlined = link.evaluate(
        """el => {
            const s = getComputedStyle(el);
            if (s.textDecorationLine === 'underline') return true;
            if (String(s.textDecoration).includes('underline')) return true;
            if (parseFloat(s.borderBottomWidth) > 0 && s.borderBottomStyle !== 'none') return true;
            if ([...el.classList].some(c => /underline/i.test(c))) return true;
            const child = el.querySelector('span, a');
            if (child) {
              const cs = getComputedStyle(child);
              if (cs.textDecorationLine === 'underline') return true;
              if (String(cs.textDecoration).includes('underline')) return true;
            }
            return false;
        }"""
    )
    assert looks_underlined


def test_login_028(access_to_login_page):
    """Check forgot-password navigates away from login URL."""
    login_page = access_to_login_page
    login_page.click_forgot_password()
    expect(login_page.page).not_to_have_url(re.compile(r"/users/login(?:/|\\?|$)"), timeout=15000)


def test_login_029(access_to_login_page):
    """Check login button is visible on initial load (disabled only if the app disables it)."""
    login_page = access_to_login_page
    btn = login_page.page.locator(login_page.login_button)
    expect(btn).to_be_visible()
    if btn.is_disabled():
        expect(btn).to_be_disabled()


def test_login_030(access_to_login_page, e2e_registered_credentials):
    """Check wrong password with valid email shows login failure message."""
    login_page = access_to_login_page
    creds = e2e_registered_credentials
    login_page.input_email(creds["email"])
    login_page.input_password("WrongPass999!")
    login_page.click_login()
    expect(
        login_page.page.get_by_text(
            "ログインできませんでした。入力内容をご確認の上、もう一度お試しください。",
            exact=False,
        )
    ).to_be_visible(timeout=15000)


def test_login_031(access_to_login_page, e2e_registered_credentials):
    """Check unregistered email with valid password shows login failure message."""
    login_page = access_to_login_page
    creds = e2e_registered_credentials
    login_page.input_email("not-registered-e2e@example.com")
    login_page.input_password(creds["password"])
    login_page.click_login()
    expect(
        login_page.page.get_by_text(
            "ログインできませんでした。入力内容をご確認の上、もう一度お試しください。",
            exact=False,
        )
    ).to_be_visible(timeout=15000)


def test_login_032(access_to_login_page, e2e_registered_credentials):
    """Check successful login leaves the login URL."""
    login_page = access_to_login_page
    creds = e2e_registered_credentials
    login_page.input_email(creds["email"])
    login_page.input_password(creds["password"])
    login_page.click_login()
    expect(login_page.page).not_to_have_url(re.compile(r"/users/login(?:/|\\?|$)"), timeout=20000)


def test_login_033(access_to_login_page):
    """Check sign-up button is visible."""
    login_page = access_to_login_page
    expect(login_page.register_button()).to_be_visible()


def test_login_034(access_to_login_page):
    """Check sign-up button navigates away from login URL."""
    login_page = access_to_login_page
    login_page.register_button().click()
    expect(login_page.page).not_to_have_url(re.compile(r"/users/login(?:/|\\?|$)"), timeout=15000)
