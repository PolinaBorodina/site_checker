import argparse
import logging
import os
import signal
import sys
from logging.handlers import RotatingFileHandler
from time import time, sleep

from lxml.etree import XPathEvalError
from requests_html import HTMLSession

arg_pars = argparse.ArgumentParser()
arg_pars.add_argument("-d", "--delay", default="60", type=int, help="change default delay between requests in seconds")
arg_pars.add_argument("-t", "--timeout", default="5", type=int, help="change default request timeout in seconds")
arg_pars.add_argument("-ar", "--allow_redirect", default=False, action=argparse.BooleanOptionalAction,
                      help="add -ar if you want to allow redirects")
arg_pars.add_argument("-cfg", "--config_file", default="config.txt",
                      help="set a path to a config file, default path is 'config.txt' in a project directory")
arg_pars.add_argument("-logs", "--logging_level", default="INFO", type=str,
                      help="change a level of logs to write: DEBUG, INFO, WARNING, ERROR")
arg_pars.add_argument("-lfsize", "--log_file_size", default="20971520", type=int, help="change max size of a log file")
args = arg_pars.parse_args()

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=args.logging_level,
    handlers=[RotatingFileHandler(filename='logs.txt', maxBytes=args.log_file_size, backupCount=1),
              logging.StreamHandler(stream=sys.stdout)])


def get_configs():
    try:
        config_file = open(args.config_file)
    except FileNotFoundError:
        logging.error(f'please check config file settings', exc_info=True)
        sys.exit()
    cfgs = {}

    for line in config_file:
        if line == '\n':
            continue
        conf_elms = line.split(';')
        cfgs.update({conf_elms[0].rstrip('\n'): conf_elms[1:]})

    config_file.close()

    return cfgs


def get(url):
    start_time = time()
    response_time = 0
    try:
        page = HTMLSession().get(url, timeout=args.timeout, allow_redirects=args.allow_redirect)
        response_time = f"{round((time() - start_time)*1000)} ms"
        page.raise_for_status()
    except Exception as e:
        if response_time == 0:
            response_time = f"{round((time() - start_time)*1000)} ms"
        return 'error', e, response_time

    return 'ok', page, response_time


def check_page(cfg):
    for url, elements in cfg.items():
        status, current_page, response_time = get(url)
        if status == 'error':
            logging.error(
                f"  page: {url}, there is an error during a page request: {current_page}, time: {response_time}")
            continue

        logging.info(f"   page: {url}, status: {status}, {current_page}, response time: {response_time}")
        if elements == ['\n'] or elements == ['']:
            continue

        for element in elements:
            try:
                elem = current_page.html.xpath(elements[elements.index(element)])
                if not elem:
                    logging.warning(f"page: {url}, there is no expected element with xpath = {element}".rstrip('\n'))
                else:
                    logging.debug(f"  page: {url}, element {elements.index(element)+1} is found")
            except XPathEvalError:
                continue


if __name__ == '__main__':
    print("Press Ctrl+C to stop")
    signal.signal(signal.SIGINT, lambda *_: os._exit(1))

    configs = get_configs()
    while True:
        check_page(configs)
        sleep(args.delay)
