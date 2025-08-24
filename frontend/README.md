# ERP System Frontend

A modern, responsive web frontend for the ERP System built with Flask and Bootstrap.

## Features

- 🎨 Modern, responsive design with Bootstrap 5
- 📊 Interactive dashboard with real-time statistics
- 👥 Customer management (CRUD operations)
- 🧾 Invoice management
- 💳 Payment tracking
- 🔐 Secure authentication with JWT tokens
- 📱 Mobile-friendly responsive design
- ⚡ Fast and lightweight

## Screenshots

### Dashboard
- Real-time statistics and charts
- Quick action buttons
- Performance metrics

### Customer Management
- List all customers with search functionality
- Add/Edit/Delete customers
- Customer detail views

### Payments
- Payment tracking and history
- Payment method management
- Summary statistics

## Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd erpsystem/frontend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Make sure your FastAPI backend is running:**
   ```bash
   # In another terminal, from erpsystem directory
   python run.py
   ```

4. **Start the frontend server:**
   ```bash
   python run.py
   ```

5. **Open your browser:**
   ```
   http://localhost:5000
   ```

## Default Login

- **Email:** admin@admin.com
- **Password:** admin123

## Project Structure

```
frontend/
├── app.py                 # Main Flask application
├── run.py                 # Startup script
├── requirements.txt       # Python dependencies
├── routes/               # Route blueprints
│   ├── __init__.py
│   ├── customers.py      # Customer routes
│   ├── invoices.py       # Invoice routes
│   └── payments.py       # Payment routes
└── templates/            # HTML templates
    ├── base.html         # Base template
    ├── login.html        # Login page
    ├── dashboard.html    # Dashboard
    ├── customers/        # Customer templates
    │   ├── list.html
    │   ├── create.html
    │   └── view.html
    └── payments/         # Payment templates
        └── list.html
```

## API Integration

The frontend communicates with the FastAPI backend running on `http://localhost:8000/api/v1/`

### Endpoints Used:
- `POST /auth/login` - User authentication
- `GET /users/me` - Get current user info
- `GET /customers/summary` - Customer statistics
- `GET /invoices/summary` - Invoice statistics
- `GET /quotes/summary` - Quote statistics
- `GET /payments/summary` - Payment statistics
- `GET /customers/` - List customers
- `POST /customers/` - Create customer
- `GET /customers/{id}` - Get customer details
- `PUT /customers/{id}` - Update customer
- `DELETE /customers/{id}` - Delete customer

## Features

### Authentication
- JWT token-based authentication
- Session management
- Automatic token refresh
- Secure logout

### Dashboard
- Real-time statistics from API
- Interactive charts and graphs
- Quick action buttons
- Performance metrics

### Customer Management
- Full CRUD operations
- Search and filter functionality
- Customer detail views
- Form validation

### Responsive Design
- Mobile-first approach
- Bootstrap 5 components
- Custom CSS styling
- Interactive animations

## Customization

### Styling
The frontend uses custom CSS variables for easy theming:

```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --success-color: #27ae60;
    --warning-color: #f39c12;
    --danger-color: #e74c3c;
}
```

### Adding New Routes
1. Create a new blueprint in `routes/`
2. Register it in `app.py`
3. Create corresponding templates
4. Add navigation links in `base.html`

## Development

### Running in Development Mode
```bash
python run.py
```

### Production Deployment
For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Make sure FastAPI backend is running on port 8000
   - Check API_BASE_URL in route files

2. **Authentication Issues**
   - Clear browser cookies/session
   - Check if user exists in database
   - Verify JWT token format

3. **Template Not Found**
   - Check template file paths
   - Ensure templates directory structure is correct

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
