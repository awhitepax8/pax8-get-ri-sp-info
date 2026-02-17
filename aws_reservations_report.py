#!/usr/bin/env python3
"""
AWS Reserved Instances and Savings Plans Report Script

This script retrieves and displays details about:
- EC2 Reserved Instances
- RDS Reserved Instances  
- Savings Plans subscriptions

Requirements:
- boto3 library
- AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
"""

import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError


def format_datetime(dt):
    """Format datetime object to readable string"""
    if dt:
        # Handle if dt is already a string
        if isinstance(dt, str):
            return dt
        # Handle datetime object
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    return 'N/A'


def get_all_regions(session):
    """Get all available AWS regions"""
    try:
        ec2 = session.client('ec2', region_name='us-east-1')  # Use us-east-1 to get all regions
        response = ec2.describe_regions()
        return [region['RegionName'] for region in response['Regions']]
    except ClientError as e:
        print(f"Error getting regions: {e}")
        # Fallback to common regions if API call fails
        return [
            'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
            'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-central-1',
            'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ap-northeast-2',
            'ap-south-1', 'ca-central-1', 'sa-east-1'
        ]


def get_ec2_reserved_instances(session, region):
    """Retrieve EC2 Reserved Instances for a specific region"""
    try:
        ec2 = session.client('ec2', region_name=region)
        response = ec2.describe_reserved_instances()
        
        reserved_instances = []
        for ri in response['ReservedInstances']:
            reserved_instances.append({
                'Type': 'EC2 Reserved Instance',
                'Region': region,
                'ReservedInstancesId': ri['ReservedInstancesId'],
                'InstanceType': ri['InstanceType'],
                'AvailabilityZone': ri.get('AvailabilityZone', 'N/A'),
                'State': ri['State'],
                'Start': format_datetime(ri.get('Start')),
                'End': format_datetime(ri.get('End')),
                'Duration': f"{ri['Duration']} seconds",
                'InstanceCount': ri['InstanceCount'],
                'ProductDescription': ri['ProductDescription'],
                'InstanceTenancy': ri['InstanceTenancy'],
                'OfferingClass': ri['OfferingClass'],
                'OfferingType': ri['OfferingType'],
                'FixedPrice': ri.get('FixedPrice', 0),
                'UsagePrice': ri.get('UsagePrice', 0),
                'CurrencyCode': ri.get('CurrencyCode', 'USD')
            })
        
        return reserved_instances
    
    except ClientError as e:
        if e.response['Error']['Code'] not in ['UnauthorizedOperation', 'AccessDenied']:
            print(f"Error retrieving EC2 Reserved Instances in {region}: {e}")
        return []


def get_rds_reserved_instances(session, region):
    """Retrieve RDS Reserved Instances for a specific region"""
    try:
        rds = session.client('rds', region_name=region)
        response = rds.describe_reserved_db_instances()
        
        reserved_instances = []
        for ri in response['ReservedDBInstances']:
            reserved_instances.append({
                'Type': 'RDS Reserved Instance',
                'Region': region,
                'ReservedDBInstanceId': ri['ReservedDBInstanceId'],
                'DBInstanceClass': ri['DBInstanceClass'],
                'Engine': ri['ProductDescription'],
                'State': ri['State'],
                'Start': format_datetime(ri.get('StartTime')),
                'Duration': f"{ri['Duration']} seconds",
                'DBInstanceCount': ri['DBInstanceCount'],
                'OfferingType': ri['OfferingType'],
                'MultiAZ': ri['MultiAZ'],
                'FixedPrice': ri.get('FixedPrice', 0),
                'UsagePrice': ri.get('UsagePrice', 0),
                'CurrencyCode': ri.get('CurrencyCode', 'USD')
            })
        
        return reserved_instances
    
    except ClientError as e:
        if e.response['Error']['Code'] not in ['UnauthorizedOperation', 'AccessDenied']:
            print(f"Error retrieving RDS Reserved Instances in {region}: {e}")
        return []


