from ..cores import paths,get_logger,setup_logger

setup_logger()
log = get_logger("test")

log.info("test log")

log.debug(paths.logs) 
log.info(paths.logs) 
log.warning(paths.logs) 
log.critical(paths.logs) 
log.error(paths.logs) 

# uv run -m Backend.src.ztests.env_log