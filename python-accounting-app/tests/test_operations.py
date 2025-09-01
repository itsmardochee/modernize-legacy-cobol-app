import pytest
from decimal import Decimal
from unittest.mock import Mock, patch, call
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from operations import Operations


class TestOperations:
    """Unit tests for Operations - TC_BAL_*, TC_CRE_*, TC_DEB_*"""
    
    @pytest.fixture
    def mock_data_program(self):
        """Create mock DataProgram"""
        mock_dp = Mock()
        mock_dp.execute_operation.return_value = Decimal('1000.00')
        return mock_dp
    
    @pytest.fixture
    def operations(self, mock_data_program):
        """Create Operations instance with mocked DataProgram"""
        ops = Operations()
        ops.data_program = mock_data_program
        return ops
    
    @pytest.mark.unit
    def test_initialization(self):
        """Test Operations initialization"""
        ops = Operations()
        assert ops.operation_type == ""
        assert ops.amount == Decimal('0.00')
        assert ops.final_balance == Decimal('1000.00')
    
    @pytest.mark.unit
    def test_total_operation_tc_bal_001(self, operations, mock_data_program, capsys):
        """TC_BAL_001: Initial balance inquiry - 1000.00"""
        mock_data_program.execute_operation.return_value = Decimal('1000.00')
        
        operations.execute_operation('TOTAL ')
        
        # Verify DataProgram was called with 'read'
        mock_data_program.execute_operation.assert_called_with('read', Decimal('1000.00'))
        
        # Check display output
        captured = capsys.readouterr()
        assert "Current balance: 1000.00" in captured.out
        assert operations.operation_type == 'TOTAL'
    
    @pytest.mark.unit
    def test_total_operation_tc_bal_002(self, operations, mock_data_program, capsys):
        """TC_BAL_002: Balance after credit - 1200.00"""
        mock_data_program.execute_operation.return_value = Decimal('1200.00')
        
        operations.execute_operation('TOTAL ')
        
        captured = capsys.readouterr()
        assert "Current balance: 1200.00" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', side_effect=lambda prompt: print(prompt) or'250.50')
    def test_credit_operation_tc_cre_001(self, mock_input, operations, mock_data_program, capsys):
        """TC_CRE_001: Valid credit amount - 250.50"""
        mock_data_program.execute_operation.side_effect = [Decimal('1000.00'), Decimal('1250.50')]
        
        operations.execute_operation('CREDIT')
        
        # Verify calls to DataProgram
        expected_calls = [
            call('read', Decimal('1000.00')),
            call('write', Decimal('1250.50'))
        ]
        mock_data_program.execute_operation.assert_has_calls(expected_calls)
        
        # Check display output
        captured = capsys.readouterr()
        assert "Enter credit amount:" in captured.out
        assert "Amount credited. New balance: 1250.50" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='0')
    def test_credit_operation_tc_cre_002(self, mock_input, operations, mock_data_program, capsys):
        """TC_CRE_002: Zero credit amount"""
        mock_data_program.execute_operation.side_effect = [Decimal('1000.00'), Decimal('1000.00')]
        
        operations.execute_operation('CREDIT')
        
        # Should accept zero amount and process normally
        captured = capsys.readouterr()
        assert "Amount credited. New balance: 1000.00" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='99.99')
    def test_credit_operation_tc_cre_003(self, mock_input, operations, mock_data_program, capsys):
        """TC_CRE_003: Decimal credit amount - 99.99"""
        mock_data_program.execute_operation.side_effect = [Decimal('1000.00'), Decimal('1099.99')]
        
        operations.execute_operation('CREDIT')
        
        captured = capsys.readouterr()
        assert "Amount credited. New balance: 1099.99" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='999999.99')
    def test_credit_operation_tc_cre_004(self, mock_input, operations, mock_data_program, capsys):
        """TC_CRE_004: Maximum credit amount - 999999.99"""
        mock_data_program.execute_operation.side_effect = [Decimal('1000.00'), Decimal('1000999.99')]
        
        operations.execute_operation('CREDIT')
        
        captured = capsys.readouterr()
        assert "Amount credited" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', side_effect=lambda prompt: print(prompt) or'200.00')
    def test_debit_operation_tc_deb_001(self, mock_input, operations, mock_data_program, capsys):
        """TC_DEB_001: Valid debit with sufficient funds - 200.00"""
        mock_data_program.execute_operation.side_effect = [Decimal('1000.00'), Decimal('800.00')]
        
        operations.execute_operation('DEBIT ')
        
        # Verify calls to DataProgram
        expected_calls = [
            call('read', Decimal('1000.00')),
            call('write', Decimal('800.00'))
        ]
        mock_data_program.execute_operation.assert_has_calls(expected_calls)
        
        captured = capsys.readouterr()
        assert "Enter debit amount:" in captured.out
        assert "Amount debited. New balance: 800.00" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='1000.00')
    def test_debit_operation_tc_deb_002(self, mock_input, operations, mock_data_program, capsys):
        """TC_DEB_002: Debit amount equal to balance"""
        mock_data_program.execute_operation.side_effect = [Decimal('1000.00'), Decimal('0.00')]
        
        operations.execute_operation('DEBIT ')
        
        captured = capsys.readouterr()
        assert "Amount debited. New balance: 0.00" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='1500.00')
    def test_debit_operation_tc_deb_003(self, mock_input, operations, mock_data_program, capsys):
        """TC_DEB_003: Insufficient funds - debit 1500.00 from 1000.00"""
        mock_data_program.execute_operation.return_value = Decimal('1000.00')
        
        operations.execute_operation('DEBIT ')
        
        # Should only call read, not write
        mock_data_program.execute_operation.assert_called_once_with('read', Decimal('1000.00'))
        
        captured = capsys.readouterr()
        assert "Insufficient funds for this debit." in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='0')
    def test_debit_operation_tc_deb_004(self, mock_input, operations, mock_data_program, capsys):
        """TC_DEB_004: Zero debit amount"""
        mock_data_program.execute_operation.side_effect = [Decimal('1000.00'), Decimal('1000.00')]
        
        operations.execute_operation('DEBIT ')
        
        captured = capsys.readouterr()
        assert "Amount debited. New balance: 1000.00" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='100.01')
    def test_debit_operation_tc_deb_005(self, mock_input, operations, mock_data_program, capsys):
        """TC_DEB_005: Insufficient funds by 1 cent - 100.01 from 100.00"""
        mock_data_program.execute_operation.return_value = Decimal('100.00')
        operations.final_balance = Decimal('100.00')
        
        operations.execute_operation('DEBIT ')
        
        captured = capsys.readouterr()
        assert "Insufficient funds for this debit." in captured.out
    
    @pytest.mark.unit
    def test_format_currency(self, operations):
        """Test currency formatting to 2 decimal places"""
        result = operations._format_currency(Decimal('123.456'))
        assert result == Decimal('123.46')
        
        result = operations._format_currency(Decimal('123.454'))
        assert result == Decimal('123.45')
    
    @pytest.mark.unit
    @patch('builtins.input', side_effect=['invalid', '100.50'])
    def test_get_amount_input_invalid_then_valid(self, mock_input, operations, capsys):
        """Test TC_ROB_001: Special characters in amount input"""
        amount = operations._get_amount_input("Enter amount: ")
        assert amount == Decimal('100.50')
        
        captured = capsys.readouterr()
        assert "Invalid amount format" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', side_effect=['-100', '100.50'])
    def test_get_amount_input_negative_then_valid(self, mock_input, operations, capsys):
        """Test TC_ROB_002: Negative amounts"""
        amount = operations._get_amount_input("Enter amount: ")
        assert amount == Decimal('100.50')
        
        captured = capsys.readouterr()
        assert "Amount cannot be negative" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', side_effect=['9999999.99', '100.50'])
    def test_get_amount_input_over_limit_then_valid(self, mock_input, operations, capsys):
        """Test amount over COBOL PIC 9(6)V99 limit"""
        amount = operations._get_amount_input("Enter amount: ")
        assert amount == Decimal('100.50')
        
        captured = capsys.readouterr()
        assert "Amount exceeds maximum limit" in captured.out
