from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class FindBay(Behaviour):
    def __init__(self, robot, videoStream, supress_list, params):
        super().__init__(robot, videoStream, supress_list, params)

        self.speed = 8


    def take_control(self):
        return not self.supress and self.carrying_box()


    def suppress_behaviors(self):
        for bh in self.supress_list:
            bh.supress = True


    def turn(self):
        self.robot.moveWheels(self.speed/2, self.speed)


    def action(self):
        print("----> control: FindBay")

        self.supress = False
        self.suppress_behaviors()

        while (not self.supress):
            self.turn()
            self.robot.wait(0.1)

        self.robot.stopMotors()