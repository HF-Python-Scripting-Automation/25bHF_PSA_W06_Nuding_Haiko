import logging
from psa_utils.logger import get_logger

def get_aufgabe_01_logger():
    return get_logger("Aufgabe-01", filename="aufgabe-01.log", level=logging.DEBUG, clear=True)

def get_aufgabe_02_logger():
    return get_logger("Aufgabe-02", filename="aufgabe-02.log", level=logging.DEBUG, clear=True)

def get_aufgabe_03_logger():
    return get_logger("Aufgabe-02", filename="aufgabe-03.log", level=logging.DEBUG, clear=True)
