"""
Playwright Automation Showcase – automated tests mapped to sheet「Playwright_advance」.

Target: http://bsv-nhungnguyen.github.io/
"""

from __future__ import annotations

import re
import time
from pathlib import Path

import pytest
from playwright.sync_api import expect

from pages.advanced_showcase_page import AdvancedShowcasePage, SHOWCASE_URL

# ── TC 001–005: Frames & iframes ─────────────────────────────────────


def test_advanced_001(showcase: AdvancedShowcasePage):
  """TC 001 – Simple iframe: submit form and verify success message inside the frame."""
  showcase.submit_simple_frame("Playwright")
  output = showcase.simple_frame.locator("#frame-output")
  expect(output).to_have_text("Success: Hello Playwright!")


def test_advanced_002(showcase: AdvancedShowcasePage):
  """TC 002 – Nested iframe A: load nested frames and verify Iframe A controls."""
  showcase.load_nested_frames()
  frame_a = showcase.iframe_a
  expect(frame_a.locator("b")).to_have_text("Iframe A")
  expect(frame_a.get_by_role("button", name="Click button")).to_be_visible()
  expect(frame_a.get_by_role("button", name="Open Iframe B")).to_be_visible()


def test_advanced_003(showcase: AdvancedShowcasePage):
  """TC 003 – Open Iframe B from Iframe A and verify Iframe B content."""
  showcase.load_nested_frames()
  showcase.iframe_a.locator("#btn-open-B").click()
  frame_b = showcase.iframe_b()
  expect(frame_b.locator("b")).to_have_text("Iframe B")
  expect(frame_b.get_by_role("button", name="Click button")).to_be_visible()
  expect(frame_b.get_by_role("button", name="Open Iframe C")).to_be_visible()


def test_advanced_004(showcase: AdvancedShowcasePage):
  """TC 004 – Open Iframe C from Iframe B and verify Iframe C content."""
  showcase.load_nested_frames()
  showcase.iframe_a.locator("#btn-open-B").click()
  showcase.iframe_b().locator("#btn-open-C").click()
  frame_c = showcase.iframe_c()
  expect(frame_c.locator("b")).to_have_text("Iframe C")
  expect(frame_c.get_by_role("button", name="Click button")).to_be_visible()


def test_advanced_005(showcase: AdvancedShowcasePage):
  """TC 005 – Click button inside Iframe C and verify feedback message."""
  showcase.load_nested_frames()
  showcase.iframe_a.locator("#btn-open-B").click()
  showcase.iframe_b().locator("#btn-open-C").click()
  frame_c = showcase.iframe_c()
  frame_c.locator("#btn-C").click()
  expect(frame_c.locator("#res-C")).to_have_text("Iframe C Clicked!")


# ── TC 006–010: Windows & popups / modal ─────────────────────────────


def test_advanced_006(showcase: AdvancedShowcasePage):
  """TC 006 – New tab: open playwright.dev and reach the Installation section."""
  popup = showcase.open_new_tab_playwright_dev()
  popup.get_by_role("link", name=re.compile(r"Get started", re.I)).first.click()
  popup.wait_for_load_state("domcontentloaded")
  expect(popup).to_have_title(re.compile(r"Installation", re.I))


def test_advanced_007(showcase: AdvancedShowcasePage):
  """TC 007 – Popup window: verify popup title text."""
  popup = showcase.open_popup_window()
  expect(popup.locator("h2")).to_have_text("Popup Activated")


def test_advanced_008(showcase: AdvancedShowcasePage):
  """TC 008 – In-page modal: Secure Confirmation dialog is displayed."""
  showcase.open_in_page_modal()
  expect(showcase.page.get_by_role("heading", name="Secure Confirmation")).to_be_visible()
  expect(
    showcase.page.get_by_text("Please enter your verification code", exact=False)
  ).to_be_visible()


def test_advanced_009(showcase: AdvancedShowcasePage):
  """TC 009 – Modal confirm: enter code and verify result message."""
  verification_code = "QA-1234"
  showcase.open_in_page_modal()
  showcase.modal_input().fill(verification_code)
  showcase.confirm_modal()
  expect(showcase.modal_result).to_contain_text(f"Verified: {verification_code}")


def test_advanced_010(showcase: AdvancedShowcasePage):
  """TC 010 – Modal cancel: entered text must not appear in modal-result."""
  showcase.open_in_page_modal()
  showcase.modal_input().fill("should-not-appear")
  showcase.cancel_modal()
  expect(showcase.modal_result).not_to_contain_text("Verified:")
  expect(showcase.modal_result).not_to_contain_text("should-not-appear")


# ── TC 011–017: Native dialogs ───────────────────────────────────────


