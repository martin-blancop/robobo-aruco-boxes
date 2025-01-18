from robobopy.Robobo import Robobo
from robobopy_videostream.RoboboVideo import RoboboVideo

from behaviour_mod.find_box import FindBoxes
from behaviour_mod.approach_box import ApproachBox
from behaviour_mod.pick_box import PickBox
from behaviour_mod.find_bay import FindBay
from behaviour_mod.approach_bay import ApproachBay
from behaviour_mod.deliver_box import DeliverBox

import time

def main():
    robobo = Robobo("localhost")
    robobo.connect()
    robobo.moveTiltTo(90,5)

    videoStream = RoboboVideo("localhost")  
    videoStream.connect() 
    robobo.startStream()

    params = {
        "stop": False,
        "bay_aruco": {
            3: {2, 6},
            8: {1, 4, 7},
            9: {5}
        },
        "default_bay": 16,
        "current_box_id": None,
        "carrying_box": False,
        "delivered_boxes": set()
    }

    robobo.startArUcoTagDetection()
    find_boxes_behaviour = FindBoxes(robobo, videoStream, [], params)
    approach_box_behaviour = ApproachBox(robobo, videoStream, [find_boxes_behaviour], params)
    pick_box_behaviour = PickBox(robobo, videoStream, [find_boxes_behaviour, approach_box_behaviour], params)
    find_bay_behaviour = FindBay(robobo, videoStream, [find_boxes_behaviour, approach_box_behaviour, pick_box_behaviour], params)
    approach_bay_behaviour = ApproachBay(robobo, videoStream, [find_boxes_behaviour, approach_box_behaviour, pick_box_behaviour, find_bay_behaviour], params)
    deliver_box_behaviour = DeliverBox(robobo, videoStream, [find_boxes_behaviour, approach_box_behaviour, pick_box_behaviour, find_bay_behaviour, approach_bay_behaviour], params)

    threads = [find_boxes_behaviour, approach_box_behaviour, pick_box_behaviour, find_bay_behaviour, approach_bay_behaviour, deliver_box_behaviour]

    find_boxes_behaviour.start()  
    approach_box_behaviour.start() 
    pick_box_behaviour.start()
    find_bay_behaviour.start()
    approach_bay_behaviour.start()
    deliver_box_behaviour.start()

    while not params["stop"]:
        time.sleep(0.1)

    for thread in threads:
        thread.join()

    print(f'params: {params}')
    robobo.disconnect()

if __name__ == "__main__":
    main()
