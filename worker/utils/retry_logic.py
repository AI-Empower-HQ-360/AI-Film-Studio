"""
Retry utilities for worker tasks.
"""
from functools import wraps
from typing import Callable, Type, Tuple
from celery.exceptions import MaxRetriesExceededError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)


def celery_retry_on_exception(
    exceptions: Tuple[Type[Exception], ...],
    max_retries: int = 3,
    countdown: int = 60
):
    """
    Decorator for automatic Celery task retry on specific exceptions.
    
    Args:
        exceptions: Tuple of exception types to catch
        max_retries: Maximum number of retries
        countdown: Delay between retries in seconds
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except exceptions as exc:
                # Get current retry count
                retry_count = self.request.retries
                
                if retry_count >= max_retries:
                    raise MaxRetriesExceededError(
                        f"Max retries ({max_retries}) exceeded for {self.name}"
                    )
                
                # Retry with exponential backoff
                raise self.retry(
                    exc=exc,
                    countdown=countdown * (2 ** retry_count),
                    max_retries=max_retries
                )
        
        return wrapper
    return decorator


def external_api_retry(max_attempts: int = 3):
    """
    Decorator for retrying external API calls with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError))
    )
