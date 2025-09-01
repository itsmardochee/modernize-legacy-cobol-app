# Test Plan - COBOL Account Management System

## Overview
This test plan covers all business logic of the COBOL application composed of three main modules: [`MainProgram`](main.cob), [`Operations`](operations.cob), and [`DataProgram`](data.cob).

## Functional Tests

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_MAIN_001** | **User Interface - Main menu display** | Application is started | 1. Launch the application<br/>2. Observe initial display | Menu displays with:<br/>- "Account Management System"<br/>- Options 1-4 (View Balance, Credit, Debit, Exit)<br/>- Prompt "Enter your choice (1-4):" | | | |
| **TC_MAIN_002** | **Navigation - Valid option selection (1)** | Main menu displayed | 1. Enter "1"<br/>2. Observe behavior | "View Balance" option selected and [`Operations`](operations.cob) called with 'TOTAL ' | | | |
| **TC_MAIN_003** | **Navigation - Valid option selection (2)** | Main menu displayed | 1. Enter "2"<br/>2. Observe behavior | "Credit Account" option selected and [`Operations`](operations.cob) called with 'CREDIT' | | | |
| **TC_MAIN_004** | **Navigation - Valid option selection (3)** | Main menu displayed | 1. Enter "3"<br/>2. Observe behavior | "Debit Account" option selected and [`Operations`](operations.cob) called with 'DEBIT ' | | | |
| **TC_MAIN_005** | **Navigation - Exit option selection (4)** | Main menu displayed | 1. Enter "4"<br/>2. Observe behavior | - "Exiting the program. Goodbye!" message displayed<br/>- Application terminates | | | |
| **TC_MAIN_006** | **Validation - Invalid option** | Main menu displayed | 1. Enter invalid value (0, 5, letter)<br/>2. Observe behavior | - "Invalid choice, please select 1-4." message displayed<br/>- Menu displays again | | | |
| **TC_MAIN_007** | **Loop - Return to menu after operation** | Operation completed (except exit) | 1. Perform an operation (1, 2, or 3)<br/>2. Observe after completion | Main menu displays again | | | |

## Balance Inquiry Tests

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_BAL_001** | **Inquiry - Initial balance** | - Application started<br/>- No transactions performed | 1. Select option "1"<br/>2. Observe display | "Current balance: 1000.00" message displayed | | | Default initial balance |
| **TC_BAL_002** | **Inquiry - Balance after credit** | Credit of 200.00 performed | 1. Select option "1"<br/>2. Observe display | "Current balance: 1200.00" message displayed | | | |
| **TC_BAL_003** | **Inquiry - Balance after debit** | Debit of 150.00 performed | 1. Select option "1"<br/>2. Observe display | Current balance minus 150.00 displayed | | | |

## Credit Tests

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_CRE_001** | **Credit - Valid amount** | Initial balance: 1000.00 | 1. Select option "2"<br/>2. Enter "250.50" when prompted<br/>3. Observe messages | - "Enter credit amount:" displayed<br/>- "Amount credited. New balance: 1250.50" displayed<br/>- Balance updated in [`DataProgram`](data.cob) | | | |
| **TC_CRE_002** | **Credit - Zero amount** | Initial balance: 1000.00 | 1. Select option "2"<br/>2. Enter "0" when prompted<br/>3. Observe messages | - Credit accepted<br/>- Balance remains 1000.00<br/>- Confirmation message displayed | | | Edge case test |
| **TC_CRE_003** | **Credit - Decimal amount** | Initial balance: 1000.00 | 1. Select option "2"<br/>2. Enter "99.99" when prompted<br/>3. Observe messages | - Credit accepted<br/>- New balance: 1099.99<br/>- Confirmation message displayed | | | |
| **TC_CRE_004** | **Credit - Maximum amount** | Initial balance: 1000.00 | 1. Select option "2"<br/>2. Enter "999999.99" when prompted<br/>3. Observe messages | Behavior according to PIC 9(6)V99 limits | | | Upper boundary test |

## Debit Tests

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_DEB_001** | **Debit - Valid amount with sufficient funds** | Initial balance: 1000.00 | 1. Select option "3"<br/>2. Enter "200.00" when prompted<br/>3. Observe messages | - "Enter debit amount:" displayed<br/>- "Amount debited. New balance: 800.00" displayed<br/>- Balance updated in [`DataProgram`](data.cob) | | | |
| **TC_DEB_002** | **Debit - Amount equal to balance** | Initial balance: 1000.00 | 1. Select option "3"<br/>2. Enter "1000.00" when prompted<br/>3. Observe messages | - Debit accepted<br/>- New balance: 0.00<br/>- Confirmation message displayed | | | Edge case test |
| **TC_DEB_003** | **Debit - Insufficient funds** | Initial balance: 1000.00 | 1. Select option "3"<br/>2. Enter "1500.00" when prompted<br/>3. Observe messages | - "Insufficient funds for this debit." displayed<br/>- Balance remains 1000.00 (unchanged) | | | Critical business rule |
| **TC_DEB_004** | **Debit - Zero amount** | Initial balance: 1000.00 | 1. Select option "3"<br/>2. Enter "0" when prompted<br/>3. Observe messages | - Debit accepted<br/>- Balance remains 1000.00<br/>- Confirmation message displayed | | | Edge case test |
| **TC_DEB_005** | **Debit - Insufficient funds (1 cent)** | Initial balance: 100.00 | 1. Select option "3"<br/>2. Enter "100.01" when prompted<br/>3. Observe messages | - "Insufficient funds for this debit." displayed<br/>- Balance remains 100.00 (unchanged) | | | Decimal precision test |

