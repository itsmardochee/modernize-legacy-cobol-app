import pytest
from decimal import Decimal
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import DataProgram


class TestDataProgram:
    """Unit tests for DataProgram - TC_DATA_001, TC_DATA_002, TC_DATA_003"""
    
    @pytest.fixture
    def data_program(self):
        """Create DataProgram instance"""
        return DataProgram()
    
    @pytest.mark.unit
    def test_initialization(self):
        """Test DataProgram initialization - STORAGE-BALANCE VALUE 1000.00"""
        dp = DataProgram()
        assert dp.storage_balance == Decimal('1000.00')
        assert dp.operation_type == ""
    
    @pytest.mark.unit
    def test_read_operation_tc_data_001(self, data_program):
        """TC_DATA_001: READ operation - STORAGE-BALANCE copied to BALANCE"""
        # Test initial read
        result = data_program.execute_operation('read', Decimal('0.00'))
        assert result == Decimal('1000.00')
        assert data_program.operation_type == 'read'
    
    @pytest.mark.unit
    def test_write_operation_tc_data_002(self, data_program):
        """TC_DATA_002: WRITE operation - STORAGE-BALANCE updated with new value"""
        new_balance = Decimal('1250.75')
        result = data_program.execute_operation('write', new_balance)
        
        assert result == Decimal('1250.75')
        assert data_program.storage_balance == Decimal('1250.75')
        assert data_program.operation_type == 'write'
    
    @pytest.mark.unit
    def test_read_after_write(self, data_program):
        """Test READ after WRITE to verify persistence"""
        # Write new balance
        data_program.execute_operation('write', Decimal('2500.25'))
        # Read it back
        result = data_program.execute_operation('read', Decimal('0.00'))
        assert result == Decimal('2500.25')
    
    @pytest.mark.unit
    def test_format_currency_precision(self, data_program):
        """Test PIC 9(6)V99 precision formatting"""
        # Test with more than 2 decimal places
        result = data_program.execute_operation('write', Decimal('1000.567'))
        assert result == Decimal('1000.57')  # Rounded to 2 decimals
    
    @pytest.mark.unit
    def test_invalid_operation_type(self, data_program):
        """Test unknown operation type handling"""
        result = data_program.execute_operation('INVALID', Decimal('1000.00'))
        # Should return the input balance unchanged
        assert result == Decimal('1000.00')
    
    @pytest.mark.unit
    def test_get_current_balance_utility(self, data_program):
        """Test utility method for getting current balance"""
        assert data_program.get_current_balance() == Decimal('1000.00')
        
        # Update balance and test again
        data_program.execute_operation('write', Decimal('1500.50'))
        assert data_program.get_current_balance() == Decimal('1500.50')
    
    @pytest.mark.unit
    def test_reset_balance_utility(self, data_program):
        """Test utility method for resetting balance"""
        # Change balance first
        data_program.execute_operation('write', Decimal('2000.00'))
        assert data_program.get_current_balance() == Decimal('2000.00')
        
        # Reset to default
        result = data_program.reset_balance()
        assert result == Decimal('1000.00')
        assert data_program.get_current_balance() == Decimal('1000.00')
        
        # Reset to custom value
        result = data_program.reset_balance(Decimal('500.00'))
        assert result == Decimal('500.00')
