import math

class RoboticArm:
    def __init__(self, num_joints=3, link_length=100):
        self.num_joints = num_joints
        self.link_length = link_length
        self.angles = [0.0] * num_joints
        self.lengths = [100] * num_joints 

    def set_angles(self, angles):
        self.angles = angles
        return self.get_positions()

    def get_positions(self):
        x, y = 0, 0
        positions = [(x, y)]
        total_angle = 0
        for angle in self.angles:
            total_angle += math.radians(angle)
            x += self.link_length * math.cos(total_angle)
            y += self.link_length * math.sin(total_angle)
            positions.append((x, y))
        return positions
