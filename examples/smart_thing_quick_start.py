# needed to run a local version of the AI
from highcliff.ai import AI

from highcliff.actions import ActionStatus

# the Highcliff actions to be tested
from highcliff.exampleactions import MonitorBodyTemperature, AuthorizeRoomTemperatureChange, ChangeRoomTemperature

# get a reference to the ai and its network
highcliff = AI.instance()
network = highcliff.network()


# execute a single action with a single goal

# define a test body temperature monitor
class TestBodyTemperatureMonitor(MonitorBodyTemperature):
    def behavior(self):
        print("We are now monitoring body temperature")


# instantiate the test body temperature monitor
TestBodyTemperatureMonitor(highcliff)

# define the test world state and goals
network.update_the_world({})

# run a local version of Highcliff
highcliff.set_goals({"is_room_temperature_change_needed": True})
highcliff.run(life_span_in_iterations=1)