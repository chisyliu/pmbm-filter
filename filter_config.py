import numpy as np

from gaussian_density import GaussianDensity


class FilterConfig(object):
    def __init__(self,
                 state_dim: int,
                 measurement_dim: int,
                 prob_survival: float = 0.9,
                 prob_detection: float = 0.9,
                 poisson_birth_weight: float = np.log(5e-3),
                 poisson_birth_gating_size: float = 11.0,
                 poisson_prune_threshold: float = -3,
                 poisson_merge_threshold: float = 2.0,
                 poisson_clutter_intensity: float = 1e-4,
                 pmbm_desired_num_global_hypotheses: int = 10,
                 pmbm_prune_single_hypothesis_existence: float = 1e-3,
                 pmbm_prune_global_hypothesis_log_weight: float = -5.0):
        self.state_dim = state_dim
        self.measurement_dim = measurement_dim
        self.prob_survival = prob_survival
        self.prob_detection = prob_detection
        self.poisson_birth_weight = poisson_birth_weight
        self.poisson_birth_gating_size = poisson_birth_gating_size
        self.poisson_prune_threshold = poisson_prune_threshold
        self.poisson_merge_threshold = poisson_merge_threshold
        self.poisson_clutter_intensity = poisson_clutter_intensity
        self.pmbm_desired_num_global_hypotheses = pmbm_desired_num_global_hypotheses
        self.pmbm_prune_single_hypothesis_existence = pmbm_prune_single_hypothesis_existence
        self.pmbm_prune_global_hypothesis_log_weight = pmbm_prune_global_hypothesis_log_weight


def get_gaussian_density_NuScenes_CV() -> GaussianDensity:
    """
    Set up motion & measurement model for NuScenes, Constant Velocity
    :return:
    """
    state_dim = 6   # [x, y, yaw, vx, vy, vyaw]
    meas_dim = 3  # [x, y, yaw]
    dt = 0.5  # sampling time
    # motion model
    F = np.eye(state_dim)
    F[:3, 3:] = np.eye(3) * dt
    Q = np.diag([9.45275998e-02, 9.45620374e-02, 1.41680460e-01, 9.45275998e-02, 9.45620374e-02, 1.41680460e-01])  # of truck
    # measurement model
    H = np.concatenate((np.eye(3), np.zeros((3, 3))), axis=1)
    R = np.diag([0.23228021, 0.22229261, 1.05163481])  # of class trailer

    density = GaussianDensity(state_dim, meas_dim, F, Q, H, R)
    return density