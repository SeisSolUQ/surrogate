import argparse
import importlib
import time

import src.surrogate.test_client as test_client


# ==================================================================================================
def process_cli_arguments():
    argParser = argparse.ArgumentParser(
        prog="run_testclient.py",
        usage="python %(prog)s [options]",
        description="Run file for surrogate test client",
    )

    argParser.add_argument(
        "-app",
        "--application",
        type=str,
        required=True,
        help="Application directory",
    )

    argParser.add_argument(
        "-t",
        "--sleeptime",
        type=float,
        required=False,
        default=1,
        help="Artificial sleep time to allow for data pickling",
    )

    cliArgs = argParser.parse_args()
    application_dir = cliArgs.application.replace("/", ".").strip(".")
    sleep_time = cliArgs.sleeptime

    return application_dir, sleep_time


# ==================================================================================================
def main():
    application_dir, sleep_time = process_cli_arguments()
    settings_module = f"{application_dir}.settings"
    settings = importlib.import_module(settings_module)

    client = test_client.TestClient(settings.test_client_settings)
    print("Run test client...")
    client.run()
    time.sleep(sleep_time)


if __name__ == "__main__":
    main()
