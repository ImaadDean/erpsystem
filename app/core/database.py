try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

from app.core.config import settings
import asyncio


class MockSupabaseClient:
    """Mock client for when Supabase is not available"""
    def table(self, table_name: str):
        return MockTable(table_name)


class MockTable:
    """Mock table for testing without database"""
    def __init__(self, table_name: str):
        self.table_name = table_name

    def select(self, *args):
        return MockQuery(self.table_name, "select")

    def insert(self, data):
        return MockQuery(self.table_name, "insert", data)

    def update(self, data):
        return MockQuery(self.table_name, "update", data)

    def delete(self):
        return MockQuery(self.table_name, "delete")


class MockQuery:
    """Mock query for testing without database"""
    def __init__(self, table_name: str, operation: str, data=None):
        self.table_name = table_name
        self.operation = operation
        self.data = data

    def eq(self, column, value):
        return self

    def limit(self, count):
        return self

    def range(self, start, end):
        return self

    def execute(self):
        # Return mock response
        if self.operation == "select":
            return type('MockResponse', (), {'data': []})()
        elif self.operation == "insert":
            return type('MockResponse', (), {'data': [{'id': 1, **self.data}] if self.data else [{'id': 1}]})()
        else:
            return type('MockResponse', (), {'data': []})()


class SupabaseClient:
    def __init__(self):
        self.client: Client = None
        self.service_client: Client = None
        self._connection_attempted = False

    def get_client(self) -> Client:
        """Get the regular Supabase client (with anon key)"""
        if not self.client and not self._connection_attempted:
            self._connection_attempted = True
            if not SUPABASE_AVAILABLE:
                print("⚠️  Supabase library not available, using mock client")
                self.client = MockSupabaseClient()
                return self.client

            try:
                # Create client using simple positional arguments
                self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
                print("✅ Supabase client created successfully")
            except Exception as e:
                print(f"❌ Error creating Supabase client: {e}")
                print("🔄 Using mock client for development")
                self.client = MockSupabaseClient()
        return self.client

    def get_service_client(self) -> Client:
        """Get the service role Supabase client (with service key)"""
        if not self.service_client:
            if not SUPABASE_AVAILABLE:
                print("⚠️  Supabase library not available, using mock service client")
                self.service_client = MockSupabaseClient()
                return self.service_client

            try:
                # Create service client using simple positional arguments
                self.service_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
                print("✅ Supabase service client created successfully")
            except Exception as e:
                print(f"❌ Error creating Supabase service client: {e}")
                print("🔄 Using mock service client for development")
                self.service_client = MockSupabaseClient()
        return self.service_client


# Global instance
supabase_client = SupabaseClient()


def get_supabase() -> Client:
    """Dependency to get Supabase client"""
    return supabase_client.get_client()


def get_supabase_service() -> Client:
    """Dependency to get Supabase service client"""
    return supabase_client.get_service_client()


async def init_db():
    """Initialize database connection"""
    try:
        client = get_supabase()
        if client is None:
            print("❌ Database connection failed: Could not create Supabase client")
            return

        # Test connection (this will work with both real and mock clients)
        response = client.table('users').select('id').limit(1).execute()

        if isinstance(client, MockSupabaseClient):
            print("🔄 Using mock database client for development")
            print("📝 To use real database:")
            print("   1. Fix the Supabase client dependency issue")
            print("   2. Run the database_setup.sql script in your Supabase project")
        else:
            print("✅ Database connection established")

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Note: Make sure you have run the database_setup.sql script in your Supabase project")
