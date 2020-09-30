
import logging
from src.main import main
from src.helper import create_logger

logger = create_logger('root','logs/root.log', logging.DEBUG, logging.WARNING)


if __name__ == "__main__":
    logger.info("Running the app")
    main()
    logger.info("Closing the app")
