# AWS Reservations Report

A Python script to retrieve and report on AWS Reserved Instances and Savings Plans across your AWS account.

## Features

- **EC2 Reserved Instances**: Retrieve details about EC2 RIs including instance types, states, pricing, and terms
- **RDS Reserved Instances**: Get information about RDS RIs including database classes, engines, and configurations
- **Savings Plans**: Fetch Savings Plans details including commitments, payment options, and coverage
- **Multiple Output Formats**: Console output with summary and detailed reports, plus JSON export
- **Error Handling**: Graceful handling of AWS API errors and missing credentials

## Prerequisites

- Python 3.6 or higher
- AWS CLI configured with appropriate credentials
- Required Python packages (see requirements.txt)

## Installation

1. Clone or download this project
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## AWS Permissions Required

Your AWS credentials need the following permissions:
- `ec2:DescribeReservedInstances`
- `rds:DescribeReservedDBInstances`
- `savingsplans:DescribeSavingsPlans`
- `sts:GetCallerIdentity`

## Usage

Run the script:
```bash
python aws_reservations_report.py
```

The script will:
1. Display account information and generation timestamp
2. Retrieve all reservation data from AWS APIs
3. Show a summary of found reservations
4. Display detailed information for each reservation
5. Save results to `aws_reservations_report.json`

## Output

### Console Output
- Account ID and region information
- Summary counts by reservation type
- Detailed information for each reservation

### JSON Export
All reservation data is saved to `aws_reservations_report.json` for further analysis or integration with other tools.

## Configuration

The script uses your default AWS profile and region. To use a different profile or region:

```python
# Modify the session creation in main()
session = boto3.Session(profile_name='your-profile', region_name='us-west-2')
```

## Error Handling

The script handles common scenarios:
- Missing AWS credentials
- Insufficient permissions
- Network connectivity issues
- Empty results (no reservations found)

## Sample Output

```
AWS Reserved Instances and Savings Plans Report
==================================================
Account ID: 123456789012
Region: us-east-1
Generated: 2025-07-11 18:00:00

Retrieving EC2 Reserved Instances...
Retrieving RDS Reserved Instances...
Retrieving Savings Plans...

================================================================================
SUMMARY
================================================================================
EC2 Reserved Instances: 3
RDS Reserved Instances: 1
Savings Plans: 2
Total Reservations: 6
```
