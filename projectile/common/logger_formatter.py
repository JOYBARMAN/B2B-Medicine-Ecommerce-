"""Crete custom color formatter for logger"""

from colorlog.formatter import ColoredFormatter


class CustomFormatter(ColoredFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, log_colors=None)
        self.log_colors = {
            "DEBUG": "bold_white",
            "INFO": "bold_green",
            "WARNING": "bold_blue",
            "ERROR": "bold_red",
            "CRITICAL": "bold_red",
        }
