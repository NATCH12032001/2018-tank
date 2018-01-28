#!/usr/bin/env python3

import magicbot
import wpilib
import wpilib.drive

from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive, lift, arm, intake
from magicbot import tunable

from robotpy_ext.common_drivers import navx, pressure_sensors
from ctre.wpi_talonsrx import WPI_TalonSRX


class Robot(magicbot.MagicRobot):
    drive = drive.Drive
    lift = lift.Lift
    arm = arm.Arm
    intake = intake.Intake

    time = tunable(0)
    plates = tunable('')
    pressure = tunable(0)

    def createObjects(self):
        """
        Initialize robot components.
        """
        # Joysticks
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)

        # Motor controllers
        self.lf_motor = WPI_TalonSRX(10)
        self.lr_motor = WPI_TalonSRX(15)
        self.rf_motor = WPI_TalonSRX(20)
        self.rr_motor = WPI_TalonSRX(25)

        # Drivetrain object
        self.train = wpilib.drive.DifferentialDrive(wpilib.SpeedControllerGroup(self.lf_motor, self.lr_motor),
                                                    wpilib.SpeedControllerGroup(self.rf_motor, self.rr_motor))

        # Lift
        self.lift_motor_a = wpilib.Victor(7)
        self.lift_motor_b = wpilib.Victor(8)
        self.lift_hold = wpilib.Solenoid(5)

        # Arm components
        self.elevator_motor = wpilib.Victor(5)
        self.forearm = wpilib.DoubleSolenoid(2, 3)
        self.hand = wpilib.DoubleSolenoid(0, 1)

        # Intake
        self.intake_arm_left = wpilib.Victor(6)
        self.intake_arm_left.setInverted(True)
        self.intake_arm_right = wpilib.Victor(9)
        self.intake_arms = wpilib.SpeedControllerGroup(self.intake_arm_left,
                                                       self.intake_arm_right)

        self.intake_wheel_left = wpilib.Spark(3)
        self.intake_wheel_left.setInverted(True)
        self.intake_wheel_right = wpilib.Spark(4)
        self.intake_wheels = wpilib.SpeedControllerGroup(self.intake_wheel_left,
                                                         self.intake_wheel_right)

        # NavX (purple board on top of the RoboRIO)
        self.navx = navx.AHRS.create_spi()

        # Utility
        self.ds = wpilib.DriverStation.getInstance()
        self.timer = wpilib.Timer()
        self.pressure_sensor = pressure_sensors.REVAnalogPressureSensor(5)

    def robotPeriodic(self):
        """
        Executed periodically regardless of mode.
        """
        self.time = int(self.timer.getMatchTime())
        self.pressure = self.pressure_sensor.pressure

    def autonomous(self):
        """
        Prepare for and start autonomous mode.
        """
        # Read data on plate colors from FMS.
        # 3.10: "The FMS provides the ALLIANCE color assigned to each PLATE to the Driver Station software. Immediately following the assignment of PLATE color prior to the start of AUTO."
        # Will fetch a string of three characters ('L' or 'R') denoting position of the current alliance's on the switches and scale, with the nearest structures first.
        # More information: http://wpilib.screenstepslive.com/s/currentCS/m/getting_started/l/826278-2018-game-data-details
        self.plates = list(self.ds.getGameSpecificMessage())

        # Call autonomous
        super().autonomous()

    def disabledInit(self):
        """
        Executed once right away when robot is disabled.
        """
        # Reset Gyro to 0
        self.navx.reset()

    def disabledPeriodic(self):
        """
        Executed periodically while robot is disabled.

        Useful for testing.
        """
        pass

    def teleopInit(self):
        """
        Executed when teleoperated mode begins.
        """
        pass

    def teleopPeriodic(self):
        """
        Executed periodically while robot is in teleoperated mode.
        """
        # Read from joysticks to move drivetrain accordingly
        self.drive.move(-self.joystick_left.getY(), self.joystick_right.getX())

        # Lift
        if self.joystick_left.getRawButton(3):
            self.lift.run()

        # Intake
        if self.joystick_right.getRawButton(1):
            self.intake.actuate()

        # Arm
        if self.joystick_left.getRawButton(3):
            self.arm.up()
        elif self.joystick_left.getRawButton(2):
            self.arm.down()

        elif self.joystick_right.getRawButton(3):
            self.arm.top()
        elif self.joystick_right.getRawButton(2):
            self.arm.bottom()


if __name__ == '__main__':
    wpilib.run(Robot)
