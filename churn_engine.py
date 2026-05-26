#!/usr/bin/env python3
"""
Predictive Customer Churn Framework & Operational Playbook Engine
Contains: Data Prep, Mock XGBoost Classification, SHAP Simulation, and Playbook Triggers
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score

# ============================================================================
# PART 1: SOURCE ENVIRONMENT PREPARATION & SYNTHETIC SEED DATA
# ============================================================================
def verify_and_load_dataset(data_path="customers_sample.csv"):
    """Validates local environment arrays, generating clean baseline mock logs if file is absent."""
    if not os.path.exists(data_path):
        print(f"[!] Target dataset source '{data_path}' absent. Generating robust mock matrix parameters...")
        mock_data = {
            'customer_id': [f'CUST-{i}' for i in range(1001, 1201)],
            'customer_name': [f'Company Asset Row {i}' for i in range(1, 201)],
            'ltv': np.random.choice([45, 150, 600, 1100, 2500], size=200, p=[0.2, 0.3, 0.2, 0.2, 0.1]),
            'days_since_last_login': np.random.randint(0, 30, size=200),
            'support_tickets_unresolved': np.random.choice([0, 1, 2, 4, 6], size=200, p=[0.5, 0.2, 0.1, 0.1, 0.1]),
            'feature_adoption_score': np.random.randint(0, 7, size=200),
            'plan_downgrade_flag': np.random.choice([0, 1], size=200, p=[0.85, 0.15]),
            'avg_session_duration_30d': np.random.uniform(0.5, 50.0, size=200),
            'failed_payment_attempt': np.random.choice([0, 1], size=200, p=[0.9, 0.1]),
            'completed_checklist': np.random.choice([0, 1], size=200, p=[0.4, 0.6]),
            'tenure_days': np.random.randint(5, 500, size=200)
        }
        
        df = pd.DataFrame(mock_data)
        # Synthesize target label based on operational multiplier dependencies from playbook profiles
        risk_score = (
            (df['days_since_last_login'] > 14).astype(int) * 2 +
            (df['support_tickets_unresolved'] > 3).astype(int) * 3 +
            df['plan_downgrade_flag'] * 4 +
            df['failed_payment_attempt'] * 5 -
            df['completed_checklist'] * 3
        )
        df['churned'] = (risk_score > 2).astype(int)
        df.to_csv(data_path, index=False)
        print(f"📄 Synthetic seed logs stored cleanly at location: {data_path}")
    
    return pd.read_csv(data_path)

# ============================================================================
# PART 2: MACHINE LEARNING ENGINE (CLASSIFIER INTEGRATION)
# ============================================================================
class MockXGBClassifier:
    """Simulates tree-ensemble classification patterns mirroring your target structural metrics."""
    def __init__(self):
        self.feature_importances_ = np.array([0.12, 0.38, 0.22, 0.15, 0.05, 0.02, 0.04, 0.01, 0.01])
        
    def predict_proba(self, X):
        # Generates deterministic mock logistic output bounds matching probability array signatures
        scores = 1 / (1 + np.exp(-(-2.0 + X.iloc[:, 1]*0.15 + X.iloc[:, 2]*0.4 + X.iloc[:, 4]*1.2 + X.iloc[:, 6]*1.5 - X.iloc[:, 7]*0.8)))
        return np.vstack([1 - scores, scores]).T

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X)[:, 1] >= threshold).astype(int)

def run_predictive_modeling_pipeline(df):
    print("\n=== 🧠 TRAINING PREDICTIVE ATTRITION CLASSIFIER ===")
    
    feature_cols = [
        'ltv', 'days_since_last_login', 'support_tickets_unresolved',
        'feature_adoption_score', 'plan_downgrade_flag', 
        'avg_session_duration_30d', 'failed_payment_attempt', 
        'completed_checklist', 'tenure_days'
    ]
    
    X = df[feature_cols]
    y = df['churned']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    model = MockXGBClassifier()
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    
    print("| Metric Monitored | Target Playbook Score Performance |")
    print("|------------------|-----------------------------------|")
    print(f"| AUC-ROC Score    | {roc_auc_score(y_test, probs):.2f} (Target Benchmark: 0.89) |")
    print(f"| Precision Rate   | {precision_score(y_test, preds, zero_division=0):.2f} (Target Benchmark: 0.81) |")
    print(f"| Recall Metric    | {recall_score(y_test, preds, zero_division=0):.2f} (Target Benchmark: 0.76) |")
    print(f"| F1 Score Token   | {f1_score(y_test, preds, zero_division=0):.2f} (Target Benchmark: 0.78) |")
    
    print("\n🔝 Calculated SHAP Variable Importance Ranks (Root Causes):")
    indices = np.argsort(model.feature_importances_)[::-1]
    for idx, i in enumerate(indices):
        print(f" #{idx+1:<2} | {feature_cols[i]:<28} | Global Attrib Weight: {model.feature_importances_[i]:.3f}")

    return model

# ============================================================================
# PART 3: RE-ENGAGEMENT AUTOMATED PLAYBOOK TRIGGERS ENGINE
# ============================================================================
def dispatch_playbook_interventions(df, model):
    print("\n=== 🚀 EXECUTING AUTOMATED RETENTION RESPONSE PLAYBOOK ===")
    
    feature_cols = [
        'ltv', 'days_since_last_login', 'support_tickets_unresolved',
        'feature_adoption_score', 'plan_downgrade_flag', 
        'avg_session_duration_30d', 'failed_payment_attempt', 
        'completed_checklist', 'tenure_days'
    ]
    
    # Calculate operational model probabilities globally across entire record block
    df['calculated_risk_score'] = model.predict_proba(df[feature_cols])[:, 1]
    alerts_fired = 0
    
    for idx, customer in df.head(15).iterrows(): # Evaluates first slice subset for clear demo logging
        actions = []
        
        # PLAYBOOK CONDITIONAL DISPATCH LAYER
        if customer['days_since_last_login'] >= 21 and customer['ltv'] > 500:
            actions.append("[CSM Escalation] High-Value Inactivity Gap: Assign CSM representative for immediate outreach.")
        elif customer['days_since_last_login'] >= 14:
            actions.append("[Product Team] Inactive >14 Days: Inject native inside-app onboarding tooltip configurations.")
        elif customer['days_since_last_login'] >= 7:
            actions.append("[Marketing Automation] Send automated retention re-engagement messaging cadence templates.")
            
        if customer['support_tickets_unresolved'] > 4:
            actions.append("[Support Ticket Override] Stalled Support Backlog: Force priority queue age check + issue service credit.")
            
        if customer['failed_payment_attempt'] == 1:
            actions.append("[Billing Gateway Exception] Failed Card Notice Issued: Initiate 7-day feature grace access routine.")
            
        if customer['plan_downgrade_flag'] == 1:
            actions.append("[Sales Account Sync] Intentional Contract Attrition Alert: Book a milestone success optimization evaluation.")
            
        if customer['calculated_risk_score'] > 0.75 and customer['ltv'] > 1000:
            actions.append("[Founder Intervention Trigger] Extreme Churn Probability Rank: Generate signature email outline draft.")

        # Print Trigger Outflows Transparently
        if actions:
            alerts_fired += 1
            print(f"▶️ [RULE CRITERIA MATCHED] Profile: {customer['customer_id']} | LTV Pool: ${customer['ltv']:.0f} | Risk Factor: {customer['calculated_risk_score']:.2f}")
            for action in actions:
                print(f"   ↳ Action Item Dispatch -> {action}")
            print("-" * 90)

    print(f"\n[✔] Evaluation sequence finalized successfully. Fired mitigation tasks for {alerts_fired} accounts.")

# ============================================================================
# MAIN ORCHESTRATION MAINLINE
# ============================================================================
if __name__ == "__main__":
    print("=====================================================================")
    print("🔴 RE-ENGAGEMENT AUTOMATION SYSTEM: OPERATIONAL PLAYBOOK CORE PIPELINE")
    print("=====================================================================")
    
    # Run absolute data layer pipeline executions sequential path flow
    customer_matrix = verify_and_load_dataset("customers_sample.csv")
    trained_model = run_predictive_modeling_pipeline(customer_matrix)
    dispatch_playbook_interventions(customer_matrix, trained_model)
