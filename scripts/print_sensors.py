"""
A tiny example of displaying all sensor data.

Adapted from
https://github.com/pimoroni/enviroplus-python/blob/master/examples/all-in-one-enviro-mini.py
"""
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from subprocess import PIPE, Popen

from bme280 import bme280, bme280_i2c
from bme280.bme280 import setup
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


@dataclass
class Measurements:
    """A single mesaurement."""
    timestamp: datetime
    cpu_temperature: float  # unit: Celsius
    sensor_temperature: float  # unit: Celsius
    pressure: float  # unit: hPa (=100Pa)
    relative_humidity: float  # unit: %
    light: float  # unit: lumens
    proximity: float  # unit: ??


if __name__ == "__main__":
    set_up_bme280()
    ltr559 = LTR559()
    sampling_rate_hz = 1.

    # The main loop
    try:
        while True:
            st = time.time()
            measurements = Measurements(
                timestamp=datetime.utcnow(),
                cpu_temperature=get_cpu_temperature(),
                sensor_temperature=bme280.read_temperature(),
                pressure=bme280.read_pressure(),
                relative_humidity=bme280.read_humidity(),
                light=ltr559.get_lux(),
                proximity=ltr559.get_proximity(),
            )
            print(measurements)
            et = time.time()
            time_to_take_sample = et - st
            if time_to_take_sample < 1/sampling_rate_hz:
                time.sleep(1/sampling_rate_hz - time_to_take_sample)

    # Exit cleanly
    except KeyboardInterrupt:
        sys.exit(0)
