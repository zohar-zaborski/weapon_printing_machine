from sqlalchemy import create_engine, inspect

# Specify the path to the test database explicitly
TEST_DATABASE_URL = "sqlite:///../test.db"  # Adjust this path if needed

# Create an engine connected to the test database
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

def print_existing_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if tables:
        print("Existing tables in the test database:")
        for table in tables:
            print(f"- {table}")
    else:
        print("No tables found in the test database.")

# Run the function
if __name__ == "__main__":
    print_existing_tables()