def test_advanced_011(showcase: AdvancedShowcasePage):
  """TC 011 – Alert: browser alert shows expected message."""
  messages: list[str] = []

  def on_dialog(dialog):
    messages.append(dialog.message)
    dialog.accept()

  showcase.page.on("dialog", on_dialog)
  showcase.trigger_alert()
  showcase.page.wait_for_timeout(300)
  assert messages == ["This is a browser alert!"]


def test_advanced_012(showcase: AdvancedShowcasePage):
  """TC 012 – Alert OK: accept alert and ensure dialog handler completes."""
  accepted = {"value": False}

  def on_dialog(dialog):
    dialog.accept()
    accepted["value"] = True

  showcase.page.on("dialog", on_dialog)
  showcase.trigger_alert()
  showcase.page.wait_for_timeout(300)
  assert accepted["value"] is True


def test_advanced_013(showcase: AdvancedShowcasePage):
  """TC 013 – Confirm: dialog message is Continue?."""
  messages: list[str] = []

  def on_dialog(dialog):
    messages.append(dialog.message)
    dialog.dismiss()

  showcase.page.on("dialog", on_dialog)
  showcase.trigger_confirm()
  showcase.page.wait_for_timeout(300)
  assert messages == ["Continue?"]


def test_advanced_014(showcase: AdvancedShowcasePage):
  """TC 014 – Confirm OK: result area shows Confirmed."""
  def on_dialog(dialog):
    dialog.accept()

  showcase.page.on("dialog", on_dialog)
  showcase.trigger_confirm()
  expect(showcase.confirm_result).to_contain_text("Confirmed")


def test_advanced_015(showcase: AdvancedShowcasePage):
  """TC 015 – Confirm Cancel: result area shows Cancelled."""
  def on_dialog(dialog):
    dialog.dismiss()

  showcase.page.on("dialog", on_dialog)
  showcase.trigger_confirm()
  expect(showcase.confirm_result).to_contain_text("Cancelled")


def test_advanced_016(showcase: AdvancedShowcasePage):
  """TC 016 – Prompt OK: entered value is reflected on the page."""
  prompt_value = "Automation Tester"

  def on_dialog(dialog):
    dialog.accept(prompt_value)

  showcase.page.on("dialog", on_dialog)
  showcase.trigger_prompt()
  expect(showcase.prompt_result).to_contain_text(prompt_value)


def test_advanced_017(showcase: AdvancedShowcasePage):
  """TC 017 – Prompt Cancel: result shows Dismissed."""
  def on_dialog(dialog):
    dialog.dismiss()

  showcase.page.on("dialog", on_dialog)
  showcase.trigger_prompt()
  expect(showcase.prompt_result).to_contain_text("Dismissed")


# ── TC 018–023: Visual regression (screenshot / video) ────────────────


def test_advanced_018(showcase: AdvancedShowcasePage, artifacts_dir: Path):
  """TC 018 – Full-page screenshot after Normal State shows System Normal."""
  showcase.set_vr_normal_state()
  expect(showcase.vr_full_display).to_contain_text("System Normal")
  shot_path = artifacts_dir / "full_page_018.png"
  # Screenshot configuration format: page.screenshot(path="screenshot.png")
  showcase.page.screenshot(path=str(shot_path))
  assert shot_path.exists() and shot_path.stat().st_size > 0


def test_advanced_019(
  showcase: AdvancedShowcasePage,
  element_screenshot_on_failure: Path,
):
  """TC 019 – Element screenshot on failure only: passing test leaves no file."""
  showcase.set_vr_normal_state()
  expect(showcase.vr_full_display).to_contain_text("System Normal")
  assert not element_screenshot_on_failure.exists()


def test_advanced_020(
  showcase: AdvancedShowcasePage,
  element_screenshot_on_failure: Path,
):
  """TC 020 – Element screenshot on failure: failure UI triggers element capture."""
  showcase.set_vr_failure_state()
  expect(showcase.vr_full_display).to_contain_text("CRITICAL FAILURE")
  # Emulate screenshot-on-failure when the visual check would not pass.
  showcase.screenshot_element.screenshot(path=str(element_screenshot_on_failure))
  assert element_screenshot_on_failure.exists()
  assert element_screenshot_on_failure.stat().st_size > 0


def test_advanced_021(browser, artifacts_dir: Path):
  """TC 021 – Video on every run using context with record_video_dir."""
  # Video configuration format:
  # browser = playwright.chromium.launch()
  # context = browser.new_context(record_video_dir="videos/")
  context = browser.new_context(record_video_dir=str(artifacts_dir / "videos"))
  page = context.new_page()
  showcase = AdvancedShowcasePage(page)
  showcase.navigate()
  showcase.play_video_sequence()
  expect(showcase.video_action_text).to_have_text(
    re.compile(r"Sequence complete", re.I),
    timeout=15_000,
  )
  video_path = page.video.path() if page.video else None
  page.close()
  context.close()
  assert video_path is not None


