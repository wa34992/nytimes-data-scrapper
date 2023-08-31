import logging

# Generating logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('app.log', 'w', 'utf-8')
handler.setFormatter(logging.Formatter('%(process)d-%(levelname)s-%(message)s'))
logger.addHandler(handler)
