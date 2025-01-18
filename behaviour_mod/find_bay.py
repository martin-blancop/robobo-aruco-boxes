from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class FindBay(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)

        self.speed = 12

        self.Kp = 0.4
        self.Ki = 0.0
        self.Kd = 0.0

        self.setpoint = 10

        self.prev_error = 0.0
        self.integral = 0.0

        self.dt = 0.1


    def take_control(self):
        return not self.supress and self.carrying_box()


    def suppress_behaviors(self):
        for bh in self.supress_list:
            bh.supress = True


    def follow_wall_pid(self):
        measurement = self.robot.readIRSensor(IR.FrontLL)

        error = self.setpoint - measurement

        self.integral += error * self.dt
        
        derivative = (error - self.prev_error) / self.dt

        output = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)

        left_speed = self.speed + output
        right_speed = self.speed - output

        self.robot.moveWheels(left_speed, right_speed)

        self.prev_error = error


    def action(self):
        print("----> control: FindBay")

        self.supress = False
        self.suppress_behaviors()
        self.robot.movePanTo(-20, 40)

        while (not self.supress):
            self.follow_wall_pid()
            self.robot.wait(0.1)

        self.robot.stopMotors()