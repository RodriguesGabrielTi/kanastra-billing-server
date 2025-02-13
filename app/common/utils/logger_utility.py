import logging
import traceback


class LoggerUtility:
    @staticmethod
    def log_info(logger: logging.Logger, message: str):
        """Logs an informational message."""
        logger.info(f"[INFO] {message}")

    @staticmethod
    def log_warning(logger: logging.Logger, message: str):
        """Logs a warning message."""
        logger.warning(f"[WARNING] {message}")

    @staticmethod
    def log_error(logger: logging.Logger, message: str, exception: Exception = None):
        """Logs an error message with optional stacktrace."""
        if exception:
            logger.error(f"[ERROR] {message}\n{traceback.format_exc()}")
        else:
            logger.error(f"[ERROR] {message}")

    @staticmethod
    def log_critical(logger: logging.Logger, message: str, exception: Exception = None):
        """Logs a critical error message with optional stacktrace."""
        if exception:
            logger.critical(f"[CRITICAL] {message}\n{traceback.format_exc()}")
        else:
            logger.critical(f"[CRITICAL] {message}")
