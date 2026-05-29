import os
import re

from playwright.sync_api import FrameLocator, Page, expect

SHOWCASE_URL = os.getenv(
    "SHOWCASE_URL", "http://bsv-nhungnguyen.github.io/"
).rstrip("/") + "/"

HOOKS_USERNAME = os.getenv("HOOKS_USERNAME", "admin")
HOOKS_PASSWORD = os.getenv("HOOKS_PASSWORD", "password123")


class AdvancedShowcasePage:
  """Page object for the Playwright Automation Showcase demo site."""

  def __init__(self, page: Page) -> None:
    self.page = page

  def navigate(self) -> None:
    self.page.goto(SHOWCASE_URL, wait_until="domcontentloaded")

  # ── Frames & iframes ──────────────────────────────────────────────

  @property
  def simple_frame(self) -> FrameLocator:
    return self.page.frame_locator("#demo-iframe")

  @property
  def iframe_a(self) -> FrameLocator:
    return self.page.frame_locator("#iframe-A")

  def load_nested_frames(self) -> None:
    self.page.locator("#btn-open-nested").click()
    expect(self.page.locator("#iframe-A")).to_be_visible()

  def iframe_b(self) -> FrameLocator:
    return self.iframe_a.frame_locator("#iframe-B")

  def iframe_c(self) -> FrameLocator:
    return self.iframe_b().frame_locator("#iframe-C")

  def submit_simple_frame(self, name: str) -> None:
    frame = self.simple_frame
    frame.locator("#iframe-name").fill(name)
    frame.locator("#iframe-submit-btn").click()

  # ── Windows & popups ──────────────────────────────────────────────

  def open_new_tab_playwright_dev(self) -> Page:
    with self.page.expect_popup() as popup_info:
      self.page.locator("#btn-new-tab").click()
    popup = popup_info.value
    popup.wait_for_load_state("domcontentloaded")
    return popup

  def open_popup_window(self) -> Page:
    with self.page.expect_popup() as popup_info:
      self.page.locator("#btn-popup").click()
    popup = popup_info.value
    popup.wait_for_load_state("domcontentloaded")
    return popup

  def open_in_page_modal(self) -> None:
    self.page.locator("#btn-internal-modal").click()
    expect(self.page.locator("#modal-overlay")).to_have_class(re.compile(r"\bactive\b"))

  def modal_input(self):
    return self.page.locator("#modal-input")

  def confirm_modal(self) -> None:
    self.page.locator("#modal-confirm-btn").click()

  def cancel_modal(self) -> None:
    self.page.locator("#modal-cancel-btn").click()

  @property
  def modal_result(self):
    return self.page.locator("#modal-result")

  # ── Native dialogs ────────────────────────────────────────────────

  def trigger_alert(self) -> None:
    self.page.locator("#btn-alert").click()

  def trigger_confirm(self) -> None:
    self.page.locator("#btn-confirm").click()

  def trigger_prompt(self) -> None:
    self.page.locator("#btn-prompt").click()

  @property
  def confirm_result(self):
    return self.page.locator("#confirm-result")

  @property
  def prompt_result(self):
    return self.page.locator("#prompt-result")

  # ── Tracing & submission ──────────────────────────────────────────

  def fill_trace_form(self, name: str, email: str) -> None:
    self.page.locator("#trace-name").fill(name)
    self.page.locator("#trace-email").fill(email)

  def clear_trace_form(self) -> None:
    self.page.locator("#trace-name").fill("")
    self.page.locator("#trace-email").fill("")

  def submit_trace_form(self) -> None:
    self.page.locator("#btn-trace-submit").click()

  @property
  def trace_result(self):
    return self.page.locator("#trace-result")

  # ── Visual regression UI ──────────────────────────────────────────

  @property
  def vr_full_display(self):
    return self.page.locator("#vr-full-display")

  def set_vr_normal_state(self) -> None:
    self.page.locator("#btn-reset-state").click()

  def set_vr_failure_state(self) -> None:
    self.page.locator("#btn-trigger-failure").click()

  @property
  def screenshot_element(self):
    return self.page.locator("#screenshot-element")

  def play_video_sequence(self) -> None:
    self.page.locator("#btn-play-seq").click()

  @property
  def video_action_text(self):
    return self.page.locator("#vr-action-txt")

  # ── Hooks demo ────────────────────────────────────────────────────

  def hooks_login(self, username: str = HOOKS_USERNAME, password: str = HOOKS_PASSWORD) -> None:
    self.page.locator("#hk-username").fill(username)
    self.page.locator("#hk-password").fill(password)
    self.page.locator("#hk-btn-login").click()
    expect(self.page.locator("#hk-main-section")).to_be_visible()

  def hooks_logout(self) -> None:
    self.page.locator("#hk-btn-logout").click()

  def hooks_create_record(self, name: str, category: str = "bug") -> None:
    self.page.locator("#hk-record-name").fill(name)
    self.page.locator("#hk-record-category").select_option(category)
    self.page.locator("#hk-btn-create").click()

  def hooks_record_rows(self):
    return self.page.locator("#hk-record-list tr[data-record-id]")

  def hooks_delete_first_record(self) -> None:
    self.page.locator("#hk-record-list button").filter(has_text="Delete").first.click()

  @property
  def hooks_create_message(self):
    return self.page.locator("#hk-create-msg")

  @property
  def hooks_record_count(self):
    return self.page.locator("#hk-rec-count")
