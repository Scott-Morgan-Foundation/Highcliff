__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2020 appliedAIstudio"
__version__ = "0.1"

# copying the state of the world for reflection
import copy

from highcliff.actions.actions import ActionStatus

# AI, GOAP
from goap.planner import RegressivePlanner
from goap.algo.astar import PathNotFoundException

# used to create and access centralized infrastructure
from highcliff.infrastructure import LocalNetwork

# used to make AI a singleton
from highcliff.singleton import Singleton

# needed to log debug messages to the terminal window
from highcliff.logging import log_event_to_the_terminal_window


def intent_is_real(intent, reality):
    is_real = True
    for key in intent:
        try:
            if intent[key] != reality[key]:
                # there is a value in the intent not in reality
                is_real = False
        except KeyError:
            # there is a key in the intent not in reality
            is_real = False

    return is_real


@Singleton
class AI:
    _network = LocalNetwork.instance()
    _goals = None
    _capabilities = []
    _diary = []
    _debug_logging = False

    def set_debug_logging(self, debug_logging):
        self._debug_logging = debug_logging

    def network(self):
        return self._network

    def set_goals(self, goals):
        self._goals = goals

    def capabilities(self):
        return self._capabilities

    def add_capability(self, action):
        self._capabilities.append(action)

    # TODO: add code to remove a capability

    def run(self, life_span_in_iterations):
        # if the life span is specified as some positive number, stay alive for that number of iterations
        if life_span_in_iterations > 0:
            # log that the ai is running
            if self._debug_logging:
                log_event_to_the_terminal_window("Running the AI for " + str(life_span_in_iterations) + " iterations")
            # run the ai
            for iteration in range(life_span_in_iterations):
                self._run_ai()

        # if the life span is specified as -1, run forever
        else:
            # log that the ai is running
            if self._debug_logging:
                log_event_to_the_terminal_window("Running the AI indefinitely")
            # run the ai
            while True:
                self._run_ai()

    def reset(self):
        self._network.reset()
        self._goals = None
        self._diary = []
        self._capabilities = []

    def _get_world_state(self):
        # this function returns the current state of the world
        return self._network.the_world()

    def _select_goal(self, prioritized_goals):
        # work on the next highest-priority goal that has not yet been met

        # the default is to select an empty goal
        selected_goal = {}

        # go through goals in priority order
        for goal in self._goals:
            # if the condition is not in the world, add it to the world, assume it's false, pursue the goal
            if goal not in self._get_world_state():
                self._network.update_the_world({goal: False})
                selected_goal = {goal: self._goals[goal]}
                break

            # if the goal is already met (matches the condition of the world) then skip it
            if self._goals[goal] == self._get_world_state()[goal]:
                pass

            # if the goal is not met (mismatches the condition of the world) pursue it
            if self._goals[goal] != self._get_world_state()[goal]:
                selected_goal = {goal: self._goals[goal]}
                break

        return selected_goal

    def _reflect(self, goal, world_state_before, plan, action_status, world_state_after):
        diary_entry = {
            "my_goal": goal,
            "the_world_state_before": world_state_before,
            "my_plan": plan,
            "action_status": action_status,
            "the_world_state_after": world_state_after
        }
        self._diary.append(diary_entry)

    def _run_ai(self):
        # todo: go through this and get rid of unnecessary updates
        # select a single goal from the list of goals
        goal = self._select_goal(self._goals)

        # log that a goal has been selected
        if self._debug_logging:
            log_event_to_the_terminal_window("The AI has selected a goal: " + str(goal))

        # create a planner capable of achieving the selected goal
        planner = RegressivePlanner(self._get_world_state(), self.capabilities())

        # start by assuming that there is no plan, the action will have no effect and will fail
        plan = None
        action_status = ActionStatus.FAIL
        actual_effect = {}

        # take a snapshot of the current world state before taking action that may change it
        world_state_snapshot = copy.copy(self._get_world_state())

        # todo: refactor this into methods so that they are easier to read
        try:
            # make a plan
            plan = planner.find_plan(goal)

            # log that a plan has been created
            if self._debug_logging:
                log_event_to_the_terminal_window("The AI has made a plan to execute the goal")

            try:
                next_action = plan[0].action

                # execute the first act in the plan. it will affect the world and get us one step closer to the goal
                # the plan will be updated and actions executed until the goal is reached
                intended_effect = copy.copy(next_action.effects)
                next_action.act()

                # TODO: catch the error if the action is no longer available

            except IndexError:
                # if there is no viable plan, then record no intended effect
                intended_effect = {}

            # the action is a success if the altered world matches the action's intended effect
            actual_effect = copy.copy(self._get_world_state())
            action_had_intended_effect = intent_is_real(intended_effect, actual_effect)
            if action_had_intended_effect:
                action_status = ActionStatus.SUCCESS

        except PathNotFoundException:
            # no viable plan found. no action to be taken

            # log that no viable plan was found
            if self._debug_logging:
                log_event_to_the_terminal_window("The AI has found no viable plan to achieve the selected goal")

        except KeyError:
            # there are no registered actions that can satisfy the specified goal. no action to be taken

            # log that no necessary registered actions were found
            if self._debug_logging:
                log_event_to_the_terminal_window("The AI has no registered actions capable of satisfying the goal")

        # record the results of this iteration
        # todo: replace the 'after' world state with a copy
        self._reflect(copy.copy(goal), world_state_snapshot, copy.copy(plan), copy.copy(action_status), copy.copy(self._get_world_state()))

    def diary(self):
        return self._diary
