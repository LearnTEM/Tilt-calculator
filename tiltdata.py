import numpy as np

def theta_angle_rad(direction, z_axis, x_axis):
    y_axis = np.cross(z_axis, x_axis)
    a = np.dot(direction, x_axis)
    b = np.dot(direction, y_axis)
    theta = np.arccos(a)
    # print(a, b)
    return theta


def x_matrix(hkl: np.ndarray, uvw: np.ndarray, ab: np.ndarray):
    print(f"hkl: {hkl}")
    print(f"uvw: {uvw}")
    print(f"ab: {ab}")
    uvw_prim = np.cross(hkl, uvw)
    print(f"uvw_p: {uvw_prim}")
    x = np.zeros((3,3), dtype=float)
    x[0,:]=ab[0] * uvw - ab[1] * uvw_prim
    x[1,:]=ab[1] * uvw + ab[0] * uvw_prim
    x[2] = hkl
    return x


def matrix_A(alpha):
        A = np.array([
            [np.cos(alpha), 0, -np.sin(alpha)],
            [0, 1, 0],
            [np.sin(alpha), 0, np.cos(alpha)]
        ])
        return A

def matrix_B(beta):
    B = np.array([
        [1, 0, 0],
        [0, np.cos(beta), -np.sin(beta)],
        [0, np.sin(beta), np.cos(beta)]
    ])
    return B


def U_matrix(a, b, x):
    ab = np.matmul(a, b)
    U = np.matmul(ab.transpose(), x)
    return U


def normalize(a):
    length = np.sqrt((a * a).sum())
    assert length > 0
    return a / length


def almost_equal(a, b, threshold):
    sub = a - b
    distance = (sub*sub).sum()
    if distance < threshold:
        return True
    else:
        return False


def ab_from_matrix(AB_mat, threshold):
    alpha = np.arcsin(-AB_mat[0,2])
    beta = np.arcsin(AB_mat[2,1])
    check_matrix = np.matmul(matrix_A(alpha), matrix_B(beta))
    if not almost_equal(AB_mat, check_matrix, threshold):
        print("AB_mat:")
        print(AB_mat)
        print("check_matrix")
        print(check_matrix)
    return alpha, beta


class TiltData:
    def __init__(self) -> None:
        self.h1, self.k1, self.l1=0,0,1
        # self.hkl1 = np.array([0,0,1])
        # self.hkl2 = np.array([1,0,0])
        self.h2, self.k2, self.l2=1,0,0
        self.alpha1 = 0.0
        self.beta1 = 0.0
        self.rotate_theta = 0.0
        self.alpha2, self.beta2 = None, None
    
    
    def calculate(self) -> None:
        hkl1 = normalize(np.array([self.h1, self.k1, self.l1], dtype=float))
        hkl2 = normalize(np.array([self.h2, self.k2, self.l2], dtype=float))
        uvw = normalize(np.cross(hkl1, hkl2))

        deg2rad = lambda degree: degree * np.pi / 180
        rad2deg = lambda rad: rad * 180 / np.pi

        # print(self.rotate_theta)
        theta = deg2rad(self.rotate_theta) + theta_angle_rad(uvw, hkl1, x_axis=np.array([1,0,0]))
        ab = np.array([np.cos(theta), np.sin(theta)], dtype=float)

        x1 = x_matrix(hkl1, uvw, ab)

        # print(self.alpha1)
        alpha1 = deg2rad(float(self.alpha1))
        beta1 = deg2rad(float(self.beta1))
        a1 = matrix_A(alpha1)
        b1 = matrix_B(beta1)
        u =  U_matrix(a1, b1, x1)

        x2 = x_matrix(hkl2, uvw, ab)
        AB2 = np.matmul(x2, u.transpose())
        alpha2, beta2 = ab_from_matrix(AB2, 1e-2)
        self.alpha2 = rad2deg(alpha2)
        self.beta2 = rad2deg(beta2)
        print(x1, u)