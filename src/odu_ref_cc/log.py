import logging

# create logger
log = logging.getLogger("odu_ref_cc")
log_level = logging.INFO
log.setLevel(log_level)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(log_level)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
log.addHandler(ch)
