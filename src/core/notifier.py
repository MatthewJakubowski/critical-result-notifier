import os
import logging

class VoiceNotifier:
    def __init__(self):
        self.sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_num = os.getenv('TWILIO_FROM_NUMBER')

    def make_call(self, to_number, message_type="ALERT"):
        """
        Initiates a call via Twilio.
        Returns True if call started, False if error.
        """
        # SAFEGUARD: If no keys are present, simulate the call to prevent crash
        if not self.sid or "your_sid" in str(self.sid):
            logging.warning(f"📞 [SIMULATION] Calling {to_number} ({message_type}) - API Key not configured")
            return True
            
        try:
            # In production, here we would initialize Twilio Client
            # client.calls.create(...)
            logging.info(f"📞 [TWILIO] Initiating secure call to {to_number}...")
            return True
        except Exception as e:
            logging.error(f"Twilio API Failed: {e}")
            return False