## Data Persistence Tests

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_DATA_001** | **Read - READ operation** | [`DataProgram`](data.cob) initialized | 1. Call DataProgram with 'READ'<br/>2. Verify returned value | STORAGE-BALANCE is copied to BALANCE | | | Unit test |
| **TC_DATA_002** | **Write - WRITE operation** | [`DataProgram`](data.cob) initialized | 1. Call DataProgram with 'WRITE' and new value<br/>2. Verify STORAGE-BALANCE | STORAGE-BALANCE is updated with new value | | | Unit test |
| **TC_DATA_003** | **Persistence - Data between operations** | Multiple transactions performed | 1. Perform credit 200.00<br/>2. Check balance<br/>3. Perform debit 50.00<br/>4. Check final balance | - After credit: 1200.00<br/>- After debit: 1150.00<br/>- Data persists between calls | | | Integration test |

## Integration Tests

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_INT_001** | **Complete flow - Balance inquiry** | Application started | 1. [`MainProgram`](main.cob) → menu<br/>2. Option 1 → [`Operations`](operations.cob) 'TOTAL '<br/>3. [`Operations`](operations.cob) → [`DataProgram`](data.cob) 'READ'<br/>4. Return to user | Communication between all modules successful | | | End-to-end test |
| **TC_INT_002** | **Complete flow - Credit** | Application started | 1. [`MainProgram`](main.cob) → menu<br/>2. Option 2 → [`Operations`](operations.cob) 'CREDIT'<br/>3. Amount input → calculation → [`DataProgram`](data.cob) 'WRITE'<br/>4. User confirmation | Complete credit transaction successful | | | End-to-end test |
| **TC_INT_003** | **Complete flow - Successful debit** | Sufficient balance | 1. [`MainProgram`](main.cob) → menu<br/>2. Option 3 → [`Operations`](operations.cob) 'DEBIT '<br/>3. Funds validation → calculation → [`DataProgram`](data.cob) 'WRITE'<br/>4. User confirmation | Complete debit transaction successful | | | End-to-end test |
| **TC_INT_004** | **Complete flow - Rejected debit** | Insufficient balance | 1. [`MainProgram`](main.cob) → menu<br/>2. Option 3 → [`Operations`](operations.cob) 'DEBIT '<br/>3. Funds validation fails<br/>4. Error message to user | Transaction rejected, data unchanged | | | Business rule test |

## Robustness Tests

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_ROB_001** | **Handling - Special characters in amount** | Credit/debit menu displayed | 1. Select credit or debit<br/>2. Enter non-numeric characters<br/>3. Observe behavior | Defined behavior (error or conversion) | | | Input validation test |
| **TC_ROB_002** | **Handling - Negative amounts** | Credit/debit menu displayed | 1. Select credit or debit<br/>2. Enter negative amount<br/>3. Observe behavior | Defined behavior per business rules | | | Edge case test |
| **TC_ROB_003** | **Handling - Multiple sessions** | Multiple simultaneous users | 1. Start multiple instances<br/>2. Perform transactions<br/>3. Verify consistency | Predictable behavior for shared data | | | Concurrency test |

## Acceptance Criteria

### Critical Features (Mandatory)
- ✅ Balance inquiry without modification
- ✅ Credit with correct balance update
- ✅ Debit with funds verification
- ✅ Rejection of debits with insufficient funds
- ✅ Correct menu navigation
- ✅ Clean application exit

### Business Rules
- ✅ Initial balance: 1000.00
- ✅ Precision: 2 decimal places
- ✅ No negative balance allowed
- ✅ Data persistence during session

### Performance
- ✅ Response time < 1 second for each operation
- ✅ Responsive user interface

## Notes for Python Migration

This test plan will serve as the foundation for:
1. **Unit tests**: Each corresponding Python function
2. **Integration tests**: Communication between Python modules
3. **Regression tests**: Validation that business logic remains identical
4. **Validation tests**: Confirmation with business stakeholders

**Reference COBOL files**:
- [`main.cob`](main.cob) - User interface
- [`operations.cob`](operations.cob) - Business logic  
- [`data.cob`](data.cob) - Data persistence
