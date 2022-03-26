__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2020 appliedAIstudio"
__version__ = "0.1"

# needed to continue monitoring body temperature for a given period of time
import time
from threading import Thread

# needed to get body temperature readings
from temperature_sensor import TemperatureScale, get_body_temperature

# the Highcliff actions we are going to implement
from highcliff.temperature import MonitorTemperature

# needed to connect to the remote Highcliff AI
import rpyc


'''
The body temperature monitor application depends on a connection with the a remote ai server.
This code assumes that the ai server is up and running already.
'''


class BodyTemperatureMonitor(MonitorTemperature):
    def behavior(self):
        # monitor the current body temperature
        current_body_temperature = get_body_temperature(TemperatureScale.FAHRENHEIT)

        # an adjustment is needed only if the current body temperature is outside a normal range
        normal_body_temperature_in_fahrenheit = range(97, 99)
        if current_body_temperature not in normal_body_temperature_in_fahrenheit:
            # todo: we should see these executing. instrument the ai to see actions executing
            print("the body temperature is not normal")
            self._adjustment_needed()
        else:
            print("the body temperature is fine")
            # pause before checking the body temperature again
            seconds_to_pause_before_next_checking_body_temperature = 5
            time.sleep(seconds_to_pause_before_next_checking_body_temperature)


def run_body_temperature_monitor():
    # create a connection. we assume that the ai server has been started at the specified ip address and port
    connection = rpyc.connect("localhost", 18861)
    highcliff_ai = connection.root.get_ai_instance()
    print("connected to the remote AI server")

    # run the body temperature model and register it with the highcliff ai
    BodyTemperatureMonitor(highcliff_ai)
    print("registered with the remote AI server")

    # keep the body temperature active for a period of time
    print("monitoring body temperature")
    seconds_to_spend_monitoring_body_temperature = 10
    monitor_execution_thread = Thread(target=time.sleep, args=(seconds_to_spend_monitoring_body_temperature,))
    monitor_execution_thread.start()

    # todo: unregister from the ai
    # disconnect from the ai


if __name__ == "__main__":
    run_body_temperature_monitor()
