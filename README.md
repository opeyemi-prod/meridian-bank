# Meridian Bank API

Backend service for the Meridian Bank web and mobile clients. Provides
authentication, account management, fund transfers, statements, and
administrative operations over a JSON REST API.

## Features

- Customer registration and token-based login (JWT)
- Account balance and transaction history
- Inter-account fund transfers
- Monthly statement generation, retrieval, and co-branding
- Operations/admin tooling: user listing, database backup, config import,
  and metrics

## Stack

- Python 3 / Flask (application-factory pattern, blueprints per domain)
- SQLite (development) — swappable for PostgreSQL in production
- PyJWT for session tokens
- `requests` for payment-gateway and FX-provider integration

## Getting started

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # fill in your secrets
python run.py               # starts on http://0.0.0.0:8080
```

The database schema is created and seeded automatically on first run.

## Project layout

```
meridian-bank/
├── run.py                  # entrypoint
├── requirements.txt
├── .env.example
└── app/
    ├── __init__.py         # application factory
    ├── config.py
    ├── database.py
    ├── auth/               # register, login, password reset, JWT
    ├── accounts/           # balances, transactions, profile
    ├── transfers/          # fund movement
    ├── admin/              # operations tooling
    ├── statements/         # statement PDFs and branding
    └── utils/              # shared helpers
```

## API overview

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Create a customer account |
| POST | `/api/auth/login` | Obtain a JWT |
| POST | `/api/auth/reset` | Request a password-reset token |
| GET  | `/api/auth/whoami` | Inspect the current token's claims |
| GET  | `/api/accounts/<id>` | Account details |
| GET  | `/api/accounts/<id>/transactions` | Transaction list |
| POST | `/api/accounts/profile` | Update profile fields |
| POST | `/api/transfers` | Move funds between accounts |
| GET  | `/api/transfers/history` | Transfer history |
| GET  | `/api/admin/users` | List users (ops) |
| POST | `/api/admin/backup` | Trigger a database backup (ops) |
| POST | `/api/admin/config/import` | Load a config bundle (ops) |
| GET  | `/api/statements/download` | Download a statement file |
| GET  | `/api/statements/branding` | Fetch a co-branding logo |

## License

Internal — Meridian Bank Engineering.
