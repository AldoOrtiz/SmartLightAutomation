from flask import Flask, render_template, request
import asyncio
import time
from utils.Bridge import Bridge
from utils.BluetoothScanner import BluetoothScanner

app = Flask(__name__)

BLE_TAG_MAC = "1E3B8B89-D2ED-5403-D2B2-03CDBE7F432B"
light_list = []  # List of all lights

def rgb_to_xy(red, green, blue):
    """ conversion of RGB colors to CIE1931 XY colors
    Formulas implemented from: https://gist.github.com/popcorn245/30afa0f98eea1c2fd34d
    """

    # gamma correction
    red = pow((red + 0.055) / (1.0 + 0.055), 2.4) if red > 0.04045 else (red / 12.92)
    green = pow((green + 0.055) / (1.0 + 0.055), 2.4) if green > 0.04045 else (green / 12.92)
    blue = pow((blue + 0.055) / (1.0 + 0.055), 2.4) if blue > 0.04045 else (blue / 12.92)


    # convert rgb to xyz
    x = red * 0.649926 + green * 0.103455 + blue * 0.197109
    y = red * 0.234327 + green * 0.743075 + blue * 0.022598
    z = green * 0.053077 + blue * 1.035763

    # convert xyz to xy
    x = x / (x + y + z)
    y = y / (x + y + z)

    return [x, y]

def sort_lights(light_list):
    """Sort lights into different groups based on the room they're in"""
    group1 = light_list[0:2]

    return group1


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/on", methods=["POST"])
def turn_on():
    global light_list
    bridge = Bridge()
    light_list = bridge.lights
    bed1 = sort_lights(light_list)
    for light in bed1:
        light.on = True
    return "",204

@app.route("/off", methods=["POST"])
def turn_off():
    global light_list
    bridge = Bridge()
    light_list = bridge.lights
    bed1 = sort_lights(light_list)
    for light in bed1:
        light.on = False
    return "",204

@app.route("/brightness/<int:level>", methods=["POST"])
def set_brightness(level):
    global light_list
    bridge = Bridge()
    light_list = bridge.lights
    bed1 = sort_lights(light_list)
    for i in range(len(bed1)):
        bridge.set_brightness(bed1[i].light_id, level)
    return "",204    


@app.route("/color/<int:r>/<int:g>/<int:b>", methods=["POST"])
def change_color(r, g, b):
    global light_list
    bridge = Bridge()
    light_list = bridge.lights
    bed1 = sort_lights(light_list)
    xy = rgb_to_xy(r, g, b)
    for i in range(len(bed1)):
        bridge.set_color(bed1[i].light_id, xy)
    return "", 204




if __name__ == '__main__':
    # check_bt_scan()
    app.run(debug=True)