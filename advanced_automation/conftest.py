"""Fixtures and hooks for Playwright Automation Showcase tests (TC 27–30)."""

from __future__ import annotations

from pathlib import Path

import pytest

from pages.advanced_showcase_page import HOOKS_PASSWORD, HOOKS_USERNAME, AdvancedShowcasePage

ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
TRACES_DIR = ARTIFACTS_DIR / "traces"

for _dir in (ARTIFACTS_DIR, SCREENSHOTS_DIR, VIDEOS_DIR, TRACES_DIR):
  _dir.mkdir(parents=True, exist_ok=True)

_module_before_all_ran = False


@pytest.fixture(scope="module", autouse=True)
def advanced_showcase_module_hooks():
  """TC 27–28: module-level beforeAll / afterAll console guidance."""
  global _module_before_all_ran
  print("\n[beforeAll] Setup test environment")
  print(f"Artifacts will be saved to: {ARTIFACTS_DIR.resolve()}")
  _module_before_all_ran = True
  yield
  print("\n[afterAll] End test session – cleanup environment")


@pytest.fixture
def module_before_all_ran():
  return _module_before_all_ran


@pytest.fixture
def showcase(page) -> AdvancedShowcasePage:
  showcase_page = AdvancedShowcasePage(page)
  showcase_page.navigate()
  return showcase_page


@pytest.fixture
def artifacts_dir():
  return ARTIFACTS_DIR


@pytest.fixture
def screenshots_dir():
  return SCREENSHOTS_DIR


@pytest.fixture
def traces_dir():
  return TRACES_DIR


@pytest.fixture
def element_screenshot_on_failure(page, request, screenshots_dir):
  """Capture #screenshot-element only when the test fails (TC 19–20)."""
  target = page.locator("#screenshot-element")
  shot_path = screenshots_dir / f"{request.node.name}.png"

  yield shot_path

  rep = getattr(request.node, "rep_call", None)
  if rep is not None and rep.failed:
    target.screenshot(path=str(shot_path))


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
  outcome = yield
  rep = outcome.get_result()
  setattr(item, f"rep_{call.when}", rep)


@pytest.fixture
def hooks_demo_logged_in(showcase: AdvancedShowcasePage):
  """TC 29–30: beforeEach – login once before hook-demo tests."""
  showcase.hooks_login(HOOKS_USERNAME, HOOKS_PASSWORD)
  return showcase


@pytest.fixture
def hooks_demo_with_record(hooks_demo_logged_in: AdvancedShowcasePage, request):
  """TC 29: beforeEach – create a record before the test runs."""
  record_name = f"hook-record-{request.node.name}"
  hooks_demo_logged_in.hooks_create_record(record_name, category="task")
  yield hooks_demo_logged_in, record_name


@pytest.fixture
def hooks_demo_cleanup_after(hooks_demo_logged_in: AdvancedShowcasePage):
  """TC 30: afterEach – remove any records left on the table."""
  yield hooks_demo_logged_in
  while hooks_demo_logged_in.hooks_record_rows().count() > 0:
    hooks_demo_logged_in.hooks_delete_first_record()


