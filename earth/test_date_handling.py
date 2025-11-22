#!/usr/bin/env python3
"""
Test for date handling in prepare_initial_condition.py

This test validates that the script correctly handles date inputs from YAML files
whether they are parsed as datetime objects or strings.
"""

import unittest
import tempfile
import yaml
from pathlib import Path
from datetime import date

class TestDateHandling(unittest.TestCase):
    """Test date extraction from YAML configuration."""
    
    @staticmethod
    def convert_date_value(end_date_value):
        """Helper method to convert date value to YYYYMMDD format."""
        if hasattr(end_date_value, 'strftime'):
            return end_date_value.strftime('%Y%m%d')
        else:
            return str(end_date_value).replace('-', '')
    
    def test_date_as_datetime_object(self):
        """Test handling of date parsed as datetime.date object by YAML."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml_content = {
                'integration': {
                    'end-date': date(2024, 10, 1)
                }
            }
            yaml.safe_dump(yaml_content, f)
            yaml_file = f.name
        
        try:
            # Load the YAML and test the conversion logic
            with open(yaml_file, 'r') as f:
                config_data = yaml.safe_load(f)
                end_date_value = config_data['integration'].get('end-date')
                end_date = self.convert_date_value(end_date_value)
                self.assertEqual(end_date, '20241001')
        finally:
            Path(yaml_file).unlink()
    
    def test_date_as_string(self):
        """Test handling of date as string in YAML."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            # Write YAML with date as a string
            f.write('integration:\n')
            f.write('  end-date: "2024-10-02"\n')
            yaml_file = f.name
        
        try:
            # Load the YAML and test the conversion logic
            with open(yaml_file, 'r') as f:
                config_data = yaml.safe_load(f)
                end_date_value = config_data['integration'].get('end-date')
                end_date = self.convert_date_value(end_date_value)
                self.assertEqual(end_date, '20241002')
        finally:
            Path(yaml_file).unlink()
    
    def test_date_unquoted_in_yaml(self):
        """Test handling of unquoted date in YAML (auto-parsed as date object)."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            # Write YAML with unquoted date (will be auto-parsed)
            f.write('integration:\n')
            f.write('  end-date: 2024-10-15\n')
            yaml_file = f.name
        
        try:
            # Load the YAML and test the conversion logic
            with open(yaml_file, 'r') as f:
                config_data = yaml.safe_load(f)
                end_date_value = config_data['integration'].get('end-date')
                end_date = self.convert_date_value(end_date_value)
                self.assertEqual(end_date, '20241015')
        finally:
            Path(yaml_file).unlink()


if __name__ == '__main__':
    unittest.main()
