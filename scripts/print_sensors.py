"""
A tiny example of displaying all sensor data.

Adapted from
https://github.com/pimoroni/enviroplus-python/blob/master/examples/all-in-one-enviro-mini.py
"""
import sys
import time
from subprocess import PIPE, Popen

from bme280 import bme280, bme280_i2c
from bme280.bme280 import setup
from enviroplus import gas
from ltr559 import LTR559


# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(
        ["vcgencmd", "measure_temp"], stdout=PIPE, universal_newlines=True
    )
    output, _error = process.communicate()
    return float(output[output.index("=") + 1 : output.rindex("'")])  # noqa


def set_up_bme280() -> None:
    # See this readme for how to find your magic values
    # https://github.com/kbrownlees/bme280
    bme280_i2c.set_default_i2c_address(int(0x76))
    bme280_i2c.set_default_bus(1)
    setup()


if __name__ == "__main__":
    set_up_bme280()

    # Tuning factor for compensation. Decrease this number to adjust the
    # temperature down, and increase to adjust up
    factor = 2.25

    cpu_temps = [get_cpu_temperature()] * 5

    delay = 0.5  # Debounce the proximity tap
    mode: int = 0  # The starting mode
    last_page: float = 0
    light = 1

    # Create a values dict to store the data
    variables = [
        "temperature",
        "pressure",
        "humidity",
        "light",
    ]

    ltr559 = LTR559()

    # The main loop
    try:
        while True:
            proximity = ltr559.get_proximity()

            # If the proximity crosses the threshold, toggle the mode
            if proximity > 1500 and time.time() - last_page > delay:
                mode += 1
                mode %= len(variables)
                last_page = time.time()

            # One mode for each variable
            if mode == 0:
                # variable = "temperature"
                unit = "C"
                cpu_temp = get_cpu_temperature()
                # Smooth out with some averaging to decrease jitter
                cpu_temps = cpu_temps[1:] + [cpu_temp]
                avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
                raw_temp = bme280.read_temperature()
                data = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
                print("{}: {:.1f} {}".format(variables[mode], data, unit))

            if mode == 1:
                # variable = "pressure"
                unit = "hPa"
                data = bme280.read_pressure()
                print("{}: {:.1f} {}".format(variables[mode], data, unit))

            if mode == 2:
                # variable = "humidity"
                unit = "%"
                data = bme280.read_humidity()
                print("{}: {:.1f} {}".format(variables[mode], data, unit))

            # TODO: bme280.read_adc()

            if mode == 3:
                # variable = "light"
                unit = "Lux"
                if proximity < 10:
                    data = ltr559.get_lux()
                else:
                    data = 1
                print("{}: {:.1f} {}".format(variables[mode], data, unit))

            if mode == 4:
                # variable = "oxidised"
                unit = "kO"
                data = gas.read_all()
                data = data.oxidising / 1000
                print("{}: {:.1f} {}".format(variables[mode], data, unit))

            if mode == 5:
                # variable = "reduced"
                unit = "kO"
                data = gas.read_all()
                data = data.reducing / 1000
                print("{}: {:.1f} {}".format(variables[mode], data, unit))

            if mode == 6:
                # variable = "nh3"
                unit = "kO"
                data = gas.read_all()
                data = data.nh3 / 1000
                print("{}: {:.1f} {}".format(variables[mode], data, unit))

    # Exit cleanly
    except KeyboardInterrupt:
        sys.exit(0)
