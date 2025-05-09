import numpy as np
from lib.calcJacobian import calcJacobian


def IK_velocity(q_in, v_in, omega_in):
    """
    :param q_in: 1 x 7 vector corresponding to the robot's current configuration.
    :param v_in: The desired linear velocity in the world frame. If any element is
    Nan, then that velocity can be anything
    :param omega_in: The desired angular velocity in the world frame. If any
    element is Nan, then that velocity is unconstrained i.e. it can be anything
    :return:
    dq - 1 x 7 vector corresponding to the joint velocities. If v_in and omega_in
         are infeasible, then dq should minimize the least squares error. If v_in
         and omega_in have multiple solutions, then you should select the solution
         that minimizes the l2 norm of dq
    """

    ## STUDENT CODE GOES HERE

    dq = np.zeros((1, 7))

    v_in = v_in.reshape((3, 1))
    omega_in = omega_in.reshape((3, 1))

    v_mat = np.append(v_in, omega_in)
    to_remove = ~np.isnan(v_mat)
    jacobian = calcJacobian(q_in)
    v_mat_no_NaN = v_mat[to_remove]
    jacobian_no_NaN = jacobian[to_remove]
    
    dq = np.linalg.lstsq(jacobian_no_NaN, v_mat_no_NaN, rcond=None)[0]

    return dq


if __name__ == "__main__":
     q = np.array([0, 0, 0, -np.pi / 2, 0, np.pi / 2, np.pi / 4])
     v_in = np.array([1, 1, 1])
     omega_in = np.array([2, 1, np.nan])
     print(np.round(IK_velocity(q, v_in, omega_in), 3))