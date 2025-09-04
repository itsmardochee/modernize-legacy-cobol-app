#!/usr/bin/env python3
"""
Data Program Module - Data Persistence Layer
Converted from COBOL DataProgram (data.cob)
"""

from decimal import Decimal, ROUND_HALF_UP
import json
import os
from typing import Union


class DataProgram:
    """Data program class handling data persistence operations"""

    def __init__(self):
        """Initialize the data program - equivalent to WORKING-STORAGE SECTION"""
        # STORAGE-BALANCE PIC 9(6)V99 VALUE 1000.00
        self.storage_balance = Decimal("1000.00")
        self.operation_type = ""

        # Enhanced persistence - store data in JSON file for session persistence
        # self.data_file = '/workspaces/modernize-legacy-cobol-app/account_data.json'
        # self._load_data()

    def _format_currency(self, value):
        """Format decimal value to 2 decimal places like COBOL PIC 9(6)V99"""
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # def _load_data(self):
    #     """Load data from persistent storage (enhanced from COBOL)"""
    #     try:
    #         if os.path.exists(self.data_file):
    #             with open(self.data_file, 'r') as f:
    #                 data = json.load(f)
    #                 self.storage_balance = Decimal(str(data.get('balance', '1000.00')))
    #         else:
    #             # First run - use default balance
    #             self._save_data()
    #     except Exception as e:
    #         print(f"Warning: Could not load data file, using default balance: {e}")
    #         self.storage_balance = Decimal('1000.00')

    # def _save_data(self):
    #     """Save data to persistent storage (enhanced from COBOL)"""
    #     try:
    #         data = {
    #             'balance': str(self.storage_balance),
    #             'last_updated': str(__import__('datetime').datetime.now())
    #         }
    #         with open(self.data_file, 'w') as f:
    #             json.dump(data, f, indent=2)
    #     except Exception as e:
    #         print(f"Warning: Could not save data file: {e}")

    def _handle_read_operation(self, balance):
        """
        Handle read operation - equivalent to IF OPERATION-TYPE = 'READ'

        Args:
            balance (Decimal): Balance parameter from calling program

        Returns:
            Decimal: Current storage balance
        """
        # MOVE STORAGE-BALANCE TO BALANCE
        return self.storage_balance

    def _handle_write_operation(self, balance):
        """
        Handle write operation - equivalent to ELSE IF OPERATION-TYPE = 'WRITE'

        Args:
            balance (Decimal): New balance to store

        Returns:
            Decimal: Updated balance (same as input)
        """
        # MOVE BALANCE TO STORAGE-BALANCE
        self.storage_balance = self._format_currency(balance)

        # # Enhanced: Persist to file
        # self._save_data()

        return self.storage_balance

    def execute_operation(self, passed_operation, balance):
        """
        Main operation executor - equivalent to PROCEDURE DIVISION USING PASSED-OPERATION BALANCE

        Args:
            passed_operation (str): Operation type ('read' or 'write')
            balance (Decimal): Balance parameter

        Returns:
            Decimal: Result balance based on operation
        """
        # MOVE PASSED-OPERATION TO OPERATION-TYPE
        self.operation_type = passed_operation.lower().strip()

        try:
            # Convert balance to Decimal if it's not already
            if not isinstance(balance, Decimal):
                balance = Decimal(str(balance))

            # Handle operations - equivalent to IF/ELSE IF structure
            if self.operation_type == "read":
                return self._handle_read_operation(balance)

            elif self.operation_type == "write":
                return self._handle_write_operation(balance)

            else:
                print(f"Unknown operation: {self.operation_type}")
                return balance

        except Exception as e:
            print(f"Error in DataProgram operation '{self.operation_type}': {e}")
            return balance

        # GOBACK - return to calling program (implicit in Python)

    def get_current_balance(self):
        """Utility method to get current balance without operation overhead"""
        return self.storage_balance