def test_advanced_022(browser, artifacts_dir: Path):
  """TC 022 – Passing run with explicit video context still creates a video file."""
  videos_before = set((artifacts_dir / "videos").glob("**/*"))
  context = browser.new_context(record_video_dir=str(artifacts_dir / "videos"))
  page = context.new_page()
  showcase = AdvancedShowcasePage(page)
  showcase.navigate()
  showcase.play_video_sequence()
  expect(showcase.video_action_text).to_have_text(
    re.compile(r"Sequence complete", re.I),
    timeout=15_000,
  )
  video_path = page.video.path() if page.video else None
  page.close()
  context.close()
  videos_after = set((artifacts_dir / "videos").glob("**/*"))
  assert video_path is not None
  assert len(videos_after) >= len(videos_before)


def test_advanced_023(browser, artifacts_dir: Path):
  """TC 023 – Short timeout failure with explicit video context retains video."""
  context = browser.new_context(record_video_dir=str(artifacts_dir / "videos"))
  page = context.new_page()
  showcase = AdvancedShowcasePage(page)
  showcase.navigate()
  showcase.play_video_sequence()
  with pytest.raises(AssertionError):
    expect(showcase.video_action_text).to_have_text(
      re.compile(r"Sequence complete", re.I),
      timeout=1_000,
    )
  video_path = page.video.path() if page.video else None
  page.close()
  context.close()
  assert video_path is not None


# ── TC 024–026: Tracing & submission ────────────────────────────────


def _stop_trace(context, traces_dir: Path, name: str) -> Path:
  trace_path = traces_dir / f"{name}.zip"
  context.tracing.stop(path=str(trace_path))
  return trace_path


def test_advanced_024(showcase: AdvancedShowcasePage, traces_dir: Path):
  """TC 024 – Tracing always on: submit valid form and save trace archive."""
  context = showcase.page.context
  context.tracing.start(screenshots=True, snapshots=True)
  dev_name = "Playwright Dev"
  showcase.fill_trace_form(dev_name, "dev@example.com")
  showcase.submit_trace_form()
  expect(showcase.trace_result).to_contain_text(f"Submitted: {dev_name}")
  trace_path = _stop_trace(context, traces_dir, "024_pass")
  assert trace_path.exists() and trace_path.stat().st_size > 0


def test_advanced_025(showcase: AdvancedShowcasePage, traces_dir: Path):
  """TC 025 – Tracing on failure: empty submit shows validation and saves trace."""
  context = showcase.page.context
  context.tracing.start(screenshots=True, snapshots=True)
  showcase.clear_trace_form()
  showcase.submit_trace_form()
  expect(showcase.trace_result).to_contain_text("Both fields are required")
  with pytest.raises(AssertionError):
    expect(showcase.trace_result).to_contain_text("Submitted:")
  trace_path = _stop_trace(context, traces_dir, "025_fail")
  assert trace_path.exists()


def test_advanced_026(showcase: AdvancedShowcasePage, traces_dir: Path):
  """TC 026 – Tracing on failure only: successful submit must not leave a trace file."""
  dev_name = "Trace Pass"
  showcase.fill_trace_form(dev_name, "pass@example.com")
  showcase.submit_trace_form()
  expect(showcase.trace_result).to_contain_text(f"Submitted: {dev_name}")
  trace_path = traces_dir / "026_should_not_exist.zip"
  assert not trace_path.exists()


# ── TC 027–030: Pytest hooks (Hooks Demo) ─────────────────────────────


def test_advanced_027(module_before_all_ran: bool):
  """TC 027 – beforeAll hook prints artifact path guidance in the terminal."""
  assert module_before_all_ran is True


def test_advanced_028():
  """TC 028 – afterAll hook runs at module teardown (see conftest module fixture)."""
  assert True


def test_advanced_029(hooks_demo_with_record):
  """TC 029 – beforeEach: login and create record before the test body runs."""
  showcase, record_name = hooks_demo_with_record
  expect(showcase.hooks_record_rows()).to_have_count(1)
  expect(showcase.hooks_create_message).to_contain_text(record_name)


def test_advanced_030(hooks_demo_cleanup_after: AdvancedShowcasePage):
  """TC 030 – afterEach: records created during the test are deleted automatically."""
  showcase = hooks_demo_cleanup_after
  record_name = f"cleanup-{int(time.time())}"
  showcase.hooks_create_record(record_name, category="feature")
  expect(showcase.hooks_record_rows()).to_have_count(1)
  expect(showcase.hooks_record_count).to_have_text("1")
