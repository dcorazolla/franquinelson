from src.util.logger import Logger
import logging

def test_logger_methods():
    logger = Logger()
    logger.debug("Debug message %s", 1)
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")


def test_logger_com_handler_existente(monkeypatch):
    fake_logger = logging.getLogger("fake")
    fake_logger.addHandler(logging.StreamHandler())

    # Simula uma stack com dois frames
    class FakeFrame:
        frame = type("Frame", (), {"f_locals": {"self": object()}})()

    monkeypatch.setattr("inspect.stack", lambda: [None, FakeFrame()])
    monkeypatch.setattr("logging.getLogger", lambda *args, **kwargs: fake_logger)

    Logger()
