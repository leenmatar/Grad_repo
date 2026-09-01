from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/support_ticket_db"

engine = create_engine(DATABASE_URL)
