# needed to run a local version of the AI
from highcliff.ai import AI

from highcliff.exampleactions import MonitorBodyTemperature, ChangeRoomTemperature, AuthorizeRoomTemperatureChange, \
    AlertCareProvider, LogBodyTemperatureData

# define the state of the world and the ai capabilities. when there is a central infrastructure available,
# these statements will be replaced with a url to the infrastructure
the_world_GLOBAL_VARIABLE = {"is_body_temperature_monitored": False, "is_room_temperature_comfortable": False}
capabilities_GLOBAL_VARIABLE = []


# hack together simulations of thermometers, UIs, etc
# launch the simulations
class SimulatedMessagingApp(AlertCareProvider):
    def behavior(self):
        print("Tell Francis that the room temperature will be raised because Peter is cold")
        return self.effects


SimulatedMessagingApp()


class SimulatedSmartThermometer(ChangeRoomTemperature):
    def behavior(self):
        print("Turn up the heat and make the room a bit warmer")
        return self.effects


SimulatedSmartThermometer()


class SimulatedUserInterface(AuthorizeRoomTemperatureChange):
    def behavior(self):
        print("Ask Peter if he's okay with raising the temperature in the room")
        print("Peter gave the okay to raise the room's temperature")
        return self.effects


SimulatedUserInterface()


class SimulatedDataLogger(LogBodyTemperatureData):
    def behavior(self):
        print("In the data lake, make a place to store the history of Peter's body temperature")
        return self.effects


SimulatedDataLogger()

# run the ai. when there is a central infrastructure available, this code will be run on the infrastructure
# and the following statements will not be necessary
ai_life_span_in_iterations = 3
AI(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE, ai_life_span_in_iterations)
