
README: Creating and Using a Reactive Architecture Template for Robobo Robot

Overview
--------
This project provides a basic implementation of a reactive (subsumption) architecture for the Robobo robot. 
It demonstrates how to use threads to run multiple behaviors concurrently, ensuring modularity and adaptability in robot behavior.

File Descriptions
-----------------

1. behaviour.py:
   - A base class that inherits from `Thread`.
   - Manages threads for individual robot behaviors.
   - Includes essential methods like:
     - `take_control()`: Determines when a behavior should take control.
     - `action()`: Defines the specific actions of the behavior.
     - `run()`: Continuously monitors conditions and executes the behavior.
   - Serves as a template for creating new robot behaviors.

2. find_wall.py:
   - Implements a specific behavior (`FindWall`) to make the robot stop when it detects a nearby wall.
   - Activation criteria: The front IR sensor detects a value greater than or equal to a threshold (`front_distance`).
   - Actions:
     - Moves towards the wall until a defined goal value (`goal`) is reached.
     - Suppresses other behaviors while active.
     - Signals mission completion by setting a stop flag.

3. go_to_wall.py:
   - Implements a specific behavior (`GoToWall`) that makes the robot move forward.
   - Activation criteria: Always activates unless suppressed by a higher-priority behavior.
   - Actions:
     - Moves forward until a target IR sensor value (`goal`) is reached.
     - Stops when suppressed or the goal is achieved.

4. main.py:
   - Combines and manages the behaviors (`FindWall` and `GoToWall`) to create a complete reactive architecture.
   - Key features:
     - Connects to the Robobo robot.
     - Initializes shared parameters (`params`) for communication between behaviors.
     - Starts all behaviors as threads.
     - Monitors the mission's completion using a `stop` flag.
     - Ensures a clean exit by joining threads and disconnecting the robot.

How to Use
----------

1. Setup:
   - Ensure you have the required libraries installed (e.g., `robobopy`).
   - Place all the files in the same directory or adjust import paths as necessary.

2. Running the Example:
   - Execute `main.py` to see the robot:
     - Move forward (`GoToWall`).
     - Stop when it detects a wall (`FindWall`).

3. Creating Your Own Behaviors:
   - Use `behaviour.py` as a base class for your new behaviors.
   - Override the `take_control()` and `action()` methods to define:
     - When the behavior should activate.
     - What actions it should perform.

4. Integrating New Behaviors:
   - Import your new behavior class in `main.py`.
   - Instantiate the behavior and add it to the `threads` list.
   - Define suppression rules by passing relevant behaviors to the `supress_list`.

Example: Adding a New Behavior
------------------------------

Suppose you want to add a behavior to detect a specific color:

1. Create a new file, `find_color.py`:
   ```python
   from behaviour_mod.behaviour import Behaviour
   from robobopy.utils.BlobColor import BlobColor

   class FindColor(Behaviour):
       def __init__(self, robot, supress_list, params, color=BlobColor.RED):
           super().__init__(robot, supress_list, params)
           self.color = color

       def take_control(self):
           return self.robot.detectColor(self.color)

       def action(self):
           print("----> control: FindColor")
           self.supress = False
           for bh in self.supress_list:
               bh.supress = True
           self.robot.sayText(f"Detected {self.color}!")
           self.set_stop()
   ```

2. Update `main.py`:
   ```python
   from behaviour_mod.find_color import FindColor
   find_color_behaviour = FindColor(robobo, [go_to_wall_behaviour, find_wall_behaviour], params, BlobColor.RED)
   threads = [go_to_wall_behaviour, find_wall_behaviour, find_color_behaviour]
   ```

Notes
-----
- The order of behaviors in the `threads` list determines their priority (low to high).
- Use the `supress_list` to manage behavior dependencies and suppression.
- Always test new behaviors individually before integrating them.
