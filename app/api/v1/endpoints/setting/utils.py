"""
Settings management utilities and helper functions
"""

from typing import Dict, Any, List
import json


def validate_setting_value(value: Any, value_type: str) -> bool:
    """Validate setting value against its type"""
    type_validators = {
        "string": lambda x: isinstance(x, str),
        "number": lambda x: isinstance(x, (int, float)),
        "boolean": lambda x: isinstance(x, bool),
        "json": lambda x: isinstance(x, (dict, list)),
        "array": lambda x: isinstance(x, list)
    }
    
    validator = type_validators.get(value_type)
    return validator(value) if validator else True


def format_setting_value(value: Any, value_type: str) -> str:
    """Format setting value for storage"""
    if value_type == "json" or value_type == "array":
        return json.dumps(value)
    return str(value)


def parse_setting_value(value: str, value_type: str) -> Any:
    """Parse setting value from storage"""
    if value_type == "number":
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            return 0
    elif value_type == "boolean":
        return value.lower() in ('true', '1', 'yes', 'on')
    elif value_type == "json" or value_type == "array":
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return {} if value_type == "json" else []
    return value


def get_default_settings() -> List[Dict[str, Any]]:
    """Get default application settings"""
    return [
        {
            "settingCategory": "app_settings",
            "settingKey": "app_name",
            "settingValue": "ERP System",
            "valueType": "string",
            "isPublic": True,
            "description": "Application name"
        },
        {
            "settingCategory": "app_settings",
            "settingKey": "app_version", 
            "settingValue": "1.0.0",
            "valueType": "string",
            "isPublic": True,
            "description": "Application version"
        },
        {
            "settingCategory": "company_settings",
            "settingKey": "company_name",
            "settingValue": "Your Company Name",
            "valueType": "string",
            "isPublic": True,
            "description": "Company name"
        },
        {
            "settingCategory": "finance_settings",
            "settingKey": "default_currency",
            "settingValue": "USD",
            "valueType": "string",
            "isPublic": True,
            "description": "Default currency"
        }
    ]


def filter_public_settings(settings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter settings to only include public ones"""
    return [setting for setting in settings if setting.get("isPublic", False)]


def group_settings_by_category(settings: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group settings by category"""
    grouped = {}
    for setting in settings:
        category = setting.get("settingCategory", "general")
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(setting)
    return grouped
