# Critical Lab Notifier - Main Orchestrator
# Copyright (c) 2026 Mateusz Jakubowski

import time
import logging
import yaml
import random
import os
from dotenv import load_dotenv
from src.core.database import IncidentDatabase
from src.core.notifier import VoiceNotifier

# Setup Enterprise Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
)

class CriticalResultSystem:
    def __init__(self):
        load_dotenv()
        # Load Config securely
        try:
            with open("config/settings.yaml") as f:
                self.cfg = yaml.safe_load(f)
        except Exception as e:
            logging.warning(f"Config load failed ({e}), using defaults.")
            self.cfg = {'system': {'max_retries': 3, 'loop_interval': 10, 'db_path': 'data/incidents.db'}}
        
        # Init Subsystems
        self.db = IncidentDatabase(self.cfg['system']['db_path'])
        self.notifier = VoiceNotifier()
        
        # Load Contacts (Environment Variables preferred for PII)
        self.doctor_phone = os.getenv('DOCTOR_PHONE', '+15550100001')
        self.manager_phone = os.getenv('MANAGER_PHONE', '+15550100002')

    def mock_lis_fetch(self):
        """Simulates fetching data from Lab Information System (HL7/SQL)"""
        # 10% chance to generate a critical result every loop for Demo purposes
        if random.random() > 0.90:
            return {
                "order_id": f"ORD-{random.randint(1000,9999)}",
                "value": round(random.uniform(6.5, 8.0), 1), # Critical Potassium > 6.2
                "analyte": "K"
            }
        return None

    def run(self):
        logging.info("--- 🚑 SYSTEM STARTED: Critical Result Monitor v2.0 ---")
        logging.info("--- Mode: Enterprise Logic (Singularity) ---")

        while True:
            try:
                # 1. INGESTION PHASE (Symulacja pobierania wyników)
                new_result = self.mock_lis_fetch()
                if new_result:
                    logging.warning(f"🩸 CRITICAL VALUE DETECTED: Order {new_result['order_id']} (K+ {new_result['value']})")
                    self.db.create_incident(new_result['order_id'], new_result['value'], self.doctor_phone)

                # 2. PROCESSING PHASE (Maszyna Stanów)
                pending = self.db.get_pending()
                
                for incident in pending:
                    
                    # STATE: NEW -> Call Doctor
                    if incident.status == 'NEW':
                        logging.info(f"Processing NEW Incident {incident.order_id}...")
                        if self.notifier.make_call(incident.phone, "ALERT"):
                            self.db.update_status(incident.id, 'PROCESSING', increment_retry=True)
                    
                    # STATE: PROCESSING -> Check Retries -> Escalate
                    elif incident.status == 'PROCESSING':
                        if incident.retries >= self.cfg['system']['max_retries']:
                            logging.error(f"🚨 MAX RETRIES REACHED for Order {incident.order_id}. ESCALATING!")
                            self.db.update_status(incident.id, 'ESCALATING')
                        else:
                            logging.info(f"Waiting for ACK on Order {incident.order_id} (Attempt {incident.retries})")

                    # STATE: ESCALATING -> Call Manager
                    elif incident.status == 'ESCALATING':
                        logging.warning(f"⚠️  Calling MANAGER for Order {incident.order_id}")
                        if self.notifier.make_call(self.manager_phone, "ESCALATION"):
                            self.db.update_status(incident.id, 'ESCALATED')

                # 3. SLEEP PHASE
                time.sleep(self.cfg['system']['loop_interval'])

            except KeyboardInterrupt:
                logging.info("System shutting down...")
                break
            except Exception as e:
                logging.critical(f"System Crash: {e}")
                time.sleep(5)

if __name__ == "__main__":
    app = CriticalResultSystem()
    app.run()
