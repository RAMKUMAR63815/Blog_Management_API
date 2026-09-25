import sqlite3

DB_NAME = "blog.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

try:
    print("Starting users table migration...")

    # Disable foreign key checks temporarily
    cursor.execute("PRAGMA foreign_keys = OFF")

    # Create new users table with password nullable
    cursor.execute("""
        CREATE TABLE users_new (
            id INTEGER PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255),
            subscription_plan_id INTEGER,
            provider VARCHAR(50) NOT NULL DEFAULT 'local',
            auth0_id VARCHAR(255) UNIQUE
        )
    """)

    # Copy existing users
    cursor.execute("""
        INSERT INTO users_new (
            id,
            username,
            email,
            password,
            subscription_plan_id,
            provider,
            auth0_id
        )
        SELECT
            id,
            username,
            email,
            password,
            subscription_plan_id,
            provider,
            auth0_id
        FROM users
    """)

    # Remove old table
    cursor.execute("DROP TABLE users")

    # Rename new table
    cursor.execute("""
        ALTER TABLE users_new
        RENAME TO users
    """)

    # Recreate indexes
    cursor.execute("""
        CREATE INDEX ix_users_id
        ON users (id)
    """)

    cursor.execute("""
        CREATE INDEX ix_users_username
        ON users (username)
    """)

    cursor.execute("""
        CREATE INDEX ix_users_email
        ON users (email)
    """)

    cursor.execute("""
        CREATE INDEX ix_users_auth0_id
        ON users (auth0_id)
    """)

    conn.commit()

    print("Users table migration completed successfully!")

except Exception as e:
    conn.rollback()
    print("Migration failed:", e)

finally:
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.close()