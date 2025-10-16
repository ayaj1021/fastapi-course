from sqlalchemy import create_engine

# Paste your actual database URL from Render here
DATABASE_URL = "postgresql://postgressql_fastapi_course_user:uMluego05GoOdXV8QINu0RFLI2sIAOx4@dpg-d3o85ter433s739scfeg-a.oregon-postgres.render.com/postgressql_fastapi_course"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("✅ Connection successful!")
except Exception as e:
    print("❌ Connection failed:", e)