def get_savings_plans(session, region):
    """Retrieve Savings Plans for a specific region"""
    try:
        savingsplans = session.client('savingsplans', region_name=region)
        response = savingsplans.describe_savings_plans()
        
        savings_plans = []
        for sp in response['savingsPlans']:
            savings_plans.append({
                'Type': 'Savings Plan',
                'Region': region,
                'SavingsPlanId': sp['savingsPlanId'],
                'SavingsPlanArn': sp['savingsPlanArn'],
                'Description': sp.get('description', 'N/A'),
                'State': sp['state'],
                'PlanType': sp['savingsPlanType'],
                'PaymentOption': sp['paymentOption'],
                'Start': format_datetime(sp.get('start')),
                'End': format_datetime(sp.get('end')),
                'Commitment': f"{sp['commitment']} {sp['currency']}/hour",
                'Currency': sp['currency'],
                'UpfrontPayment': sp.get('upfrontPaymentAmount', 'N/A'),
                'RecurringPayment': sp.get('recurringPaymentAmount', 'N/A'),
                'TermDurationInSeconds': sp.get('termDurationInSeconds', 'N/A'),
                'EC2InstanceFamily': sp.get('ec2InstanceFamily', 'N/A'),
                'Region': sp.get('region', 'N/A')
            })
        
        return savings_plans
    
    except ClientError as e:
        if e.response['Error']['Code'] not in ['UnauthorizedOperation', 'AccessDenied']:
            print(f"Error retrieving Savings Plans in {region}: {e}")
        return []


def print_summary(all_reservations):
    """Print a summary of all reservations"""
    ec2_count = len([r for r in all_reservations if r['Type'] == 'EC2 Reserved Instance'])
    rds_count = len([r for r in all_reservations if r['Type'] == 'RDS Reserved Instance'])
    sp_count = len([r for r in all_reservations if r['Type'] == 'Savings Plan'])
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"EC2 Reserved Instances: {ec2_count}")
    print(f"RDS Reserved Instances: {rds_count}")
    print(f"Savings Plans: {sp_count}")
    print(f"Total Reservations: {len(all_reservations)}")


def print_detailed_report(all_reservations):
    """Print detailed report of all reservations"""
    if not all_reservations:
        print("No Reserved Instances or Savings Plans found in this account.")
        return
    
    print("\n" + "="*80)
    print("DETAILED REPORT")
    print("="*80)
    
    for reservation in all_reservations:
        print(f"\n{reservation['Type']}:")
        print("-" * 40)
        
        for key, value in reservation.items():
            if key != 'Type':
                print(f"  {key}: {value}")


def save_to_json(all_reservations, filename='aws_reservations_report.json'):
    """Save the report to a JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(all_reservations, f, indent=2, default=str)
        print(f"\nReport saved to: {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")


def main():
    """Main function"""
    try:
        # Create AWS session
        session = boto3.Session()
        
        # Get current AWS account ID
        sts = session.client('sts')
        account_info = sts.get_caller_identity()
        account_id = account_info['Account']
        
        print("AWS Reserved Instances and Savings Plans Report")
        print("=" * 50)
        print(f"Account ID: {account_id}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Get all AWS regions
        print("\nGetting list of AWS regions...")
        regions = get_all_regions(session)
        print(f"Checking {len(regions)} regions for reservations...")
        
        # Collect all reservation data across all regions
        all_reservations = []
        regions_with_data = set()
        
        for region in regions:
            print(f"\nChecking region: {region}")
            region_reservations = []
            
            # Get EC2 Reserved Instances
            ec2_reservations = get_ec2_reserved_instances(session, region)
            region_reservations.extend(ec2_reservations)
            
            # Get RDS Reserved Instances
            rds_reservations = get_rds_reserved_instances(session, region)
            region_reservations.extend(rds_reservations)
            
            # Get Savings Plans
            savings_plans = get_savings_plans(session, region)
            region_reservations.extend(savings_plans)
            
            if region_reservations:
                regions_with_data.add(region)
                print(f"  Found {len(region_reservations)} reservations in {region}")
                all_reservations.extend(region_reservations)
            else:
                print(f"  No reservations found in {region}")
        
        # Display results
        print(f"\n" + "="*80)
        print("REGIONS WITH RESERVATIONS")
        print("="*80)
        if regions_with_data:
            for region in sorted(regions_with_data):
                region_count = len([r for r in all_reservations if r.get('Region') == region])
                print(f"  {region}: {region_count} reservations")
        else:
            print("No regions found with reservations")
        
        print_summary(all_reservations)
        print_detailed_report(all_reservations)
        
        # Save to JSON file
        save_to_json(all_reservations)
        
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your AWS credentials.")
        print("You can use: aws configure, environment variables, or IAM roles.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
