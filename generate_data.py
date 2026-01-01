import csv
import random
from datetime import datetime, timedelta

ENTITIES = [f"Entity_{chr(65+i)}" for i in range(26)] # A..Z

def generate_dataset(filename="demo_dataset.csv", num_tx=100):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['transaction_id', 'entity_id', 'counterparty_id', 'amount', 'timestamp', 'transaction_type', 'tax_category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        base_time = datetime.now() - timedelta(days=30)
        
        # 1. Normal Transactions
        for i in range(num_tx):
            writer.writerow({
                'transaction_id': f'tx_{i:04d}',
                'entity_id': random.choice(ENTITIES),
                'counterparty_id': random.choice(ENTITIES),
                'amount': round(random.uniform(100, 10000), 2),
                'timestamp': (base_time + timedelta(hours=i*2)).isoformat(),
                'transaction_type': 'payment',
                'tax_category': 'service'
            })
            
        # 2. Inject Circular Loop (A->B->C->A)
        loop_entities = ['Entity_A', 'Entity_B', 'Entity_C']
        writer.writerow({'transaction_id': 'fra_01', 'entity_id': 'Entity_A', 'counterparty_id': 'Entity_B', 'amount': 50000, 'timestamp': base_time.isoformat(), 'transaction_type': 'loan', 'tax_category': 'exempt'})
        writer.writerow({'transaction_id': 'fra_02', 'entity_id': 'Entity_B', 'counterparty_id': 'Entity_C', 'amount': 49500, 'timestamp': (base_time + timedelta(hours=1)).isoformat(), 'transaction_type': 'loan', 'tax_category': 'exempt'})
        writer.writerow({'transaction_id': 'fra_03', 'entity_id': 'Entity_C', 'counterparty_id': 'Entity_A', 'amount': 49000, 'timestamp': (base_time + timedelta(hours=2)).isoformat(), 'transaction_type': 'repayment', 'tax_category': 'exempt'})

    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_dataset()
