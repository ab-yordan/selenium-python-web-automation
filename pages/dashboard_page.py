from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class DashboardPage(BasePage):
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")

    def is_dashboard_displayed(self):
        return self.is_visible(self.DASHBOARD_HEADER)
