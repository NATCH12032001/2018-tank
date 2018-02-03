import wpilib
<<<<<<< HEAD
import wpilib.drive
from magicbot import will_reset_to


class Drive:
    """
    Handle robot drivetrain.

    All drive interaction must go through this class.
    """
    train: wpilib.drive.DifferentialDrive

    y = will_reset_to(0)
    rot = will_reset_to(0)
=======

ENCODER_ROTATION = 1023
WHEEL_DIAMETER = 7.639

class Drive:
    robot_drive = wpilib.RobotDrive
>>>>>>> fff3b74fb26ae0bb16cdf0614178ee082321e472

    def __init__(self):
        self.enabled = False

<<<<<<< HEAD
    def move(self, y: float, rot: float):
        """
        Move robot.

        :param y: Speed of motion in the y direction. [-1..1]
        :param rot: Speed of rotation. [-1..1]
        """
        self.y = y
        self.rot = rot

    def execute(self):
        """
        Handle driving.
        """
        self.train.arcadeDrive(self.y, self.rot)
=======
    def on_enable(self):
        self.y = 0
        self.rotation = 0

    # Verb functions -- these functions do NOT talk to motors directly. This
    # allows multiple callers in the loop to call our functions without
    # conflicts.

    def move(self, y, rotation):
        """
        Causes the robot to move
        :param y: The speed that the robot should drive in the Y direction. -1 is forward. [-1.0..1.0]
        :param rotation: The rate of rotation for the robot that is completely independent of the translation. 1 is rotate to the right [-1.0..1.0]
        """
        self.y = y
        self.rotation = rotation

    def execute(self):
        """Actually drive."""
        self.robot_drive.arcadeDrive(self.y, -self.rotation)

        # Prevent robot from driving by default
        self.y = 0
        self.rotation = 0
>>>>>>> fff3b74fb26ae0bb16cdf0614178ee082321e472
