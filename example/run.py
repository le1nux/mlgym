import argparse
from .conv_net_blueprint import ConvNetBluePrint
from ml_gym.starter import MLGymStarter
from ml_gym.gym.jobs import AbstractGymJob


def parse_args():
    parser = argparse.ArgumentParser(description='Run a grid search on CPUs or distributed over multiple GPUs')
    parser.add_argument('--num_epochs', type=int, help='Number of epoch', default=None)
    parser.add_argument('--run_mode', choices=['TRAIN', 'EVAL'], required=True)
    parser.add_argument('--process_count', type=int, required=True, help='Max. number of processes running at a time.')
    parser.add_argument('--dashify_logging_path', type=str, required=True, help='Path to the dashify root logging directory')
    parser.add_argument('--text_logging_path', type=str, required=True, help='Path to python textual logging directory')
    parser.add_argument('--gs_config_path', type=str, required=True, help='Path to the grid search config')
    parser.add_argument('--gpus', type=int, nargs='+', help='Indices of GPUs to distribute the GS over', default=None)
    parser.add_argument('--log_std_to_file', default=False, action="store_true", help='Flag for forwarding std output to file')

    args = parser.parse_args()
    num_epochs = args.num_epochs
    run_mode = args.run_mode
    dashify_logging_path = args.dashify_logging_path
    gs_config_path = args.gs_config_path
    process_count = args.process_count
    gpus = args.gpus
    text_logging_path = args.text_logging_path
    log_std_to_file = args.log_std_to_file
    return num_epochs, run_mode, dashify_logging_path, text_logging_path, gs_config_path, process_count, gpus, log_std_to_file


if __name__ == '__main__':
    num_epochs, run_mode, dashify_logging_path, text_logging_path, gs_config_path, process_count, gpus, log_std_to_file = parse_args()
    starter = MLGymStarter(blue_print_class=ConvNetBluePrint,
                           run_mode=AbstractGymJob.Mode[run_mode],
                           dashify_logging_path=dashify_logging_path,
                           text_logging_path=text_logging_path,
                           process_count=process_count,
                           gpus=gpus,
                           log_std_to_file=log_std_to_file)
    starter.start()
