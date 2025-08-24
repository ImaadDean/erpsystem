#!/usr/bin/env python3
"""
Startup script for the ERP System
"""

import uvicorn
import os
from app.core.config import settings

if __name__ == "__main__":
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("Please copy .env.example to .env and configure your settings.")
        print("Example: cp .env.example .env")
        exit(1)
    
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"🌍 Environment: {settings.ENVIRONMENT}")
    print(f"🔧 Debug mode: {settings.DEBUG}")
    print("📚 API Documentation will be available at: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )
