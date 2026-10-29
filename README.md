# 🛍️ ShopEasy — Online Shopping Website

ShopEasy is a web-based online shopping website built with **Python, Flask, MySQL, HTML, CSS, and JavaScript**. It lets users browse products, view descriptions and prices, manage a shopping cart, place orders, and access order history. The project also includes product/order administration and downloadable invoice or receipt PDFs.

> **Academic project:** This application is intended for learning and demonstration. Configure and test security and payment features before any real-world deployment.

## ✨ Features

- **Product catalogue** — product names, descriptions, images, prices, and stock.
- **Product image support** — images served from `static/images/`.
- **User accounts** — registration, login, and session-based access, as implemented.
- **Shopping cart** — add products and manage selected items.
- **Stock and price management** — maintain product stock and prices in MySQL.
- **Order management** — store orders and order items and view order history.
- **Invoice / receipt PDF** — download an order invoice or receipt.
- **Admin functionality** — product and order management where enabled.
- **Payment integration** — Razorpay workflow when configured with valid credentials.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend application logic |
| Flask | Web framework and routes |
| MySQL | Database |
| PyMySQL | Python–MySQL connectivity |
| HTML | Page structure |
| CSS | Styling and layout |
| JavaScript | Client-side interactions |
| phpMyAdmin / XAMPP | Local database administration |
| Razorpay | Payment integration, if configured |

## 📁 Project Structure

The exact structure may differ slightly depending on your current files.

```text
Online-Shopping-Website/
├── app.py
├── templates/
│   ├── products.html
│   ├── cart.html
│   ├── orders.html
│   └── ... other HTML templates
├── static/
│   ├── images/
│   │   ├── laptop.jpg
│   │   ├── mobile.jpg
│   │   ├── headphone.jpg
│   │   └── ... other product images
│   └── style.css
├── README.md
└── ... configuration and dependency files
```

## ✅ Prerequisites

- Python 3
- MySQL Server or XAMPP with MySQL/MariaDB
- Visual Studio Code (recommended)
- A modern browser
- The Python packages required by `app.py`

## 🚀 Setup and Run Locally

### 1. Clone the repository

Replace `YOUR-GITHUB-USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/Online-Shopping-Website.git
cd Online-Shopping-Website
```

Alternatively, download and extract the repository ZIP.

### 2. Create a virtual environment (recommended)

**Windows — Command Prompt:**

```bat
python -m venv venv
venv\Scripts\activate
```

**Windows — PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Common packages for this project include:

```bash
pip install Flask PyMySQL python-dotenv
```

Install any additional libraries your invoice generator or other modules use. If the repository contains `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database

Start MySQL through XAMPP or your installed MySQL service. Open `http://localhost/phpmyadmin` and create a database named `shopeasy`:

```sql
CREATE DATABASE shopeasy;
```

Import your project's SQL file if available. Otherwise, create the tables required by your application (`users`, `categories`, `products`, `cart`, `orders`, and `order_items`) using your existing schema. The exact schema can vary by project version.

### 5. Configure environment variables

If your application uses `python-dotenv`, create a local `.env` file in the project root and set the values expected by your `app.py`. Example values:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=shopeasy

RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

These names are examples—match them to the variable names in your code. Never publish real passwords or API secrets. Add `.env` to `.gitignore`.

Example `.gitignore` entries:

```gitignore
.env
venv/
__pycache__/
*.py[cod]
```

### 6. Run the Flask application

From the project folder:

```bash
python app.py
```

Open the website:

```text
http://127.0.0.1:5000/products
```

If your application uses a different home route, open that route instead.

## 🖼️ Adding Products and Images

1. Save product images inside `static/images/`.
2. Add a product row to the `products` table with its name, description, price, image filename, stock, and valid category ID.
3. Ensure the filename stored in MySQL exactly matches the image filename, including spaces and suffixes such as `(2).jpg`.
4. Refresh the products page and verify the image, price, description, and stock.

Example image path: `static/images/laptop.jpg`

Do not use a category ID unless it exists in the `categories` table.

## 🗄️ Main Database Tables

Based on the current project structure, the main tables are:

- `users` — user account information
- `categories` — product categories
- `products` — product details, price, image, stock, and category
- `cart` — selected products and quantities
- `orders` — order totals, dates, statuses, and payment details
- `order_items` — products and quantities associated with each order

The exact columns and constraints should match your database schema.

## 🧾 Invoices and Receipts

ShopEasy can generate downloadable PDF invoice/receipt documents for orders. Depending on the implementation, they may include the invoice number, order date, product lines, quantities, prices, total, and order/payment status.

A payment should be marked as paid only after the server verifies the payment provider's result. A pending payment should not be presented as a completed payment receipt.

## 🧪 Basic Testing Checklist

- [ ] The products page loads successfully.
- [ ] Product images and descriptions display correctly.
- [ ] Prices and stock match the database.
- [ ] An in-stock product can be added to the cart.
- [ ] Out-of-stock products cannot be purchased.
- [ ] Cart quantities and totals are calculated correctly.
- [ ] Checkout creates correct order and order-item records.
- [ ] Order history shows only the logged-in user's orders.
- [ ] Invoice/receipt PDF downloads and displays correct order details.
- [ ] Payment statuses reflect verified results, if payment integration is enabled.

## 🔐 Security Notes

- Never commit `.env`, passwords, API keys, or payment secrets to GitHub.
- Use test credentials during development and payment testing.
- Use password hashing and server-side validation.
- Protect admin routes and user-specific order routes with authentication and authorization.
- Use parameterized SQL queries.
- Before public deployment, configure HTTPS, secure session settings, backups, error logging, and payment verification.

## 🛠️ Troubleshooting

**MySQL connection error**
- Ensure MySQL is running.
- Check the database name, username, password, and host.
- Confirm the `shopeasy` database and required tables exist.

**Product image not visible**
- Confirm the file exists under `static/images/`.
- Confirm the filename in MySQL matches the file exactly.
- Ensure the template uses Flask's static-file URL correctly.

**Product does not appear**
- Confirm the product row exists in `products`.
- Check that the product route queries the correct database and table.
- Refresh the page after saving changes.

**Payment or invoice issue**
- Check the Flask terminal for the error traceback.
- Verify payment configuration with test credentials.
- Confirm the invoice route retrieves the correct order and order items.

## 👨‍💻 Author

**Mausam Chaturvedi**  
MCA — University Institute of Computing, Chandigarh University  
UID: 26MCA20182

## 📌 Project Purpose

This project demonstrates full-stack web development, relational database management, product and stock maintenance, shopping-cart workflows, order processing, and invoice generation for an academic project.

## 📄 License

No license has been specified yet. If you intend others to reuse the project, add an appropriate license file and update this section.
