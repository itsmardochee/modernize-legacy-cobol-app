import pytest
from unittest.mock import Mock, patch, call
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import MainProgram


class TestMainProgram:
    """Unit tests for MainProgram - TC_MAIN_* test cases"""
    
    @pytest.fixture
    def mock_operations(self):
        """Create mock Operations"""
        mock_ops = Mock()
        return mock_ops
    
    @pytest.fixture
    def main_program(self, mock_operations):
        """Create MainProgram with mocked Operations"""
        mp = MainProgram()
        mp.operations = mock_operations
        return mp
    
    @pytest.mark.unit
    def test_initialization(self):
        """Test MainProgram initialization"""
        mp = MainProgram()
        assert mp.user_choice == 0
        assert mp.continue_flag is True
        assert mp.operations is not None
    
    @pytest.mark.unit
    def test_display_menu_tc_main_001(self, main_program, capsys):
        """TC_MAIN_001: User Interface - Main menu display"""
        main_program.display_menu()
        captured = capsys.readouterr()
        
        expected_content = [
            "--------------------------------",
            "Account Management System",
            "1. View Balance",
            "2. Credit Account",
            "3. Debit Account",
            "4. Exit",
            "--------------------------------"
        ]
        
        for content in expected_content:
            assert content in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='1')
    def test_get_user_choice_valid(self, mock_input, main_program):
        """Test valid user choice input"""
        choice = main_program.get_user_choice()
        assert choice == 1
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='invalid')
    def test_get_user_choice_invalid(self, mock_input, main_program):
        """Test invalid user choice input"""
        choice = main_program.get_user_choice()
        assert choice == 0  # Invalid choice returns 0
    
    @pytest.mark.unit
    def test_process_choice_1_tc_main_002(self, main_program, mock_operations):
        """TC_MAIN_002: Navigation - Valid option selection (1) - View Balance"""
        main_program.process_choice(1)
        
        # Should call Operations with 'TOTAL '
        mock_operations.execute_operation.assert_called_once_with('TOTAL ')
    
    @pytest.mark.unit
    def test_process_choice_2_tc_main_003(self, main_program, mock_operations):
        """TC_MAIN_003: Navigation - Valid option selection (2) - Credit Account"""
        main_program.process_choice(2)
        
        # Should call Operations with 'CREDIT'
        mock_operations.execute_operation.assert_called_once_with('CREDIT')
    
    @pytest.mark.unit
    def test_process_choice_3_tc_main_004(self, main_program, mock_operations):
        """TC_MAIN_004: Navigation - Valid option selection (3) - Debit Account"""
        main_program.process_choice(3)
        
        # Should call Operations with 'DEBIT '
        mock_operations.execute_operation.assert_called_once_with('DEBIT ')
    
    @pytest.mark.unit
    def test_process_choice_4_tc_main_005(self, main_program, mock_operations):
        """TC_MAIN_005: Navigation - Exit option selection (4)"""
        main_program.process_choice(4)
        
        # Should set continue_flag to False
        assert main_program.continue_flag is False
        
        # Should not call operations
        mock_operations.execute_operation.assert_not_called()
    
    @pytest.mark.unit
    def test_process_choice_invalid_tc_main_006(self, main_program, mock_operations, capsys):
        """TC_MAIN_006: Validation - Invalid option"""
        main_program.process_choice(0)
        
        captured = capsys.readouterr()
        assert "Invalid choice, please select 1-4." in captured.out
        
        # Test with another invalid option
        main_program.process_choice(5)
        captured = capsys.readouterr()
        assert "Invalid choice, please select 1-4." in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', side_effect=['1', '4'])
    def test_run_complete_flow_tc_main_007(self, mock_input, main_program, mock_operations, capsys):
        """TC_MAIN_007: Loop - Return to menu after operation and then exit"""
        main_program.run()
        
        # Should call operations once for choice 1, then exit on choice 4
        mock_operations.execute_operation.assert_called_once_with('TOTAL ')
        
        captured = capsys.readouterr()
        assert "Account Management System" in captured.out
        assert "Exiting the program. Goodbye!" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', side_effect=['invalid', '1', '4'])
    def test_run_with_invalid_input_then_valid(self, mock_input, main_program, mock_operations, capsys):
        """Test run with invalid input followed by valid inputs"""
        main_program.run()
        
        # Should eventually call operations for choice 1
        mock_operations.execute_operation.assert_called_once_with('TOTAL ')
        
        captured = capsys.readouterr()
        assert "Invalid choice, please select 1-4." in captured.out
        assert "Exiting the program. Goodbye!" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='4')
    def test_run_immediate_exit(self, mock_input, main_program, mock_operations, capsys):
        """Test immediate exit without operations"""
        main_program.run()
        
        # Should not call any operations
        mock_operations.execute_operation.assert_not_called()
        
        captured = capsys.readouterr()
        assert "Exiting the program. Goodbye!" in captured.out
    
    @pytest.mark.unit
    @patch('builtins.input', side_effect=['2', '3', '1', '4'])
    def test_multiple_operations_sequence(self, mock_input, main_program, mock_operations, capsys):
        """Test sequence of multiple operations"""
        main_program.run()
        
        # Should call operations 3 times
        expected_calls = [
            call('CREDIT'),
            call('DEBIT '),
            call('TOTAL ')
        ]
        mock_operations.execute_operation.assert_has_calls(expected_calls)
        
        captured = capsys.readouterr()
        assert "Exiting the program. Goodbye!" in captured.out
