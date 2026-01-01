from app.core.database import engine, Base
from app.models_orm import AnomalyDB, TransactionDB, SnapshotDB

def reset_db():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Database schema reset complete.")

if __name__ == "__main__":
    reset_db()
