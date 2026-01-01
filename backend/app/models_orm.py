from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from app.core.database import Base
from datetime import datetime

class TransactionDB(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    source_entity = Column(String, index=True)
    target_entity = Column(String, index=True)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    transaction_type = Column(String, default="payment")
    
class AnomalyDB(Base):
    __tablename__ = "anomalies"
    
    id = Column(Integer, primary_key=True, index=True)
    anomaly_id = Column(String, unique=True, index=True)
    anomaly_type = Column(String)
    severity = Column(Float)
    description = Column(String)
    entities_involved = Column(JSON) # Store list as JSON
    evidence_data = Column(JSON)
    model_version = Column(String, index=True)
    time_slice = Column(String, index=True)
    confidence = Column(String) # Low, Medium, High
    detection_method = Column(String) # LEARNED, DETERMINISTIC
    explanation_metadata = Column(JSON) # Structured metrics
    created_at = Column(DateTime, default=datetime.utcnow)

class SnapshotDB(Base):
    __tablename__ = "snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(String, unique=True)
    data_hash = Column(String)
    node_count = Column(Integer)
    edge_count = Column(Integer)
    time_slice = Column(String, index=True)
    model_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
