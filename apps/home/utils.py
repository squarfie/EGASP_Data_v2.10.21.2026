from datetime import datetime

from django.utils.dateparse import parse_date

def clean_date(value):
    if not value or value.strip() in ["", "n/a", "NA", None]:
        return None
    
    value = value.strip()

    # Try Django's flexible parser first
    dt = parse_date(value)
    if dt:
        return dt

    # Try multiple fallback formats
    formats = [
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%m %d %Y",
        "%Y-%m-%d",
        "%Y/%m/%d"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass

    # If still invalid, return None instead of failing
    return None
