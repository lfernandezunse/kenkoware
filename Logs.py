import logging
from Resources import reportsFile

funcNominal = True

logging.basicConfig(filename=reportsFile, level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Funcion de logs
def autolog(message, exception=None):
    global funcNominal
    import inspect, logging
    func = inspect.currentframe().f_back.f_code
    logging.info(" %s: %s in %s:%i" % (
        message,
        func.co_name,
        func.co_filename,
        func.co_firstlineno
    ))
    if exception:
        funcNominal = False
        logging.info(" %s: %s in %s in %s:%i" % (
            message,
            func.co_name,
            exception,
            func.co_filename,
            func.co_firstlineno
        ))

