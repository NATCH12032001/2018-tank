#!/usr/bin/env python3

import magicbot
import wpilib
import wpilib.drive

from ctre.wpi_talonsrx import WPI_TalonSRX


class TestRobot(magicbot.MagicRobot):
    def createObjects(self):
        """
        Initialize testbench components.
        """
        self.brushless = wpilib.NidecBrushless(9, 9)

        self.lf_victor = wpilib.Victor(0)
        self.lr_victor = wpilib.Victor(1)
        self.rf_victor = wpilib.Victor(2)
        self.rr_victor = wpilib.Victor(3)

        self.lf_talon = WPI_TalonSRX(5)
        self.lr_talon = WPI_TalonSRX(10)
        self.rf_talon = WPI_TalonSRX(15)
        self.rr_talon = WPI_TalonSRX(20)

        self.drive = wpilib.drive.DifferentialDrive(wpilib.SpeedControllerGroup(self.lf_victor, self.lr_victor, self.lf_talon, self.lr_talon),
                                                    wpilib.SpeedControllerGroup(self.rf_victor, self.rr_victor, self.rf_talon, self.rr_talon))

    def teleopPeriodic(self):
        """
        Spin all motors at full speed.
        """
        self.drive.arcadeDrive(1, 0)
        self.brushless.set(1)


if __name__ == '__main__':
    wpilib.run(TestRobot)
