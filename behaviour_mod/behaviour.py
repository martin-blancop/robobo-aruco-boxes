#
# Class that inherits from Thread and manages the threads for behaviors.
# It ensures the architecture operates correctly.
#

from threading import Thread
import time

class Behaviour(Thread):
    def __init__(self, robot, supress_list, params, **kwargs):
        # Initialize the Behavior class, inheriting from Thread
        super().__init__(**kwargs)
        self.robot = robot  # Reference to the robot object
        self.__supress = False  # Internal flag for suppression
        self.supress_list = supress_list  # List of behaviors this one can suppress
        self.params = params  # Shared parameters (e.g., mission control)

    # Method to determine if the behavior should take control
    # This should be implemented in subclasses
    def take_control(self):
        pass

    # Method defining the behavior's actions
    # This should be implemented in subclasses
    def action(self):
        pass

    # Main thread execution method
    # Continuously checks if the mission is complete or if the behavior
    # should take control, and performs the associated actions
    def run(self):
        while not self.params["stop"]:  # Loop until the mission is marked as complete
            # Wait until this behavior takes control or the mission ends
            while not self.take_control() and not self.params["stop"]:
                time.sleep(0.01)  # Small delay to reduce CPU usage
            if not self.params["stop"]:  # Perform the action if the mission is still ongoing
                self.action()

    # Property to get the suppression state
    @property
    def supress(self):
        return self.__supress

    # Property setter to update the suppression state
    @supress.setter
    def supress(self, state):
        self.__supress = state
    
    def suppress_behaviors(self):
        for bh in self.supress_list:
            bh.supress = True

    def unsuppress_behaviors(self):
        for bh in self.supress_list:
            bh.supress = False

    # Method to signal that the mission should stop
    def set_stop(self):
        self.params["stop"] = True

    # Method to check if the mission is stopped
    def stopped(self):
        return self.params["stop"]
    
    def delivered_box(self):
        print(f"----> event: Delivered box {self.get_current_box()}")
        self.params["delivered_boxes"].add(self.get_current_box())
        self.params["current_box_id"] = None
        self.params["carrying_box"] = False
    
    def set_tracked_box(self, box_id):
        print(f"----> event: Tracking box {box_id}")
        self.params["current_box_id"] = box_id

    def get_current_box(self):
        return self.params.get("current_box_id", None)
    
    def set_carrying_box(self):
        print(f"----> event: Picked box {self.get_current_box()}")
        self.params["carrying_box"] = True

    def carrying_box(self):
        return self.params.get("carrying_box")

