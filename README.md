# AWS Reservations Report

A Python script to retrieve and report on AWS Reserved Instances and Savings Plans across your AWS account.

## Quick Start with AWS CloudShell

**Important**: You need to upload the script to CloudShell before running it.

1. Open AWS CloudShell from your AWS Console (top navigation bar)
2. Upload the script file using one of these methods:
   
   **Method A - Upload file directly:**
   - Use CloudShell's "Upload file" button in the toolbar
   - Select `aws_reservations_report.py` from your local machine
   
   **Method B - Create and paste:**
   ```bash
   nano aws_reservations_report.py
   ```
   - Copy the entire script content and paste it into the editor
   - Save with Ctrl+X, Y, Enter
   
   **Method C - Clone from repository:**
   ```bash
   git clone <your-repository-url>
   cd <repository-name>
   ```

3. Run the script:
   ```bash
   python3 aws_reservations_report.py
   ```
4. Download the results:
   
   **Option A - Download JSON report:**
   ```bash
   # The script automatically saves aws_reservations_report.json
   # Use CloudShell's "Download file" feature to get the JSON report
   ```
   
   **Option B - Save console output to text file:**
   ```bash
   # Redirect all output to a text file
   python3 aws_reservations_report.py > reservations_report.txt 2>&1
   
   # Or save only the main output (without error messages)
   python3 aws_reservations_report.py > reservations_report.txt
   
   # Then download the text file using CloudShell's download feature
   ```

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

### Option 1: Local Environment
1. Clone or download this project
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: AWS CloudShell (Recommended)
AWS CloudShell is the easiest way to run this script as it comes with:
- Python 3 and boto3 pre-installed
- AWS credentials automatically configured
- No local setup required

**Steps:**
1. Open AWS CloudShell from the AWS Console
2. **Upload the script file** to CloudShell using one of these methods:
   
   **Upload via CloudShell interface:**
   - Click the "Upload file" button in CloudShell toolbar
   - Select `aws_reservations_report.py` from your computer
   
   **Create file manually:**
   ```bash
   nano aws_reservations_report.py
   # Copy and paste the entire script content, then save
   ```
   
   **Clone from repository:**
   ```bash
   git clone <your-repo-url>
   cd <repo-directory>
   ```

3. The script is now ready to run in CloudShell

## AWS Permissions Required

Your AWS credentials need the following permissions:
- `ec2:DescribeReservedInstances`
- `rds:DescribeReservedDBInstances`
- `savingsplans:DescribeSavingsPlans`
- `sts:GetCallerIdentity`

**Note**: When using AWS CloudShell, these permissions are automatically inherited from your AWS Console session.

## Usage

### Local Environment
```bash
python aws_reservations_report.py
```

### AWS CloudShell
```bash
python3 aws_reservations_report.py
```

### Output Options

**Standard execution:**
- Displays results in the console
- Automatically saves JSON file (`aws_reservations_report.json`)

**Save console output to text file:**
```bash
# Save all output (including progress messages)
python3 aws_reservations_report.py > reservations_report.txt 2>&1

# Save only main output (cleaner, no progress messages)
python3 aws_reservations_report.py > reservations_report.txt

# Save with timestamp in filename
python3 aws_reservations_report.py > reservations_report_$(date +%Y%m%d_%H%M%S).txt
```

**Benefits of text file output:**
- Human-readable format for sharing with teams
- Easy to view in any text editor
- Includes the formatted summary and detailed sections
- Can be easily copied into emails or documents

The script will:
1. Display account information and generation timestamp
2. Retrieve all reservation data from AWS APIs
3. Show a summary of found reservations
4. Display detailed information for each reservation
5. Save results to `aws_reservations_report.json`

## Output

### Console Output
- Account ID and generation timestamp
- Progress messages showing which regions are being checked
- Summary counts by reservation type and region
- Detailed information for each reservation

### File Output Options

**JSON Export (automatic):**
All reservation data is automatically saved to `aws_reservations_report.json` for further analysis or integration with other tools.

**Text File Export (manual):**
Redirect console output to a text file for easy sharing and viewing:
```bash
# Complete output with progress messages
python3 aws_reservations_report.py > report.txt 2>&1

# Clean output without progress messages  
python3 aws_reservations_report.py > report.txt
```

## Why Use AWS CloudShell?

AWS CloudShell offers several advantages for running this script:

- **No Setup Required**: Python 3 and boto3 are pre-installed
- **Automatic Authentication**: Uses your AWS Console session credentials
- **Cross-Region Access**: Inherits permissions from your AWS account
- **No Local Dependencies**: Run from any browser without installing anything
- **Secure Environment**: Runs within AWS infrastructure
- **Free Tier**: 1 GB of persistent storage included

## Configuration

The script uses your default AWS profile and region. 

### Local Environment
To use a different profile or region:

```python
# Modify the session creation in main()
session = boto3.Session(profile_name='your-profile', region_name='us-west-2')
```

### AWS CloudShell
CloudShell automatically uses your console session credentials. The script will check all regions regardless of which region you're currently viewing in the console.

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
