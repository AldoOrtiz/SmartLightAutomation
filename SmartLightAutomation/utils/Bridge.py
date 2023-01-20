"""
Bridge class is used to represent a Hue Bridge. It is used to control the bridge and get information about it.
This class is a subclass of the Bridge class from the phue library.

The Bridge class also contains a list of Light objects representing the lights connected to the bridge.


//TODO: Lägg till config.py i gitignore
Du behöver också en fil som heter config.py som innehåller dina inloggningsuppgifter till Hue Bridge. 
Filen ska se ut så här:

BRIDGE_IP = '192.168.xxx.xxx'
USERNAME = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
"""

from phue import Bridge

class Bridge(Bridge):
    BRIDGE_IP = '192.168.xxx.xxx'
    USERNAME = "Your user name here"


    def __init__(self):
        """Initialize the Bridge object and connect to the bridge."""
        super().__init__(ip=Bridge.BRIDGE_IP, username=Bridge.USERNAME)
        print("******  Connected to bridge  ******")

    def turn_on(self, light_id):
        """Turn on the light."""
        self.set_light(light_id, 'on', True)

    def turn_off(self, light_id):
        """Turn off the light."""
        self.set_light(light_id, 'on', False)

    def set_brightness(self, light_id, brightness):
        """Set the brightness of the light."""
        self.set_light(light_id, 'bri', brightness)

    def set_color(self, light_id, color):
        """Set the color of the light."""
        self.set_light(light_id, 'xy', color)

    def set_color_temperature(self, light_id, color_temperature):
        """Set the color temperature of the light."""
        self.set_light(light_id, 'ct', color_temperature)

    def set_alert(self, light_id, alert):
        """Set the alert of the light."""
        self.set_light(light_id, 'alert', alert)

    def set_effect(self, light_id, effect):
        """Set the effect of the light."""
        self.set_light(light_id, 'effect', effect)

    def set_color_loop(self, group):  # Funktionen bör startas i en egen tråd då den är blocker
        """Set the color loop of the light."""
        TOTAL_TIME = 30  # Total tid i sekunder
        TRANSITION_TIME = 2 # Tid för varje transition i sekunder
        MAX_HUE = 65535
        hue_increment = MAX_HUE/ TOTAL_TIME
        for light in group:
            light.transitiontime = TRANSITION_TIME * 10
            light.brightness = 254
            light.on = True
            light.saturation = 254

        hue = 0
        while True:
            for light in group:
                light.hue = hue

            hue = (hue + hue_increment) % MAX_HUE

    def set_transition_time(self, light_id, transition_time):
        """Set the transition time of the light."""
        self.set_light(light_id, 'transitiontime', transition_time)

if __name__ == '__main__':
    bridge = Bridge()
    print(bridge.get_api())
    lights_list = bridge.lights
    lights_list[0].on = False