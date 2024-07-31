### Food Delivery Application ###
 ~ This is a food delivery application built with Flask that allows users to order food, and administrators to manage the products and view orders. ~

### Features
! User registration and login
! Product listing and ordering for users
! Admin functionalities to add and delete products
! Order confirmation and details display
! Input validation for phone numbers
! Installation
! Clone the repository


### File Structure
@ app.py: The main Flask application file.
@ templates/: Contains all HTML templates.
@ login.html: User login page.
@ signup.html: User registration page.
@ home_user.html: User homepage for ordering food.
@ home_admin.html: Admin homepage for managing products.
@ order_success.html: Page displayed after a successful order.
@ admin_orders.html: Admin page to view all orders.
@ static/css/: Contains CSS files for styling.
@ static/uploads: Contains all image for product.
@ home_user.css: CSS for user homepage.
@ home_admin.css: CSS for admin homepage.
@ food_app.py: Contains helper functions to interact with the database and perform business logic.

### Routes
- /: Displays the login page.
- /login: Processes the login form and redirects to the appropriate homepage.
- /signup: Displays and processes the signup form.
- /order: Displays the order form and processes order submissions.
- /order_success: Displays order success message and details.
- /add_products: Admin functionality to add new products.
- /delete_product/<int:product_id>: Admin functionality to delete a product.
- /log_out: Logs out the current user and redirects to the login page.

Adding and Deleting Products
Adding Products: Admins can add products from the admin homepage by filling out a form.
Deleting Products: Admins can delete products from the admin homepage by clicking the "Sterge" button next to each product.

# Validations
Phone Number Validation: Ensures that the phone number starts with '07' and has exactly 10 digits.

# Example Usage
User Signup
Navigate to the signup page and create a new account.

# User Login
Use your credentials to log in.

# Place an Order
Select products, enter your details, and place an order.

# Admin Functions
Log in as an admin to add or delete products.

### Admin ###
For show order please run main.py and admin_order_message.py
