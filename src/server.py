# Webhook Listener for Twilio Callbacks
# Copyright (c) 2026 Mateusz Jakubowski

from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.post("/voice/twiml/{incident_id}")
async def serve_twiml(incident_id: int):
    """
    Twilio hits this endpoint when the call is answered.
    We return XML (TwiML) instructing the robot what to speak.
    """
    response = VoiceResponse()
    gather = response.gather(num_digits=1, action=f"/voice/gather/{incident_id}", method='POST')
    
    gather.say("This is the Critical Result Notifier.", voice='alice')
    gather.say("We have a panic value report for your patient.", voice='alice')
    gather.say("Press 1 to acknowledge receipt.", voice='alice')
    
    response.say("We did not receive any input. Goodbye.", voice='alice')
    return Response(content=str(response), media_type="application/xml")

@app.post("/voice/gather/{incident_id}")
async def handle_keypress(incident_id: int, Digits: str = Form(...)):
    """
    Twilio hits this when the doctor presses a button.
    """
    response = VoiceResponse()
    
    if Digits == '1':
        logging.info(f"✅ DOCTOR ACKNOWLEDGED INCIDENT {incident_id}")
        # Here we would update the DB status to 'ACKNOWLEDGED'
        # db.update_status(incident_id, 'ACKNOWLEDGED')
        response.say("Thank you. The incident is now closed.", voice='alice')
    else:
        response.say("Invalid input.", voice='alice')
        
    return Response(content=str(response), media_type="application/xml")
