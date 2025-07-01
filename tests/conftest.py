import pytest
import time
import uuid
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from utils.logger import log_result

RUN_ID = None
ENVIRONMENT = None
TRIGGERED_BY = "manual"

def is_running_in_docker():
    return os.getenv("IS_DOCKER", "false").lower() == "true"

def create_chrome_driver():
    options = webdriver.ChromeOptions()

    if is_running_in_docker():
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-application-cache")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-data-dir=/tmp/chrome-user-data")

    else:
        options.add_argument("--start-maximized")

    return webdriver.Chrome(options=options)

def create_firefox_driver():
    options = Options()

    if is_running_in_docker():
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    return webdriver.Firefox(options=options)

def pytest_addoption(parser):
    default_browser = os.getenv("BROWSER", "chrome")
    parser.addoption(
        "--browser", action="store", default=default_browser,
        help="Browser to run tests against (chrome or firefox)"
    )

def pytest_configure(config):
    global RUN_ID, ENVIRONMENT
    RUN_ID = str(uuid.uuid4())
    ENVIRONMENT = config.getoption("--browser")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item):
    item.start_time = time.time()
    yield

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call":
        duration = round(time.time() - item.start_time, 3)
        test_name = item.name

        if result.passed:
            status = "PASSED"
            error_message = None
        elif result.failed and result.longrepr:
            status = "FAILED"
            error_message = str(result.longreprtext)[:1000]
        else:
            status = "ERROR"
            error_message = None

        print(f"[HOOK] Logging: {test_name} → {status} in {duration}s")

        log_result(
            test_name=test_name,
            status=status,
            duration=duration,
            run_id=RUN_ID,
            error_message=error_message,
            environment=ENVIRONMENT,
            triggered_by=TRIGGERED_BY,
        )

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")

    try:
        if browser == "chrome":
            driver = create_chrome_driver()

        elif browser == "firefox":
            driver = create_firefox_driver()

        else:
            raise ValueError(f"Unsupported browser: {browser}")\

    except WebDriverException as e:
        pytest.exit(f"\nBrowser '{browser}' could not be started. Reason: {e}", returncode=1)

    try:
        start_time = time.time()
        driver.get("about:blank")
        while True:
            if "about:blank" in driver.current_url:
                break
            if time.time() - start_time > 30:
                raise TimeoutError("Browser did not respond within 30 seconds.")
    except Exception as e:
        driver.quit()
        pytest.exit(f"\nTimeout or error when initializing browser: {e}", returncode=1)

    yield driver
    driver.quit()