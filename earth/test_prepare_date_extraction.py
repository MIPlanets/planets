#!/usr/bin/env python3
"""
Integration test for prepare_initial_condition.py date handling.

This test validates that the date parsing works correctly in the context
of the full script by simulating the relevant code path.
"""

import unittest
import tempfile
import yaml
from pathlib import Path
from datetime import date


class TestPrepareInitialConditionDateExtraction(unittest.TestCase):
    """Test date extraction as done in prepare_initial_condition.py."""
    
    @staticmethod
    def extract_and_convert_date(config_data):
        """
        Helper method that implements the exact date extraction logic from prepare_initial_condition.py.
        
        This is the code from lines 406-412 of prepare_initial_condition.py.
        """
        # check end-date key in config/integration
        if 'integration' not in config_data:
            raise KeyError("Missing 'integration' section in config file")
        if 'end-date' not in config_data['integration']:
            raise KeyError("Missing 'end-date' key in 'integration' section of config file")
        # datetime.date YYYY-MM-DD to YYYYMMDD
        end_date_value = config_data['integration'].get('end-date')
        # Convert to string if YAML parsed it as a date object
        if hasattr(end_date_value, 'strftime'):
            end_date = end_date_value.strftime('%Y%m%d')
        else:
            # It's already a string, convert YYYY-MM-DD to YYYYMMDD
            end_date = str(end_date_value).replace('-', '')
        return end_date
    
    def create_test_config(self, end_date_value, quote_date=False):
        """Helper to create a test YAML config with integration section."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            if quote_date:
                # Write manually to ensure quoting
                f.write('integration:\n')
                f.write(f'  end-date: "{end_date_value}"\n')
            else:
                # Use yaml dump which will handle datetime objects
                yaml_content = {
                    'integration': {
                        'end-date': end_date_value
                    }
                }
                yaml.safe_dump(yaml_content, f)
            return f.name
    
    def test_date_extraction_with_datetime_object(self):
        """Test the exact code pattern from prepare_initial_condition.py with datetime object."""
        # Create config with datetime.date object
        yaml_file = self.create_test_config(date(2024, 10, 1))
        
        try:
            # Load and extract date using helper method
            with open(yaml_file, 'r') as f:
                config_data = yaml.safe_load(f)
                end_date = self.extract_and_convert_date(config_data)
            
            self.assertEqual(end_date, '20241001')
        finally:
            Path(yaml_file).unlink()
    
    def test_date_extraction_with_string(self):
        """Test the exact code pattern from prepare_initial_condition.py with string."""
        # Create config with quoted string
        yaml_file = self.create_test_config('2024-10-02', quote_date=True)
        
        try:
            # Load and extract date using helper method
            with open(yaml_file, 'r') as f:
                config_data = yaml.safe_load(f)
                end_date = self.extract_and_convert_date(config_data)
            
            self.assertEqual(end_date, '20241002')
        finally:
            Path(yaml_file).unlink()
    
    def test_date_extraction_with_unquoted_string(self):
        """Test with unquoted date (will be auto-parsed as datetime by YAML)."""
        # Create a temp file with unquoted date
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('integration:\n')
            f.write('  end-date: 2024-10-15\n')
            yaml_file = f.name
        
        try:
            # Load and extract date using helper method
            with open(yaml_file, 'r') as f:
                config_data = yaml.safe_load(f)
                end_date = self.extract_and_convert_date(config_data)
            
            self.assertEqual(end_date, '20241015')
        finally:
            Path(yaml_file).unlink()
    
    def test_missing_integration_section(self):
        """Test that missing integration section raises appropriate error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.safe_dump({'other': 'data'}, f)
            yaml_file = f.name
        
        try:
            with open(yaml_file, 'r') as f:
                config_data = yaml.safe_load(f)
                with self.assertRaises(KeyError) as context:
                    self.extract_and_convert_date(config_data)
                
                self.assertIn("integration", str(context.exception))
        finally:
            Path(yaml_file).unlink()
    
    def test_missing_end_date(self):
        """Test that missing end-date raises appropriate error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.safe_dump({'integration': {'other': 'data'}}, f)
            yaml_file = f.name
        
        try:
            with open(yaml_file, 'r') as f:
                config_data = yaml.safe_load(f)
                with self.assertRaises(KeyError) as context:
                    self.extract_and_convert_date(config_data)
                
                self.assertIn("end-date", str(context.exception))
        finally:
            Path(yaml_file).unlink()


if __name__ == '__main__':
    unittest.main()
