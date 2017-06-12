#!/usr/bin/env python3

import logging


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    logging.basicConfig(level=logging.DEBUG)
    logging.info("backend started")

    return

if __name__ == "__main__":
    main()
