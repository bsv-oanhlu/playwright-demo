import re

from playwright.sync_api import Locator

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.email_input = "//input[@id='mail_address']"
        self.password_input = "//input[@id='password']"
        self.login_button = "//button[@id='login_button']"

    def input_email(self, email):
        self.fill(self.email_input, email)

    def input_password(self, password):
        self.fill(self.password_input, password)

    def clear_email(self):
        self.page.locator(self.email_input).clear()

    def clear_password(self):
        self.page.locator(self.password_input).clear()

    def click_login(self):
        self.click(self.login_button)

    def click_password_toggle(self) -> None:
        """パスワード表示切替（重なり・actionability で詰まる場合があるため force 可）"""
        toggle = self.password_toggle()
        toggle.scroll_into_view_if_needed()
        toggle.click(timeout=15000, force=True)

    def click_forgot_password(self) -> None:
        """パスワード再設定リンク（同一画面内の重なり対策）"""
        loc = self.forgot_password_link()
        loc.scroll_into_view_if_needed()
        loc.click(timeout=15000, force=True)

    def forgot_password_link(self) -> Locator:
        """リンク／ボタン／テキストのどれでも拾う（実装差を吸収）"""
        page = self.page
        candidates = [
            page.get_by_role("link", name=re.compile("パスワードを忘れた")),
            page.locator("a[href]").filter(has_text=re.compile("パスワードを忘れた")),
            page.get_by_role("button", name=re.compile("パスワードを忘れた")),
            page.get_by_text("パスワードを忘れた方はこちら", exact=False),
            page.locator("a").filter(has_text=re.compile("パスワードを忘れた")),
        ]
        for loc in candidates:
            if loc.count() > 0:
                return loc.first
        return page.get_by_text("パスワードを忘れた", exact=False).first

    def register_button(self) -> Locator:
        return self.page.get_by_role("button", name="新規登録")

    def password_toggle(self) -> Locator:
        """パスワード表示切替（実装により兄弟button／role=button／親ブロック内など）"""
        page = self.page
        selectors = [
            "input#password ~ button",
            "xpath=//input[@id='password']/following-sibling::button[1]",
            "xpath=//input[@id='password']/following-sibling::*[@role='button'][1]",
            "xpath=//input[@id='password']/following::button[not(@id='login_button')][1]",
            "xpath=//input[@id='password']/ancestor::div[1]//button[@type='button' and not(@id='login_button')]",
            "xpath=//input[@id='password']/ancestor::div[1]//*[@role='button' and not(@id='login_button')][1]",
        ]
        for sel in selectors:
            loc = page.locator(sel)
            if loc.count() > 0:
                return loc.first
        return page.locator(
            "xpath=//input[@id='password']/..//button[not(@id='login_button')]"
        ).first

    def blur_active(self):
        self.page.keyboard.press("Tab")

    def login(self, email, password):
        self.input_email(email)
        self.input_password(password)
        self.click(self.login_button)