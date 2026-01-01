import pandas as pd
import io
from fastapi import UploadFile, HTTPException
from typing import List, Tuple
from app.models import Transaction
from app.core.hashing import hash_content

async def ingest_csv(file: UploadFile) -> Tuple[List[Transaction], str]:
    """
    Reads a CSV file, validates rows against Transaction model,
    returns list of Transaction objects and a hash of the raw dataset.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed detected")

    content = await file.read()
    # Hash raw content for integrity proof
    raw_hash = hash_content(content.decode('utf-8')) # Simple string hash of raw bytes

    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")

    # Normalize column names (optional, map common names)
    # For now assume exact match or map loosely
    # Normalize and Validate
    # Support both new (source_entity) and legacy (entity_id) naming
    # Map legacy names to strict schema
    # Normalize Headers: content strip and lowercase for robust matching
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Map legacy names / potential user variations to strict schema
    # Keys must be lowercase now
    rename_map = {
        "entity_id": "source_entity", 
        "counterparty_id": "target_entity",
        "sender": "source_entity",
        "receiver": "target_entity",
        "source": "source_entity",
        "target": "target_entity",
        "value": "amount",
        "date": "timestamp",
        "time": "timestamp",
        "datetime": "timestamp",
        "txn_date": "timestamp"
    }
    df.rename(columns=rename_map, inplace=True)
    
    # Critical Structural Columns (Non-Negotiable)
    required_cols = {"source_entity", "target_entity", "amount", "timestamp"}
    missing = required_cols - set(df.columns)
    
    if missing:
        raise HTTPException(
            status_code=400, 
            detail=f"CSV Validation Failed. Missing required core columns: {', '.join(missing)}. Please refer to the schema instructions."
        )

    transactions = []
    
    # Iterate and validate
    for _, row in df.iterrows():
        try:
            tx = Transaction(
                transaction_id=str(row.get("transaction_id", f"txn_{_}")),
                source_entity=str(row["source_entity"]),
                target_entity=str(row["target_entity"]),
                amount=float(row["amount"]),
                timestamp=row["timestamp"],
                transaction_type=str(row.get("transaction_type", "TRANSFER")),
                
                # Context Data
                entity_context=str(row.get("entity_context", "global")),
                counterparty_context=str(row.get("counterparty_context", "global")),
                
                # Observational Overlay Data
                tax_type=str(row.get("tax_type", "")) if not pd.isna(row.get("tax_type")) else None,
                tax_rate=float(row.get("tax_rate", 0)) if not pd.isna(row.get("tax_rate")) else None,
                tax_amount=float(row.get("tax_amount", 0)) if not pd.isna(row.get("tax_amount")) else None,
                input_tax_credit=float(row.get("input_tax_credit", 0)) if not pd.isna(row.get("input_tax_credit")) else None,
                entity_size=str(row.get("entity_size", "")) if not pd.isna(row.get("entity_size")) else None
            )
            transactions.append(tx)
        except Exception as e:
            # In production, we might log errors and skip rows, or fail batch
            raise HTTPException(status_code=400, detail=f"Row {_} validation error: {str(e)}")

    return transactions, raw_hash
