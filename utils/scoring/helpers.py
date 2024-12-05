import re
from datetime import datetime
from dateutil import parser


def extract_years_of_experience(experiences_text):
    """
    Extracts total years of experience from the experiences text,
    taking into account overlapping periods.

    Args:
        experiences_text (str): The experiences text from a candidate.

    Returns:
        float: Total years of experience.
    """
    experiences = experiences_text.split('|')
    periods = []
    for exp in experiences:
        # Find dates in the experience string
        dates = re.findall(r'\((.*?)\)', exp)
        if dates:
            date_range = dates[0]
            start_date_str, end_date_str = parse_date_range(date_range)
            if start_date_str and end_date_str:
                try:
                    start_date = parser.parse(start_date_str)
                    if end_date_str.lower() in ['n/a', 'present', '']:
                        end_date = datetime.now()
                    else:
                        end_date = parser.parse(end_date_str)
                    # Ensure start_date is before end_date
                    if start_date > end_date:
                        start_date, end_date = end_date, start_date
                    periods.append((start_date, end_date))
                except Exception as e:
                    # Skip invalid date formats
                    continue
    # Merge overlapping periods
    merged_periods = merge_periods(periods)
    # Calculate total duration
    total_days = sum((end - start).days for start, end in merged_periods)
    total_years = total_days / 365.25  # Approximate number of days in a year
    return round(total_years, 2)


def parse_date_range(date_range):
    """
    Parses a date range string and returns start and end dates.

    Args:
        date_range (str): A string like 'Jan 2010 to Dec 2012'

    Returns:
        tuple: (start_date_str, end_date_str)
    """
    date_range = date_range.lower()
    # Handle different date formats
    patterns = [
        r'(\w+ \d{4}) to (\w+ \d{4}|n/a|present|)',
        r'(\w+ \d{4})-(\w+ \d{4}|n/a|present|)',
        r'(\w+ \d{4}) (\w+ \d{4}|n/a|present|)',
    ]
    for pattern in patterns:
        match = re.match(pattern, date_range)
        if match:
            return match.group(1), match.group(2)
    return None, None


def merge_periods(periods):
    """
    Merges overlapping and contiguous date periods.

    Args:
        periods (list): List of tuples (start_date, end_date)

    Returns:
        list: Merged list of tuples (start_date, end_date)
    """
    if not periods:
        return []
    # Sort periods by start date
    periods.sort(key=lambda x: x[0])
    merged = [periods[0]]
    for current in periods[1:]:
        last = merged[-1]
        # If current period overlaps or is contiguous with the last, merge them
        if current[0] <= last[1]:
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)
    return merged


def map_education_level(educations_text):
    """
    Maps education levels to numerical values.

    Args:
        educations_text (str): The educations text from a candidate.

    Returns:
        int: Education level score.
    """
    education_levels = {
        'phd': 3,
        'doctorate': 3,
        'master': 2,
        'bachelor': 1,
        'degree': 1,
        'associate': 0.5
    }
    education_score = 0
    for level, score in education_levels.items():
        if level in educations_text:
            education_score += education_levels[score]
    return education_score

