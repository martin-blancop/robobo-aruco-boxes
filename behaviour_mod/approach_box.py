from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR
from robobopy.utils.Sounds import Sounds
import cv2

class ApproachBox(Behaviour):
    def __init__(self, robot, videoStream, supress_list, params):
        super().__init__(robot, videoStream, supress_list, params)

        self.speed = 5

        self.image_width = 480
        self.image_height = 640

        self.max_camera_tilt = 105
        self.min_camera_tilt = 5
        self.camera_tilt = 90

        self.tilting_threshold = 150
        self.turning_threshold = 20
        self.aruco_size_threshold = 50

        self.bay_to_aruco_relation = params.get('bay_aruco', {})


    def getBoxes(self):
        return {box for boxes in self.bay_to_aruco_relation.values() for box in boxes}


    def take_control(self):
        return not self.supress and self.box_in_view()
        

    def box_in_view(self):
        aruco = self.robot.readArucoTag()
        if aruco.id == '':
            return False
        return int(aruco.id) in self.getBoxes()


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

            if center_x < image_center_x - self.turning_threshold and box_size < self.aruco_size_threshold and ir_measurement < 15:
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

    def tracking_box(self):
        aruco = self.robot.readArucoTag()
        if aruco.id != '':
            self.set_tracked_box(int(aruco.id))


    def action(self):
        print("----> control: ApproachBox")

        self.tracking_box()
        self.supress = False
        self.suppress_behaviors()
        
        while (not self.supress):
            cv2_image = self.videoStream.getImage()
            self.turn_towards_box()
            self.robot.wait(0.1)