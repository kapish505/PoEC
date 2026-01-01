import csv
import random
import datetime

def write_csv(filename, transactions):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['transaction_hash', 'source_entity', 'target_entity', 'amount', 'timestamp', 'transaction_type'])
        writer.writerows(transactions)
    print(f"Generated {filename} with {len(transactions)} transactions.")

def generate_base_traffic(num_tx, entities, start_date, duration_days):
    txs = []
    for _ in range(num_tx):
        src = random.choice(entities)
        tgt = random.choice(entities)
        while src == tgt:
            tgt = random.choice(entities)
        
        amount = round(random.uniform(10, 5000), 2)
        day_offset = random.randint(0, duration_days)
        ts = start_date + datetime.timedelta(days=day_offset, hours=random.randint(0, 23))
        
        txs.append([
            f"0x{random.getrandbits(64):016x}",
            src, tgt, amount, ts.strftime("%Y-%m-%d %H:%M:%S"), "TRANSFER"
        ])
    return txs

def generate_long_chain():
    # Scenario 1: Long 6-hop Chain hidden in noise
    start_date = datetime.datetime(2024, 5, 1)
    entities = [f"User_{i}" for i in range(1, 50)]
    
    # Noise
    transactions = generate_base_traffic(300, entities, start_date, 30)
    
    # 6-Hop Chain: Chain_A -> Chain_B -> ... -> Chain_F -> Chain_A
    chain_nodes = ["Chain_A", "Chain_B", "Chain_C", "Chain_D", "Chain_E", "Chain_F"]
    amount = 50000.00
    chain_time = start_date + datetime.timedelta(days=15)
    
    chain_txs = []
    for i in range(len(chain_nodes)):
        src = chain_nodes[i]
        tgt = chain_nodes[(i + 1) % len(chain_nodes)]
        # Add slight time delay
        ts = chain_time + datetime.timedelta(minutes=i*30) 
        chain_txs.append([
            f"0xchain{i}", src, tgt, amount, ts.strftime("%Y-%m-%d %H:%M:%S"), "TRANSFER"
        ])
        
    write_csv("demo_complex_long_chain.csv", transactions + chain_txs)

def generate_smurfing():
    # Scenario 2: Smurfing / Structuring (Fan-out -> Fan-in)
    # Laundering Node -> High Frequency -> Mules -> Consolidation Node
    start_date = datetime.datetime(2024, 6, 1)
    entities = [f"Citizen_{i}" for i in range(1, 30)]
    
    transactions = generate_base_traffic(200, entities, start_date, 30)
    
    source = "Kingpin_X"
    target = "Safe_Haven_Y"
    mules = [f"Mule_{i}" for i in range(1, 11)] # 10 mules
    
    smurf_txs = []
    total_amount = 100000
    chunk_size = total_amount / len(mules)
    
    # Phase 1: Fan Out (Kingpin -> Mules)
    ts_phase1 = start_date + datetime.timedelta(days=10)
    for i, mule in enumerate(mules):
        ts = ts_phase1 + datetime.timedelta(minutes=random.randint(1, 60))
        smurf_txs.append([
            f"0xsmurf_out_{i}", source, mule, chunk_size, ts.strftime("%Y-%m-%d %H:%M:%S"), "TRANSFER"
        ])
        
    # Phase 2: Fan In (Mules -> Safe Haven)
    ts_phase2 = start_date + datetime.timedelta(days=12) # 2 days later
    for i, mule in enumerate(mules):
        ts = ts_phase2 + datetime.timedelta(minutes=random.randint(1, 60))
        # Mules keep a small fee, say 5%
        send_amt = chunk_size * 0.95
        smurf_txs.append([
            f"0xsmurf_in_{i}", mule, target, send_amt, ts.strftime("%Y-%m-%d %H:%M:%S"), "TRANSFER"
        ])

    write_csv("demo_complex_smurfing.csv", transactions + smurf_txs)

def generate_multi_attack_mixed():
    # Scenario 3: High volume noise with multiple small attacks
    start_date = datetime.datetime(2024, 7, 1)
    entities = [f"Trader_{i}" for i in range(1, 100)]
    
    # Higher noise
    transactions = generate_base_traffic(1000, entities, start_date, 60)
    
    # Attack 1: Small Triangle (Classic Circular)
    t1 = start_date + datetime.timedelta(days=20)
    transactions.append([f"0xtri1", "Trader_1", "Trader_2", 15000, t1, "TRANSFER"])
    transactions.append([f"0xtri2", "Trader_2", "Trader_3", 15000, t1, "TRANSFER"])
    transactions.append([f"0xtri3", "Trader_3", "Trader_1", 15000, t1, "TRANSFER"])
    
    # Attack 2: Star Hub (Volume Spike)
    hub = "Pump_Admin"
    t2 = start_date + datetime.timedelta(days=40)
    for i in range(50, 65): # 15 victims
        transactions.append([
            f"0xstar{i}", f"Trader_{i}", hub, 2000, t2, "TRANSFER"
        ])
        
    write_csv("demo_complex_mixed.csv", transactions)

if __name__ == "__main__":
    generate_long_chain()
    generate_smurfing()
    generate_multi_attack_mixed()
