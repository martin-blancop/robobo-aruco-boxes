from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class PickBox(Behaviour):
    def __init__(self, robot, videoStream, supress_list, params):
        super().__init__(robot, videoStream, supress_list, params)

        self.speed = 4
        self.proximity_threshold = 60
        self.picked_box_threshold = 30


    def take_control(self):
        return not self.supress and self.distance_below_threshold()


    def distance_below_threshold(self):
        return self.robot.readIRSensor(IR.FrontC) > self.proximity_threshold


    def go_straight(self):
        self.robot.moveWheels(self.speed, self.speed)


    def picked_box(self):
        if(self.robot.readIRSensor(IR.FrontC) <= self.proximity_threshold):
            self.set_carrying_box()


    def action(self):
        print("----> control: PickBox")

        self.supress = False
        self.suppress_behaviors()

        while (not self.supress and self.distance_below_threshold()):
            self.go_straight()
            self.robot.wait(0.1)

        self.picked_box()