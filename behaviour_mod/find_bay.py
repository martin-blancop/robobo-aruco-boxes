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


    def follow_wall(self):
        ir_measurement_c = self.robot.readIRSensor(IR.FrontC)
        ir_measurement_ll = self.robot.readIRSensor(IR.FrontLL)

        # print(f'ir measumernts RR: {ir_measurement_rr}, R: {ir_measurement_r}, C: {ir_measurement_c}, L: {ir_measurement_l}, LL: {ir_measurement_ll}')

        if ir_measurement_ll > 10 or ir_measurement_c > 10:
            self.go_right()
        else:
            self.go_left()


    def go_right(self):
        self.robot.moveWheels(self.speed/2, self.speed)


    def go_left(self):
        self.robot.moveWheels(self.speed, self.speed/2)


    def action(self):
        print("----> control: FindBay")

        self.supress = False
        self.suppress_behaviors()
        self.robot.movePanTo(-20, 40)

        while (not self.supress):
            self.follow_wall()
            self.robot.wait(0.1)

        self.robot.stopMotors()