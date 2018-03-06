# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from yeelight import Bulb
import miio
import yaml

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

class YeelightSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(YeelightSkill, self).__init__(name="YeelightSkill")

        # Check and then monitor for credential changes
        self.settings.set_changed_callback(self.on_websettings_changed)

        # Initialize working variables used within the skill.
        self.bulb = Bulb(self.settings.get("yeelight_bulb_ip", ""))
        self.philips_lamp = miio.device(self.settings.get("philips_lamp_ip", ""), self.settings.get("philips_lamp_token", ""))
        self.vacuum_cleaner = miio.device(self.settings.get("vacuum_cleaner_ip", ""), self.settings.get("vacuum_cleaner_token", ""))

    def on_websettings_changed(self):
        self.bulb = Bulb(self.settings.get("yeelight_bulb_ip", ""))
        self.philips_lamp = miio.device(self.settings.get("philips_lamp_ip", ""), self.settings.get("philips_lamp_token", ""))
        self.vacuum_cleaner = miio.device(self.settings.get("vacuum_cleaner_ip", ""), self.settings.get("vacuum_cleaner_token", ""))


    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'
    @intent_handler(IntentBuilder("YeelightBulb").require("Switch").require("Bulb").require("State"))
    def handle_switch_yeelight_bulb(self, message):

        if message.data["State"] == "on":
            self.bulb.turn_on()
            self.speak_dialog("bulb.switch", data={"state": "on"})

        elif message.data["State"] == "off":
            self.bulb.turn_off()
            self.speak_dialog("bulb.switch", data={"state": "off"})


    @intent_handler(IntentBuilder("PhilipsLamp").require("Switch").require("Bedroom").require("Bulb").require("State"))
    def handle_switch_philips_lamp(self, message):

        if message.data["State"] == "on":
            self.philips_lamp.send('set_power', ['on'])
            self.speak_dialog("bulb.switch", data={"state": "on"})

        elif message.data["State"] == "off":
            self.philips_lamp.send('set_power', ['off'])
            self.speak_dialog("bulb.switch", data={"state": "off"})

    @intent_handler(IntentBuilder("CleanHouse").require("Clean"))
    def handle_clean_house(self, message):

        self.vacuum_cleaner.send("app_start")
        self.speak_dialog("clean.started")

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return YeelightSkill()
