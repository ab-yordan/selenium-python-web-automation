from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestLogin:

    def test_login_success(self, driver):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login("Admin", "admin123")
        assert "dashboard" in driver.current_url.lower()

    def test_login_failed(self, driver):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login("Admin", "wrongpass")
        assert "dashboard" not in driver.current_url.lower()

    def test_dashboard_visible(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        login_page.load()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_displayed()

    def test_invalid_username(self, driver):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login("InvalidUser", "admin123")
        assert "dashboard" not in driver.current_url.lower()

    def test_empty_credentials(self, driver):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login("", "")
        assert "dashboard" not in driver.current_url.lower()
