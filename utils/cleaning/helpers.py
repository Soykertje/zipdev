"""Utils to clean data."""
import re
from datetime import datetime
from typing import Union


def clean_text(text) -> str:
    """
    Clean text by removing special characters and extra spaces.
    :param text: str
    :return: str
    """
    if not text:
        return ''
    # Lowercase
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def clean_date(date) -> Union[datetime, None]:
    """
    Clean date by converting it to datetime object.
    :param date: str or datetime
    :return: Union[datetime, None]
    """
    if not date:
        return None
    if isinstance(date, str):
        return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return date


def clean_boolean(value) -> bool:
    """
    Clean boolean by converting it to boolean type.
    :param value: str or bool
    :return: bool
    """
    if isinstance(value, str):
        return value.lower() == 'true'
    return bool(value)
