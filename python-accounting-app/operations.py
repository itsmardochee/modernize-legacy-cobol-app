#!/usr/bin/env python3
"""
Operations Module - Business Logic for Account Management
Converted from COBOL Operations (operations.cob)
"""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from data import DataProgram


class Operations:
    """Operations class handling all account business logic"""
    
    def __init__(self):
        """Initialize the operations module"""
        self.operation_type = ""
        self.amount = Decimal('0.00')
        self.final_balance = Decimal('1000.00')  # Initial balance equivalent to PIC 9(6)V99 VALUE 1000.00
        self.data_program = DataProgram()
    
    def _format_currency(self, value):
        """Format decimal value to 2 decimal places like COBOL PIC 9(6)V99"""
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def _get_amount_input(self, prompt_message):
        """Get and validate amount input from user"""
        while True:
            try:
                amount_str = input(prompt_message)
                amount = Decimal(amount_str)
                
                # Validate amount is non-negative and within COBOL limits (999999.99)
                if amount < 0:
                    print("Amount cannot be negative. Please try again.")
                    continue
                elif amount > Decimal('999999.99'):
                    print("Amount exceeds maximum limit (999999.99). Please try again.")
                    continue
                
                return self._format_currency(amount)
                
            except (ValueError, TypeError, InvalidOperation):
                print("Invalid amount format. Please enter a valid number.")
                continue
    
    def _handle_total_operation(self):
        """Handle balance inquiry - equivalent to IF OPERATION-TYPE = 'TOTAL '"""
        # CALL 'DataProgram' USING 'read', FINAL-BALANCE
        self.final_balance = self.data_program.execute_operation('read', self.final_balance)
        
        # DISPLAY "Current balance: " FINAL-BALANCE
        print(f"Current balance: {self.final_balance}")
    
    def _handle_credit_operation(self):
        """Handle credit transaction - equivalent to ELSE IF OPERATION-TYPE = 'CREDIT'"""
        # DISPLAY "Enter credit amount: "
        # ACCEPT AMOUNT
        self.amount = self._get_amount_input("Enter credit amount: ")
        
        # CALL 'DataProgram' USING 'read', FINAL-BALANCE
        self.final_balance = self.data_program.execute_operation('read', self.final_balance)
        
        # ADD AMOUNT TO FINAL-BALANCE
        self.final_balance = self._format_currency(self.final_balance + self.amount)
        
        # CALL 'DataProgram' USING 'WRITE', FINAL-BALANCE
        self.data_program.execute_operation('write', self.final_balance)
        
        # DISPLAY "Amount credited. New balance: " FINAL-BALANCE
        print(f"Amount credited. New balance: {self.final_balance}")
    
    def _handle_debit_operation(self):
        """Handle debit transaction - equivalent to ELSE IF OPERATION-TYPE = 'DEBIT '"""
        # DISPLAY "Enter debit amount: "
        # ACCEPT AMOUNT
        self.amount = self._get_amount_input("Enter debit amount: ")
        
        # CALL 'DataProgram' USING 'read', FINAL-BALANCE
        self.final_balance = self.data_program.execute_operation('read', self.final_balance)
        
        # IF FINAL-BALANCE >= AMOUNT
        if self.final_balance >= self.amount:
            # SUBTRACT AMOUNT FROM FINAL-BALANCE
            self.final_balance = self._format_currency(self.final_balance - self.amount)
            
            # CALL 'DataProgram' USING 'WRITE', FINAL-BALANCE
            self.data_program.execute_operation('write', self.final_balance)
            
            # DISPLAY "Amount debited. New balance: " FINAL-BALANCE
            print(f"Amount debited. New balance: {self.final_balance}")
        else:
            # ELSE - DISPLAY "Insufficient funds for this debit."
            print("Insufficient funds for this debit.")
    
    def execute_operation(self, passed_operation):
        """
        Main operation executor - equivalent to PROCEDURE DIVISION USING PASSED-OPERATION
        
        Args:
            passed_operation (str): Operation type ('TOTAL ', 'CREDIT', 'DEBIT ')
        """
        # MOVE PASSED-OPERATION TO OPERATION-TYPE
        self.operation_type = passed_operation.strip().upper()
        
        try:
            # Handle each operation type - equivalent to IF/ELSE IF structure
            if self.operation_type == 'TOTAL':
                self._handle_total_operation()
                
            elif self.operation_type == 'CREDIT':
                self._handle_credit_operation()
                
            elif self.operation_type == 'DEBIT':
                self._handle_debit_operation()
                
            else:
                print(f"Unknown operation: {self.operation_type}")
                
        except Exception as e:
            print(f"Error processing {self.operation_type} operation: {e}")
        
        # GOBACK - return to calling program (implicit in Python)


# For testing purposes - equivalent to standalone COBOL program execution
if __name__ == "__main__":
    ops = Operations()
    
    # Test each operation
    print("Testing Operations Module:")
    print("=========================")
    
    # Test balance inquiry
    ops.execute_operation('TOTAL ')
    
    # Test credit
    print("\nTesting credit operation:")
    # Simulate user input for testing
    import sys
    from io import StringIO
    
    # Mock input for automated testing
    original_input = input
    test_inputs = iter(['100.50'])
    
    def mock_input(prompt):
        print(prompt, end='')
        value = next(test_inputs)
        print(value)
        return value
    
    # Replace input temporarily
    import builtins
    builtins.input = mock_input
    
    ops.execute_operation('CREDIT')
    ops.execute_operation('TOTAL ')
    
    # Restore original input
    builtins.input = original_input
