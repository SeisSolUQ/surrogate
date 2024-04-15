import argparse
import importlib

import umbridge as ub

import src.surrogate.surrogate_control as surrogate_control


# ==================================================================================================
def process_cli_arguments():
    argParser = argparse.ArgumentParser(
        prog="surrogate.py",
        usage="python %(prog)s [options]",
        description="Run file for Umbridge surrogate",
    )

    argParser.add_argument(
        "-app",
        "--application",
        type=str,
        required=True,
        help="Application directory",
    )

    cliArgs = argParser.parse_args()
    application_dir = cliArgs.application.replace("/", ".").strip(".")

    return application_dir


# ==================================================================================================
def main():
    application_dir = process_cli_arguments()
    settings_module = f"{application_dir}.settings_control"
    settings_module = importlib.import_module(settings_module)

    surrogate_model = settings_module.surrogate_model_type(settings_module.surrogate_model_settings)
    control = surrogate_control.SurrogateControl(
        settings_module.surrogate_control_settings,
        settings_module.control_logger_settings,
        surrogate_model,
        settings_module.simulation_model,
    )
    ub.serve_models(
        [control], port=settings_module.surrogate_control_settings.port, max_workers=100
    )


if __name__ == "__main__":
    main()
