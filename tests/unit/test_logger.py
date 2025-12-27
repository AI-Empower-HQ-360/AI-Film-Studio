"""Unit tests for logger utility"""
import logging
import pytest
from src.utils.logger import setup_logger


@pytest.mark.unit
class TestLogger:
    """Tests for logger utility"""
    
    def test_logger_setup_default(self):
        """Test logger setup with default log level"""
        logger = setup_logger("test_logger")
        
        assert logger is not None
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO
        assert len(logger.handlers) > 0
    
    def test_logger_setup_debug_level(self):
        """Test logger setup with DEBUG level"""
        logger = setup_logger("test_debug", "DEBUG")
        
        assert logger.level == logging.DEBUG
        assert logger.handlers[0].level == logging.DEBUG
    
    def test_logger_setup_warning_level(self):
        """Test logger setup with WARNING level"""
        logger = setup_logger("test_warning", "WARNING")
        
        assert logger.level == logging.WARNING
        assert logger.handlers[0].level == logging.WARNING
    
    def test_logger_setup_error_level(self):
        """Test logger setup with ERROR level"""
        logger = setup_logger("test_error", "ERROR")
        
        assert logger.level == logging.ERROR
    
    def test_logger_handler_format(self):
        """Test logger handler has correct formatter"""
        logger = setup_logger("test_format")
        
        assert len(logger.handlers) == 1
        handler = logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)
        assert handler.formatter is not None
        
        # Check format string contains expected components
        format_str = handler.formatter._fmt
        assert "%(asctime)s" in format_str
        assert "%(name)s" in format_str
        assert "%(levelname)s" in format_str
        assert "%(message)s" in format_str
    
    def test_logger_name_configuration(self):
        """Test logger name is properly configured"""
        test_names = ["module1", "module2.submodule", "app.service"]
        
        for name in test_names:
            logger = setup_logger(name)
            assert logger.name == name
    
    def test_multiple_logger_instances(self):
        """Test creating multiple logger instances"""
        logger1 = setup_logger("logger1", "INFO")
        logger2 = setup_logger("logger2", "DEBUG")
        
        assert logger1.name != logger2.name
        assert logger1.level == logging.INFO
        assert logger2.level == logging.DEBUG
    
    def test_logger_output_stream(self):
        """Test logger uses stdout as output stream"""
        import sys
        logger = setup_logger("test_stream")
        
        handler = logger.handlers[0]
        assert handler.stream == sys.stdout
