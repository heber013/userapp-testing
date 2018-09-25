import argparse
import logging.config
import os
import subprocess
import sys
import traceback
from os import environ

from behave import __main__ as behave_script
from configobj import ConfigObj

ARGS = None
CONFIG = ConfigObj(os.path.join(os.getcwd(), "config", "config.cfg"))


def main():
    __parse_arguments()
    __set_environment_variables()
    __set_proxy_configuration()
    __create_paths()
    __set_variables_to_behave()
    __run_test_cases()


def __parse_arguments():
    parser = argparse.ArgumentParser(
        description='Behave using selenium')
    parser.add_argument('-t',
                        '--tags',
                        action="append",
                        help='tags to filter tests to run',
                        required=False)
    parser.add_argument('-b',
                        '--browser',
                        default="chrome",
                        help='firefox, chrome. Default: firefox',
                        required=False)
    parser.add_argument('-g',
                        '--grid',
                        help='The remote grid url in which the tests will be executed',
                        required=False)
    parser.add_argument('-w',
                        '--wait_for',
                        help='wait for a HOST:PORT to be available before executing tests.',
                        required=False)
    parser.add_argument('--time',
                        help='Time to wait in case wait_for is specified',
                        default=15,
                        required=False)
    parser.add_argument('-o',
                        '--output_folder',
                        default=CONFIG['results']['output_dir'],
                        help='output folder where the test results will be stored under project folder',
                        required=False)
    parser.add_argument('-j',
                        '--junit',
                        action="store_true",
                        default=False,
                        help='Output JUnit-compatible reports.',
                        required=False)
    parser.add_argument('--http_proxy',
                        action="store_true",
                        default=False,
                        help='setup default http proxy (e.g. http://<proxy_url>:(proxy_port>)',
                        required=False)
    parser.add_argument('--https_proxy',
                        action="store_true",
                        default=False,
                        help='setup default https proxy (e.g. https://<proxy_url>:(proxy_port>)',
                        required=False)
    parser.add_argument('--no_proxy',
                        action="store_true",
                        default=False,
                        help='setup endpoints to be ignored by the proxy (e.g. "127.0.0.1,123.1.1.1")',
                        required=False)
    global ARGS
    ARGS = parser.parse_args()


def __set_environment_variables():
    __set_environment_variable('BROWSER', ARGS.browser)
    __set_environment_variable('GRID_URL', ARGS.grid)
    __set_tags_as_environment_variable(ARGS.tags)
    __set_environment_variable('OUTPUT', os.path.abspath(ARGS.output_folder))
    __set_environment_variable('JUNIT', ARGS.junit)
    __set_environment_variable('WEB_ADDRESS', os.environ.get('WEB_ADDRESS',
                                                             'http://localhost:5000'))


def __set_proxy_configuration():
    __set_environment_variable('http_proxy', CONFIG['proxy_solution']['http_proxy'])
    __set_environment_variable('https_proxy', CONFIG['proxy_solution']['https_proxy'])
    __set_environment_variable('no_proxy', CONFIG['proxy_solution']['no_proxy'])


def __set_environment_variable(variable, value):
    if value:
        environ[variable] = str(value)


def __set_tags_as_environment_variable(tags):
    if tags:
        for tag in tags:
            if environ.get('TAGS'):
                __set_environment_variable('TAGS', environ.get('TAGS') + ";" + tag)
            else:
                __set_environment_variable('TAGS', tag)
    else:
        environ['TAGS'] = ""


def __set_variables_to_behave():
    del sys.argv[1:]
    if environ['TAGS']:
        tags = environ['TAGS'].split(";")
        for tag in tags:
            sys.argv.append('--tags')
            sys.argv.append(tag)
    if environ.get('JUNIT'):
        sys.argv.append('--junit')
        sys.argv.append('--junit-directory')
        sys.argv.append(os.path.join(environ['OUTPUT'], 'reports'))
    sys.argv.append('--outfile')
    sys.argv.append(os.path.join(environ['OUTPUT'], 'logs', "behave.log"))


def __run_test_cases():
    try:
        if ARGS.wait_for:
            subprocess.check_call(['./wait-for-it.sh', '-t', str(ARGS.time), ARGS.wait_for])
        sys.exit(behave_script.main())
    except Exception as e:
        logging.error("Error: " + str(e))
        traceback.print_exc()


def __create_paths():
    project_paths = [environ['OUTPUT']]

    for path in project_paths:
        if not os.path.exists(path):
            os.makedirs(path)


if __name__ == '__main__':
    main()
