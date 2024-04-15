from pathlib import Path

import umbridge as ub
from sklearn.gaussian_process.kernels import RBF, ConstantKernel

import src.surrogate.surrogate_model as surrogate_model
import src.surrogate.surrogate_control as surrogate_control
import src.surrogate.utilities as util


# ==================================================================================================
simulation_model = util.request_umbridge_server("http://localhost:4242", "forward")

surrogate_model_type = surrogate_model.SKLearnGPSurrogateModel

surrogate_model_settings = surrogate_model.SKLearnGPSettings(
    scaling_kernel=ConstantKernel(constant_value=0.5, constant_value_bounds=(1e-5, 1e5)),
    correlation_kernel=RBF(length_scale=1e6, length_scale_bounds=(1e5, 1e8)),
    data_noise=1e-6,
    num_optimizer_restarts=3,
    minimum_num_training_points=3,
    normalize_output=False,
    perform_log_transform=True,
    variance_is_relative=False,
    variance_reference=None,
    value_range_underflow_threshold=1e-6,
    log_mean_underflow_value=-1000,
    mean_underflow_value=1e-6,
    init_seed=0,
    checkpoint_load_file="results_zihua/surrogate_checkpoint_pretraining.pkl",
    checkpoint_save_path=Path("results_zihua"),
)

# --------------------------------------------------------------------------------------------------
surrogate_control_settings = surrogate_control.ControlSettings(
    name="surrogate",
    port=4243,
    minimum_num_training_points=0,
    variance_threshold=1e-3,
    update_interval_rule=lambda num_updates: num_updates+1,
    checkpoint_load_file=None,
    checkpoint_save_path=Path("results_zihua"),
    overwrite_checkpoint=False,
)

control_logger_settings = util.LoggerSettings(
    do_printing=True,
    logfile_path=Path("results_zihua/online.log"),
    write_mode="w",
)
