from typing import List, Dict, Any
from app.models import Anomaly, Transaction
from app.core.context import context_manager
import networkx as nx

class TaxOverlay:
    """
    Observational Overlay Layer.
    Uses tax data (GST/VAT) to provide contextual explanation for existing structural anomalies.
    NEVER creates new anomalies or decides compliance.
    """
    
    def __init__(self):
        pass

    def apply(self, anomalies: List[Anomaly], transactions: List[Transaction]) -> List[Anomaly]:
        context = context_manager.get_active_context()
        flags = context.get("flags", {})
        
        # Build a quick lookup graph for transaction details if needed
        # (For simple demo, we iterate anomalies)
        
        tx_map = {t.transaction_id: t for t in transactions}

        for anomaly in anomalies:
            self._enhance_anomaly(anomaly, tx_map, flags)
            
        return anomalies

    def _enhance_anomaly(self, anomaly: Anomaly, tx_map: Dict[str, Transaction], flags: Dict[str, bool]):
        """
        Adds tax-specific corroboration to the anomaly explanation.
        """
        # We only really care about "circular" or "structuring" for tax overlays usually
        corroboration = []
        
        # 1. GST Overlay (India)
        if flags.get("gst_enabled"):
            # Logic: Check if ITC (Input Tax Credit) is claimed along the anomaly path
            # Proof of Concept: If involved entities have high ITC claims, mention it.
            # In a real graph, we'd trace the flow. Here we check the 'evidence' or entities.
            
            # Simulated Logic: If ANY transaction in the anomaly has ITC > 0
            has_itc = False
            for tid in anomaly.evidence_data.get("transaction_ids", []):
                tx = tx_map.get(tid)
                if tx and tx.input_tax_credit and tx.input_tax_credit > 0:
                    has_itc = True
                    break
            
            if has_itc:
                corroboration.append("ITC_FLOW_DETECTED")
                anomaly.description += " [Context: Continuous Input Tax Credit flow observed across this structure.]"
                anomaly.explanation_metadata["tax_context"] = "GST Input Credit Chain"

        # 2. VAT Overlay (EU)
        if flags.get("vat_enabled"):
            # Logic: Check for VAT Carousels (Zero-rated export + Domestic import)
            # Simulated Logic: Check if 'tax_rate' varies (0 vs 20)
            zero_rated_present = False
            standard_rated_present = False
            
            for tid in anomaly.evidence_data.get("transaction_ids", []):
                tx = tx_map.get(tid)
                if tx and tx.tax_rate is not None:
                    if tx.tax_rate == 0: zero_rated_present = True
                    if tx.tax_rate > 15: standard_rated_present = True
            
            if zero_rated_present and standard_rated_present:
                 corroboration.append("VAT_ASYMMETRY")
                 anomaly.description += " [Context: Structure involves both Zero-Rated and Standard-Rated flows, typical of VAT Carousel patterns.]"
                 anomaly.explanation_metadata["tax_context"] = "VAT Asymmetry (Carousel)"

        if corroboration:
            # We enforce the logic: Tax data INCREASES confidence or ADDS context, never decreases.
            if anomaly.confidence == "Low":
                anomaly.confidence = "Medium"
            elif anomaly.confidence == "Medium":
                anomaly.confidence = "High"
            
            anomaly.explanation_metadata["corroboration"] = corroboration
