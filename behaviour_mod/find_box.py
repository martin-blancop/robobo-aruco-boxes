from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class FindBoxes(Behaviour):
    def __init__(self, robot, videoStream, supress_list, params):
        super().__init__(robot, videoStream, supress_list, params)

        self.speed = 8


    def take_control(self):
        return not self.supress


    def turn(self):
        self.robot.moveWheels(self.speed, self.speed/2)


    def action(self):
        print("----> control: FindBox")
        self.supress = False

        while (not self.supress):
            self.turn()
            self.robot.wait(0.1)

        self.robot.stopMotors()