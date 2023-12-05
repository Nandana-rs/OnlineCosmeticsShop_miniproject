from django.test import TestCase

# Create your tests here.
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginTest(unittest.TestCase):
    def setUp(self):
        # Start the Selenium WebDriver
        self.driver = webdriver.Chrome()  # Adjust based on your WebDriver configuration
        self.driver.get("http://127.0.0.1:8000/login/")  # Replace with the actual URL of your login page

    def test_login_successful(self):
        # Find the username, password, and login button elements
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        
        # You can use a more robust selector for the login button
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )

        # Enter valid credentials
        username_input.send_keys("Anna")
        password_input.send_keys("Anna@123")

        # Click the login button
        login_button.click()

        # Wait for a while to see the result (you can adjust this based on your application's response time)
        time.sleep(2)
        
        # Assert that the URL matches the expected redirect
        self.assertEqual(self.driver.current_url, 'http://127.0.0.1:8000/home2/')

    def tearDown(self):
        # Close the browser window
        self.driver.close()


if __name__ == "__main__":
    unittest.main()


# #test2
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Start the WebDriver (you can use other browsers as well)
# driver = webdriver.Chrome()

# try:
#     # Open the HTML page
#     url = 'http://127.0.0.1:8000/serums_products/'  # Replace with the actual file path or URL
#     driver.get(url)

#     # Wait for the product list to be present on the page
#     product_list = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, 'product-list'))
#     )

#     # Get the list of products
#     products = product_list.find_elements(By.CLASS_NAME, 'product')

#     # Perform assertions or interactions based on your requirements
#     assert len(products) > 0, "No products found on the page."

#     # Example: Click on the first product and check if it redirects to the product detail page
#     first_product = products[0]
#     product_link = first_product.find_element(By.TAG_NAME, 'a')
#     product_link.click()

#     # Wait for the product detail page to load
#     WebDriverWait(driver, 10).until(
#         EC.title_contains('Product Detail')
#     )

#     # Perform more assertions or interactions on the product detail page if needed

# finally:
#     # Close the browser window
#     driver.quit()


#test3
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By

# class AddProductTest(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()  # or webdriver.Firefox() or other WebDriver
#         self.driver.get("http://127.0.0.1:8000/add_product/")

#     def tearDown(self):
#         self.driver.quit()

#     def test_add_product(self):
#         # Fill in the form with sample data
#         self.driver.find_element(By.ID, "productName").send_keys("Sample Product")
#         self.driver.find_element(By.ID, "productDescription").send_keys("Sample product description.")
#         self.driver.find_element(By.ID, "productPrice").send_keys("19.99")
        
#         # Select options from dropdowns
#         Select(self.driver.find_element(By.ID, "productCategory")).select_by_visible_text("Skincare")
#         Select(self.driver.find_element(By.ID, "productBrand")).select_by_visible_text("L'Oréal")
#         Select(self.driver.find_element(By.ID, "productSeller")).select_by_index(1)  # Assuming there's at least one seller

#         self.driver.find_element(By.ID, "stockQuantity").send_keys("100")

#         # Upload an image (replace 'path/to/your/image.jpg' with the actual path)
#         self.driver.find_element(By.ID, "productImage").send_keys("C:\\Users\\91730\\Desktop\\Cosmetics\\media\\product_images\\lakmefoundation1.PNG")

#         # Select a status
#         Select(self.driver.find_element(By.ID, "productStatus")).select_by_visible_text("Active")

#         # Enable the "Add Product" button
#         self.driver.find_element(By.ID, "addProductButton").click()

#         # Wait for the success modal to appear (you may need to adjust the wait time)
#         success_modal = self.driver.find_element(By.ID, "successModal")
#         self.assertTrue(success_modal.is_displayed(), "Success modal is not displayed")

# if __name__ == "__main__":
#     unittest.main()



#test4
