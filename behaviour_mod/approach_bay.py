from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class ApproachBay(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)

        self.speed = 12

        self.image_width = 480
        self.image_height = 640

        self.max_camera_tilt = 105
        self.min_camera_tilt = 5
        self.camera_tilt = 90

        self.tilting_threshold = 150
        self.turning_threshold = 20
        self.aruco_size_threshold = 50
        self.stopping_threshold = 70

        self.bay_to_aruco_relation = params.get('bay_aruco', {})


    def get_corresponding_bay(self):
        current_box_id = self.params.get("current_box_id")
        for bay, boxes in self.bay_to_aruco_relation.items():
            if current_box_id in boxes:
                return bay
        return self.params.get("default_bay")


    def take_control(self):
        return not self.supress and self.bay_in_view() and self.carrying_box()
        

    def bay_in_view(self):
        aruco = self.robot.readArucoTag()
        if aruco.id == '':
            return False
        corresponding_bay = self.get_corresponding_bay()
        # print(f'Carrying box: {self.params.get("current_box_id")}, Corresponding bay: {corresponding_bay}, Detected Aruco ID: {aruco.id}')
        return (corresponding_bay is not None) and (int(aruco.id) == corresponding_bay)


    def turn_left(self):
        self.robot.moveWheels(self.speed / 2, self.speed)
        

    def turn_right(self):
        self.robot.moveWheels(self.speed, self.speed / 2)

    
    def go_straight(self):
        self.robot.moveWheels(self.speed, self.speed)


    def turn_towards_box(self):
        aruco = self.robot.readArucoTag()

        if aruco is not None:
            cor1 = aruco.cor1
            cor2 = aruco.cor2
            cor3 = aruco.cor3
            cor4 = aruco.cor4

            center_x = (cor1['x'] + cor2['x'] + cor3['x'] + cor4['x']) / 4
            center_y = (cor1['y'] + cor2['y'] + cor3['y'] + cor4['y']) / 4

            box_size = abs(cor2['x'] - cor1['x'])

            image_center_x = self.image_width / 2
            image_center_y = self.image_height / 2

            ir_measurement = self.robot.readIRSensor(IR.FrontC)

            # print(f'Center: {center_x}, {center_y}, Box Size: {box_size}, Box ID: {aruco.id}, Timestamp: {aruco.timestamp}, IR: {ir_measurement}')

            if ir_measurement > self.stopping_threshold:
                self.robot.stopMotors()
            elif center_x < image_center_x - self.turning_threshold and box_size < self.aruco_size_threshold and ir_measurement < 15:
                self.turn_left()
            elif center_x > image_center_x + self.turning_threshold and box_size < self.aruco_size_threshold and ir_measurement < 15:
                self.turn_right()
            else:
                self.go_straight()

            if center_y < image_center_y - self.tilting_threshold:
                if self.camera_tilt - 5 >= self.min_camera_tilt:
                    self.camera_tilt -= 5
                    self.robot.moveTiltTo(self.camera_tilt, 5)

            elif center_y > image_center_y + self.tilting_threshold:
                if self.camera_tilt + 5 <= self.max_camera_tilt:
                    self.camera_tilt += 5
                    self.robot.moveTiltTo(self.camera_tilt, 5)


    def action(self):
        print("----> control: ApproachBay")

        self.robot.movePanTo(0, 40)

        self.supress = False
        self.suppress_behaviors()
        
        while (not self.supress) and (self.bay_in_view()):
            self.turn_towards_box()
            self.robot.wait(0.1)

        self.unsuppress_behaviors()