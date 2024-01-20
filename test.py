import unittest
from tiltdata import theta_angle_rad, np

class Test(unittest.TestCase):
    
    def test_theta_angle_rad(self):
        direction1 = np.array([0,1,0])
        direction2 = np.array([1,0,0])
        direction3 = np.array([-1,0,0])
        z_axis1 = np.array([0,0,1])
        x_axis1 = np.array([1,0,0])
        self.assertTrue(theta_angle_rad(direction1, z_axis1, x_axis1) == np.pi/2)
        self.assertTrue(theta_angle_rad(direction2, z_axis1, x_axis1) == 0)
        self.assertTrue(theta_angle_rad(direction3, z_axis1, x_axis1) == np.pi)


if __name__ == "__main__":
    unittest.main()