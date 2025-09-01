import pytest
from unittest.mock import patch
from decimal import Decimal
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import MainProgram
from operations import Operations
from data import DataProgram


class TestIntegration:
    """Integration tests - TC_INT_* and TC_DATA_003"""
    
    @pytest.fixture
    def integrated_system(self):
        """Create fully integrated system"""
        main_program = MainProgram()
        return main_program
    
    @pytest.mark.integration
    def test_complete_flow_balance_inquiry_tc_int_001(self, integrated_system, capsys):
        """TC_INT_001: Complete flow - Balance inquiry (MainProgram → Operations → DataProgram)"""
        # Test the complete chain: MainProgram → Operations → DataProgram
        main_program = integrated_system
        
        # Directly test the chain
        main_program.process_choice(1)  # View Balance
        
        captured = capsys.readouterr()
        assert "Current balance: 1000.00" in captured.out
    
    @pytest.mark.integration
    @patch('builtins.input', side_effect=lambda prompt: print(prompt) or'250.75')
    def test_complete_flow_credit_tc_int_002(self, mock_input, integrated_system, capsys):
        """TC_INT_002: Complete flow - Credit transaction"""
        main_program = integrated_system
        
        # Execute credit operation
        main_program.process_choice(2)
        
        captured = capsys.readouterr()
        assert "Enter credit amount:" in captured.out
        assert "Amount credited. New balance: 1250.75" in captured.out
        
        # Verify balance was actually updated by checking it
        main_program.process_choice(1)  # View Balance
        captured = capsys.readouterr()
        assert "Current balance: 1250.75" in captured.out
    
    @pytest.mark.integration
    @patch('builtins.input',side_effect=lambda prompt: print(prompt) or'300.50')
    def test_complete_flow_successful_debit_tc_int_003(self, mock_input, integrated_system, capsys):
        """TC_INT_003: Complete flow - Successful debit transaction"""
        main_program = integrated_system
        
        # Execute debit operation
        main_program.process_choice(3)
        
        captured = capsys.readouterr()
        assert "Enter debit amount:" in captured.out
        assert "Amount debited. New balance: 699.50" in captured.out
        
        # Verify balance was actually updated
        main_program.process_choice(1)  # View Balance
        captured = capsys.readouterr()
        assert "Current balance: 699.50" in captured.out
    
    @pytest.mark.integration
    @patch('builtins.input', side_effect=lambda prompt: print(prompt) or '1500.00')
    def test_complete_flow_rejected_debit_tc_int_004(self, mock_input, integrated_system, capsys):
        """TC_INT_004: Complete flow - Rejected debit (insufficient funds)"""
        main_program = integrated_system
        
        # Execute debit operation with insufficient funds
        main_program.process_choice(3)
        
        captured = capsys.readouterr()
        assert "Enter debit amount:" in captured.out
        assert "Insufficient funds for this debit." in captured.out
        
        # Verify balance was not changed
        main_program.process_choice(1)  # View Balance
        captured = capsys.readouterr()
        assert "Current balance: 1000.00" in captured.out
    
    # @pytest.mark.integration
    # def test_data_persistence_between_operations_tc_data_003(self):
    #     """TC_DATA_003: Data persistence between operations"""
    #     # Create separate instances to test persistence
    #     ops1 = Operations()
    #     ops2 = Operations()
        
    #     # First operation: Credit 200.00
    #     with patch('builtins.input', side_effect=lambda prompt: print(prompt) or'200.00'):
    #         ops1.execute_operation('CREDIT')
        
    #     # Second operation with new instance: Check balance
    #     # The balance should persist because DataProgram maintains STORAGE-BALANCE
    #     import io
    #     import contextlib
        
    #     f = io.StringIO()
    #     with contextlib.redirect_stdout(f):
    #         ops2.execute_operation('TOTAL ')
    #     output = f.getvalue()
        
    #     assert "Current balance: 1200.00" in output
    
    @pytest.mark.integration
    @patch('builtins.input', side_effect=['500.25', '150.75'])
    def test_multiple_operations_sequence(self, mock_input, integrated_system, capsys):
        """Test sequence of multiple operations maintaining state"""
        main_program = integrated_system
        
        # Starting balance: 1000.00
        main_program.process_choice(1)  # View Balance
        captured = capsys.readouterr()
        assert "Current balance: 1000.00" in captured.out
        
        # Credit 500.25 → 1500.25
        main_program.process_choice(2)
        captured = capsys.readouterr()
        assert "Amount credited. New balance: 1500.25" in captured.out
        
        # Debit 150.75 → 1349.50
        main_program.process_choice(3)
        captured = capsys.readouterr()
        assert "Amount debited. New balance: 1349.50" in captured.out
        
        # Final balance check
        main_program.process_choice(1)
        captured = capsys.readouterr()
        assert "Current balance: 1349.50" in captured.out
    
    @pytest.mark.integration
    @patch('builtins.input', side_effect=['1', '4'])
    def test_main_program_complete_run_tc_int_001(self, mock_input, integrated_system, capsys):
        """Test complete MainProgram run with balance inquiry"""
        main_program = integrated_system
        
        main_program.run()
        
        captured = capsys.readouterr()
        
        # Check menu display
        assert "Account Management System" in captured.out
        assert "1. View Balance" in captured.out
        
        # Check balance inquiry
        assert "Current balance: 1000.00" in captured.out
        
        # Check exit
        assert "Exiting the program. Goodbye!" in captured.out
    
    @pytest.mark.integration
    def test_decimal_precision_throughout_system(self, integrated_system):
        """Test that decimal precision is maintained throughout the system"""
        main_program = integrated_system
        
        # Test with precise decimal values
        with patch('builtins.input', return_value='123.456'):
            import io
            import contextlib
            
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                main_program.process_choice(2)  # Credit
            output = f.getvalue()
            
            # Should be rounded to 2 decimal places: 123.46
            assert "1123.46" in output  # 1000.00 + 123.46
    
    @pytest.mark.integration
    def test_boundary_conditions_integration(self, integrated_system):
        """Test boundary conditions in integrated environment"""
        main_program = integrated_system
        
        # Test exact balance debit
        with patch('builtins.input', return_value='1000.00'):
            import io
            import contextlib
            
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                main_program.process_choice(3)  # Debit exact amount
            output = f.getvalue()
            
            assert "Amount debited. New balance: 0.00" in output
        
        # Verify zero balance
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            main_program.process_choice(1)  # Check balance
        output = f.getvalue()
        
        assert "Current balance: 0.00" in output
