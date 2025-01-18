from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class DeliverBox(Behaviour):
    def __init__(self, robot, videoStream, supress_list, params):
        super().__init__(robot, videoStream, supress_list, params)

        self.speed = 2
        self.proximity_threshold = 40
        self.bay_to_aruco_relation = params.get('bay_aruco', {})


    def get_corresponding_bay(self):
        current_box_id = self.params.get("current_box_id")
        for bay, boxes in self.bay_to_aruco_relation.items():
            if current_box_id in boxes:
                return bay
        return self.params.get("default_bay")


    def take_control(self):
        return not self.supress and self.bay_in_view() and self.carrying_box() and self.distance_below_threshold()
        

    def bay_in_view(self):
        aruco = self.robot.readArucoTag()
        if aruco.id == '':
            return False
        corresponding_bay = self.get_corresponding_bay()
        return (corresponding_bay is not None) and (int(aruco.id) == corresponding_bay)


    def distance_below_threshold(self):
        return self.robot.readIRSensor(IR.FrontC) > self.proximity_threshold


    def go_straight(self):
        self.robot.moveWheels(self.speed, self.speed)

    
    def finished_delivering(self):
        return self.robot.readIRSensor(IR.FrontC) > self.stopping_threshold


    def action(self):
        print("----> control: DeliverBox")

        self.supress = False
        self.suppress_behaviors()

        while (not self.supress) and (self.distance_below_threshold()):
            self.go_straight()
            self.robot.wait(0.1)

        self.robot.stopMotors()
        self.delivered_box()
        self.unsuppress_behaviors()