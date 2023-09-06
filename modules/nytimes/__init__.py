import logging
from RPA import FileSystem


# Generating output and pictures directories and app.log file
file_sys = FileSystem.FileSystem()
dir_exist = FileSystem.Path('output').is_dir()
if dir_exist:
    FileSystem.FileSystem().remove_directory('output', True)
FileSystem.Path('output/pictures').mkdir(parents=True, exist_ok=True)
file_sys.create_file("output/app.log")

# Generating logs
logger = logging.getLogger(__name__)
logger.info("Directories and app.log file created...")
logger.setLevel(logging.INFO)
handler = logging.FileHandler('output/app.log', 'w', 'utf-8')
handler.setFormatter(logging.Formatter('%(process)d-%(levelname)s-%(message)s'))
logger.addHandler(handler)
