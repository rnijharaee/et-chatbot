# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import requests
import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import logging
logger = logging.getLogger(__name__)

class ActionAboutLocation(Action):

    def name(self) -> Text:
        return "action_about_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.latest_message.get('text', 'Mumbai')
        logger.debug(location)
        location = ''.join(e for e in location if (e.isalnum() or e == ' '))
        location = location.split(' ')[-1]
        data = requests.get(f'https://venue-et.herokuapp.com/api/places?search={location}').json()
        text_data = []
        for key, value in data.items():
            text_data.append(f"{value[0]['name']} - {key}")
        dispatcher.utter_message(text=f'Here are some places I found for you in {location}|' + '|'.join(text_data))
        # dispatcher.utter_message(text=json.dumps(tracker.latest_message))
        return []
