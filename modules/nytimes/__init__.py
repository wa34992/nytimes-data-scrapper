import logging

# Generating logs
logging.basicConfig(
    filename='app.log', encoding='utf-8', level=logging.INFO, filemode='w',
    format='%(process)d-%(levelname)s-%(message)s')

logger = logging.getLogger(__name__)
