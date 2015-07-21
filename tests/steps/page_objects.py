# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
#
# driver = webdriver.Firefox()
# driver.get("http://localhost:8000/register")
#
# class page_objects(object):
#     def wait_page_load(self,byElementId):
#         try:
#             element = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.ID, byElementId))
#             )
#         finally:
#             driver.quit()
#
# #
# # class wait_for_page_load(object):
# #
# #     def __init__(self, browser):
# #         self.browser = browser
# #
# #     def __enter__(self):
# #         self.old_page = self.browser.find_element_by_tag_name('html')
# #
# #     def page_has_loaded(self):
# #         new_page = self.browser.find_element_by_tag_name('html')
# #         return new_page.id != self.old_page.id
# #
# #     def __exit__(self, *_):
# #         wait_for(self.page_has_loaded)
# #
# #     def wait_for(condition_function):
# #         start_time = time.time()
# #         while time.time() < start_time + 3:
# #             if condition_function():
# #                 return True
# #                 else:
# #                 time.sleep(0.1)
# #
# #         raise Exception(
# #         'Timeout waiting for {}'.format(condition_function.__name__)
# #         )
# #
