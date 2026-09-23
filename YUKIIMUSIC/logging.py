# Copyright (c) 2025 @SUDEEPBOTS <HellfireDevs>
# Location: delhi,noida
#
# All rights reserved.
#
# This code is the intellectual SUDEEPBOTS.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: sudeepgithub@gmail.com

import YUKIIMUSIC.yuki_guard
import logging
import sys
import threading

LOG_FORMAT = "[%(asctime)s - %(levelname)s] - %(name)s - %(message)s"
DATE_FORMAT = "%d-%b-%y %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.FileHandler("log.txt", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
    force=True,
)

# Keep framework logs visible in GitHub Actions. Previously these were
# intentionally suppressed at ERROR, which hid useful runtime diagnostics.
for logger_name in (
    "httpx",
    "pyrogram",
    "pytgcalls",
    "pytgcalls_wrapper",
    "ntgcalls",
    "asyncio",
):
    logging.getLogger(logger_name).setLevel(logging.INFO)


def _uncaught_exception(exc_type, exc_value, exc_traceback):
    if exc_type is KeyboardInterrupt:
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.getLogger("YUKI.UNCAUGHT").error(
        "UNCAUGHT EXCEPTION: %s: %s",
        exc_type.__name__,
        exc_value,
        exc_info=(exc_type, exc_value, exc_traceback),
    )


def _thread_exception(args):
    logging.getLogger("YUKI.THREAD").error(
        "UNCAUGHT THREAD EXCEPTION in %s: %s: %s",
        args.thread.name if args.thread else "unknown",
        args.exc_type.__name__,
        args.exc_value,
        exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
    )


sys.excepthook = _uncaught_exception
if hasattr(threading, "excepthook"):
    threading.excepthook = _thread_exception


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
