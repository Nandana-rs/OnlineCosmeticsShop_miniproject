from django.test import TestCase

# Create your tests here.


#test1 nrs
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# class LoginTest(unittest.TestCase):
#     def setUp(self):
#         # Start the Selenium WebDriver
#         self.driver = webdriver.Chrome()  # Adjust based on your WebDriver configuration
#         self.driver.get("http://127.0.0.1:8000/login/")  # Replace with the actual URL of your login page

#     def test_login_successful(self):
#         # Find the username, password, and login button elements
#         username_input = self.driver.find_element(By.NAME, "username")
#         password_input = self.driver.find_element(By.NAME, "password")
        
#         # You can use a more robust selector for the login button
#         login_button = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
#         )

#         # Enter valid credentials
#         username_input.send_keys("SnehaElsa")
#         password_input.send_keys("Sneha@123")

#         # Click the login button
#         login_button.click()

#         # Wait for a while to see the result (you can adjust this based on your application's response time)
#         time.sleep(2)
        
#         # Assert that the URL matches the expected redirect
#         self.assertEqual(self.driver.current_url, 'http://127.0.0.1:8000/seller_template/')

#     def tearDown(self):
#         # Close the browser window
#         self.driver.close()


# if __name__ == "__main__":
#     unittest.main()


#test2 nrs
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





#test3_add product
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from django.urls import reverse  # Import reverse from django.urls

# class AddProductTest(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)
#         self.live_server_url = 'http://127.0.0.1:8000/'

#     def tearDown(self):
#         self.driver.quit()

#     def login(self, username, password):
#         driver = self.driver
#         driver.get(self.live_server_url)

#         # Find the login link and click on it
#         login_link = driver.find_element(By.XPATH, "//a[text()='Login']")
#         login_link.click()

#         # Enter username and password
#         username_input = driver.find_element(By.ID, "username")
#         username_input.send_keys(username)

#         password_input = driver.find_element(By.ID, "password")
#         password_input.send_keys(password)

#         # Submit the login form
#         login_button = driver.find_element(By.CLASS_NAME, "login-button")
#         login_button.click()

#         # Wait for login to complete
#         WebDriverWait(driver, 10).until(EC.url_changes(self.live_server_url))

#     def test_add_product(self):
#         # Login first
#         self.login("Naveen", "Naveen@123")

#         driver = self.driver

#         # Access the add_product page using reverse
#         add_product_url = reverse('add_product')
#         driver.get(self.live_server_url + add_product_url)

#         # Wait for the form to load
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "productName")))

#         # Fill out the form
#         product_name = driver.find_element(By.ID, "productName")
#         product_name.send_keys("Test Product")

#         product_description = driver.find_element(By.ID, "productDescription")
#         product_description.send_keys("This is a test product description.")

#         product_price = driver.find_element(By.ID, "productPrice")
#         product_price.send_keys("19.99")

#         product_category = Select(driver.find_element(By.ID, "productCategory"))
#         product_category.select_by_value("Face Makeup")

#         product_subcategory = Select(driver.find_element(By.ID, "productSubcategory"))
#         product_subcategory.select_by_value("Blush")

#         product_brand = Select(driver.find_element(By.ID, "productBrand"))
#         product_brand.select_by_value("L'Oréal")

#         stock_quantity = driver.find_element(By.ID, "stockQuantity")
#         stock_quantity.send_keys("30")

#         product_image = driver.find_element(By.ID, "productImage")
#         product_image.send_keys(r"C:\Users\91730\Desktop\Cosmetics\media\product_images\bluelady.png")

#         product_seller = Select(driver.find_element(By.ID, "productSeller"))
#         product_seller.select_by_index(1)

#         product_status = Select(driver.find_element(By.ID, "productStatus"))
#         product_status.select_by_value("active")

#         # Submit the form
#         add_product_button = driver.find_element(By.ID, "addProductButton")
#         add_product_button.click()

#         # Wait for the success modal to appear and assert its content
#         success_modal = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "successModal"))
#         )
#         success_message = success_modal.find_element(By.TAG_NAME, 'p').text
#         self.assertEqual(success_message, 'PRODUCT ADDED SUCCESSFULLY')

# if __name__ == "__main__":
#     unittest.main()


# MAIN PROJECT TESTS_______________________________________________________________________________________________________________________________
    

    #TEST1  for search bar

import time  # Import the time module

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductListSearchTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(20)
        self.live_server_url = 'http://127.0.0.1:8000/products/'  # Update with your actual URL

    def tearDown(self):
        # Delay for 5 seconds before closing the WebDriver
        time.sleep(5)
        self.driver.quit()

    def test_search_bar(self):
        driver = self.driver
        driver.get(self.live_server_url)  # Update with your actual URL

        # Find the search input and button
        search_input = driver.find_element(By.CSS_SELECTOR, '.search-bar > form:nth-child(1) > input:nth-child(1)')
        search_button = driver.find_element(By.CSS_SELECTOR, '.search-bar > form:nth-child(1) > button:nth-child(2)')

        # Perform a search
        search_input.send_keys('Bright')  # Replace with your search term
        search_button.click()

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-card'))
        )

        # Assert that the search results are displayed
        search_results = driver.find_elements(By.CLASS_NAME, 'product-card')
        self.assertGreater(len(search_results), 0, "No search results found.")

if __name__ == "__main__":
    unittest.main()

