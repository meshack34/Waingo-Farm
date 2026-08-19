# 🌱 Waingo Farm

Waingo Farm is a Django-powered agricultural e-commerce and farm management website designed to showcase and sell farm products online.

## 🚀 Project Overview

The platform provides customers with a simple way to browse farm products, view product details, explore the farm gallery, and place orders. It also includes an owner/admin area for managing products and farm content.

## ✨ Features

- 🛒 Online farm shop
- 🌱 Product management
- 📦 Product categories
- 🖼️ Farm image gallery
- 🔍 Product browsing and filtering
- 🧑‍🌾 Owner dashboard
- 📱 Responsive design
- 💳 M-Pesa payment integration
- 📸 Product and gallery image uploads
- 🔐 Django authentication and administration
- 🗄️ Database-backed product management

## 🛠️ Technologies

- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **Icons:** Bootstrap Icons
- **Database:** SQLite for development / configurable production database
- **Payments:** Safaricom M-Pesa Daraja API
- **Deployment:** PythonAnywhere
- **Version Control:** Git & GitHub

## 📂 Project Structure

```text
Waingo-Farm/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── media/
│   └── products/
├── static/
├── templates/
├── owner/
├── products/
└── waingo_farm/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py
```

> Folder names may differ slightly depending on the current project structure.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd Waingo-Farm
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DARAJA_CONSUMER_KEY=your-consumer-key
DARAJA_CONSUMER_SECRET=your-consumer-secret
DARAJA_SHORTCODE=your-shortcode
DARAJA_PASSKEY=your-passkey
DARAJA_CALLBACK_URL=your-callback-url
```

**Never commit `.env` or other secrets to GitHub.**

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create an admin account

```bash
python manage.py createsuperuser
```

### 7. Collect static files

```bash
python manage.py collectstatic
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## 🖼️ Static and Media Files

The project uses:

- `static/` for CSS, JavaScript and static assets
- `media/` for uploaded product and gallery images

For production, make sure the media directory exists on the server and that Django is configured correctly for `MEDIA_ROOT` and `MEDIA_URL`.

Example:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

During development, media URLs can be served from the project's URL configuration.

## 💳 M-Pesa Integration

Waingo Farm integrates with the Safaricom Daraja API for M-Pesa payments.

The application uses environment variables for sensitive Daraja credentials.

For local callback testing, a tunneling service such as ngrok can be used to expose the local development server.

Example:

```text
DARAJA_CALLBACK_URL=https://your-ngrok-url.ngrok-free.app/...
```

## 🌐 Deployment

The project can be deployed to PythonAnywhere.

Typical deployment steps include:

1. Clone or pull the project from GitHub.
2. Create/activate the virtual environment.
3. Install `requirements.txt`.
4. Configure environment variables.
5. Configure the WSGI application.
6. Run database migrations.
7. Run `collectstatic`.
8. Configure static files.
9. Configure media files.
10. Reload the web application.

### Important

Static files and uploaded media files are different:

- **Static:** CSS, JavaScript, icons and site assets.
- **Media:** Uploaded product/gallery images.

Uploaded media must exist on the production server. They are not automatically uploaded to PythonAnywhere simply because the code was pushed to GitHub.

## 🔒 Security

Before production deployment:

- Set `DEBUG=False`
- Use a strong Django `SECRET_KEY`
- Keep `.env` out of Git
- Configure `ALLOWED_HOSTS`
- Use HTTPS
- Protect M-Pesa credentials
- Configure production static and media files correctly

## 🧪 Development

Run Django checks:

```bash
python manage.py check
```

Run tests:

```bash
python manage.py test
```

## 📌 Current Product Categories

- Vegetables
- Fruits
- Cereals & Grains
- Root & Tuber Crops
- Legumes
- Herbs & Spices
- Livestock
- Poultry
- Eggs & Dairy
- Seeds & Seedlings
- Animal Feeds
- Farm Inputs

## 👨‍💻 Author

**Meshack Kimutai**

Waingo Farm — Agricultural E-commerce Platform

## 📄 License

This project is currently intended for the Waingo Farm project and is not published under an open-source license unless otherwise stated.
