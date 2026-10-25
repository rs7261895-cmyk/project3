# ConstructionMart — Vercel-ready Django project

A responsive Django storefront demo for browsing construction materials, managing a session cart, and creating sample orders.

## Important limitations

- Checkout creates a demo order only. It does **not** take payments or contact suppliers.
- Product prices and suppliers are sample data. Verify them before using this as a real store.
- Vercel production deployments require a persistent PostgreSQL database. The project deliberately refuses to use SQLite on Vercel because its filesystem is not persistent.

## Deploy to Vercel

### 1. Create a PostgreSQL database

Create a database with a hosted PostgreSQL provider such as Neon, or add a PostgreSQL integration from your Vercel project. Copy its connection URL. Ensure the provider's connection URL includes SSL settings if required by the provider.

### 2. Add Vercel environment variables

In **Vercel → Project → Settings → Environment Variables**, add these for Production (and Preview if you will use preview deployments):

- `DATABASE_URL`: PostgreSQL connection string from your database provider.
- `DJANGO_SECRET_KEY`: a long, random secret. Generate locally with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`.
- `DEBUG`: `False`.

Do not commit real secrets to GitHub. The `DJANGO_ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` variables are optional comma-separated lists for any custom domains; `.vercel.app` hosts are already allowed.

### 3. Deploy

Push this folder's contents to the GitHub repository connected to Vercel. Keep `manage.py`, `requirements.txt`, `pyproject.toml`, `.python-version`, and the `constructionmart/`, `store/`, `templates/`, and `static/` folders at the repository root. In Vercel, use the **Django** framework preset / automatic detection and leave the Root Directory set to the folder containing `manage.py`.

The Vercel build hook runs database migrations, collects static files, and creates the sample products that are missing. It will not overwrite product stock or prices that have already been edited.

### 4. Create an admin user

After the first deployment, run the following from your local terminal with `DATABASE_URL` set to the same PostgreSQL database URL:

```powershell
python -m pip install -r requirements.txt
python manage.py createsuperuser
```

Then visit `/admin/` on your deployed site.

## Run locally on Windows

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_products
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Without `DATABASE_URL`, local development uses `db.sqlite3`.

## Main features

- Construction materials catalogue, search, and category filters
- Quantity and price calculator on product cards
- Session-based shopping cart
- Demo checkout and order confirmation
- Django admin for products and orders
- Responsive layout

## Troubleshooting

- **`DATABASE_URL` missing on Vercel:** add the PostgreSQL connection string in Vercel Environment Variables, then redeploy.
- **`DJANGO_SECRET_KEY` missing:** add a random secret in Vercel Environment Variables, then redeploy.
- **No products shown:** check the build log for the `seed_products` command. You can run `python manage.py seed_products` with the production database URL set.
- **Existing SQLite data:** it is not automatically copied into PostgreSQL. Export and import it separately if you need to preserve local products or orders.
