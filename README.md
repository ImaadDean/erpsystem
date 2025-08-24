# ERP System - FastAPI + Supabase

A modern ERP/CRM system built with FastAPI and Supabase database.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Customer Management**: Create, read, update, and delete customer records
- **Invoice Management**: Generate and manage invoices with line items
- **Quote Management**: Create quotes and convert them to invoices
- **Payment Tracking**: Record and track payments against invoices
- **RESTful API**: Clean, documented API endpoints
- **Database**: Supabase (PostgreSQL) for reliable data storage

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Validation**: Pydantic models
- **Documentation**: Auto-generated OpenAPI/Swagger docs

## Project Structure

```
erpsystem/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── customers.py
│   │       │   ├── invoices.py
│   │       │   ├── quotes.py
│   │       │   └── payments.py
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── customer.py
│   │   ├── invoice.py
│   │   ├── quote.py
│   │   └── payment.py
│   ├── models/
│   ├── services/
│   └── utils/
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd erpsystem
pip install -r requirements.txt
```

### 2. Set up Supabase

1. Create a new project at [supaRequest error 404
No account with this email has been registered.base.com](https://supabase.com)
2. Get your project URL and API keys
3. Create the required database tables (see Database Schema section)

### 3. Environment Configuration

1. Copy `.env.example` to `.env`
2. Fill in your Supabase credentials and other configuration

```bash
cp .env.example .env
```

### 4. Run the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Database Schema

You'll need to create these tables in your Supabase database:

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Customers Table
```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR,
    phone VARCHAR,
    address TEXT,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR,
    postal_code VARCHAR,
    tax_number VARCHAR,
    notes TEXT,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Invoices Table
```sql
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    quote_id INTEGER,
    invoice_number VARCHAR,
    issue_date DATE,
    due_date DATE,
    total_amount DECIMAL(10,2) NOT NULL,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    items JSONB,
    notes TEXT,
    terms TEXT,
    status VARCHAR DEFAULT 'draft',
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Quotes Table
```sql
CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    quote_number VARCHAR,
    issue_date DATE,
    expiry_date DATE,
    total_amount DECIMAL(10,2) NOT NULL,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    items JSONB,
    notes TEXT,
    terms TEXT,
    status VARCHAR DEFAULT 'draft',
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Payments Table
```sql
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    invoice_id INTEGER REFERENCES invoices(id),
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR NOT NULL,
    payment_date DATE,
    reference_number VARCHAR,
    notes TEXT,
    status VARCHAR DEFAULT 'pending',
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/` - Get all users (admin only)

### Customers
- `POST /api/v1/customers/` - Create customer
- `GET /api/v1/customers/` - List customers
- `GET /api/v1/customers/{id}` - Get customer
- `PUT /api/v1/customers/{id}` - Update customer
- `DELETE /api/v1/customers/{id}` - Delete customer

### Invoices
- `POST /api/v1/invoices/` - Create invoice
- `GET /api/v1/invoices/` - List invoices
- `GET /api/v1/invoices/{id}` - Get invoice
- `PUT /api/v1/invoices/{id}` - Update invoice
- `DELETE /api/v1/invoices/{id}` - Delete invoice

### Quotes
- `POST /api/v1/quotes/` - Create quote
- `GET /api/v1/quotes/` - List quotes
- `GET /api/v1/quotes/{id}` - Get quote
- `PUT /api/v1/quotes/{id}` - Update quote
- `POST /api/v1/quotes/{id}/convert-to-invoice` - Convert quote to invoice

### Payments
- `POST /api/v1/payments/` - Create payment
- `GET /api/v1/payments/` - List payments
- `GET /api/v1/payments/{id}` - Get payment
- `PUT /api/v1/payments/{id}` - Update payment
- `POST /api/v1/payments/{id}/confirm` - Confirm payment

## Development

### Running Tests
```bash
pytest
```

### Code Style
The project follows PEP 8 style guidelines.

## License

This project is open source and available under the [MIT License](LICENSE).
