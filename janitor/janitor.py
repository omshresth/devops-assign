import boto3
import json
import argparse
from datetime import datetime, timezone
from constants import RESOURCE_COSTS
from rich import print
import sys

print("connecting to LocalStack.....")

ec2=boto3.client(
    "ec2" ,
    endpoint_url="http://localhost:4566" ,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

print("connected successfully!")


#Created Argument Parser
parser = argparse.ArgumentParser()

parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Scan only"
)

parser.add_argument(
    "--delete",
    action="store_true",
    help="Delete orphan resources"
)

args = parser.parse_args()
if not args.delete:
    args.dry_run = True
print("Dry Run:", args.dry_run)
print("Delete:", args.delete)


#Created Protection Function
def is_protected(tags):
    return tags.get("Protected", "false").lower() == "true" 


def parse_tags(tag_list):
    return {
        tag["Key"]: tag["Value"]
        for tag in tag_list
    }  


findings=[]

#Detect Unattached EBS Volumes
volumes = ec2.describe_volumes()

for volume in volumes["Volumes"]:

    tags = parse_tags(
        volume.get("Tags", [])
    )

    if volume["State"] == "available":

        findings.append({
            "resource_id": volume["VolumeId"],
            "resource_type": "ebs_volume",
            "reason": "unattached",
            "age_days": 0,
            "estimated_monthly_cost_usd":
                RESOURCE_COSTS["ebs_volume"],
            "tags": tags,
            "suggested_action": "delete",
            "safe_to_auto_delete":
                not is_protected(tags)
        })

        if args.delete and not is_protected(tags):

            print(
                f"Deleting volume "
                f"{volume['VolumeId']}"
            )

            ec2.delete_volume(
                VolumeId=volume["VolumeId"]
            )
    

#detect elastic ip
addresses = ec2.describe_addresses()
for address in addresses["Addresses"]:
  if "InstanceId" not in address:
    findings.append({
        "resource_id": address["AllocationId"],
        "resource_type": "elastic_ip",
        "reason": "unused",
        "age_days": 0,
        "estimated_monthly_cost_usd": RESOURCE_COSTS["elastic_ip"],
        "tags": {},
        "suggested_action": "release",
        "safe_to_auto_delete": True
    })
    if args.delete:

            print(
                f"Releasing EIP "
                f"{address['AllocationId']}"
            )

            ec2.release_address(
                AllocationId=
                    address["AllocationId"]
            )


#detect stopped instance
instances = ec2.describe_instances()

for reservation in instances["Reservations"]:
    for instance in reservation["Instances"]:

        tags = parse_tags(
            instance.get("Tags", [])
        )

        state = instance["State"]["Name"]

        if state == "stopped":
            findings.append({
                "resource_id": instance["InstanceId"],
                "resource_type": "stopped_instance",
                "reason": "instance stopped too long",
                "age_days": 14,
                "estimated_monthly_cost_usd":
                    RESOURCE_COSTS["stopped_instance"],
                "tags": tags,
                "suggested_action": "terminate",
                "safe_to_auto_delete":
                    not is_protected(tags)
            })

            if args.delete and not is_protected(tags):

                print(
                    f"Terminating instance "
                    f"{instance['InstanceId']}"
                )

                ec2.terminate_instances(
                    InstanceIds=[
                        instance["InstanceId"]
                    ]
                )

#Detect Missing Tags
REQUIRED_TAGS = ["Project", "Environment", "Owner"]
for reservation in instances["Reservations"]:
  for instance in reservation["Instances"]:   
    tags={
      tag["Key"] : tag["Value"]
      for tag in instance.get("Tags",[])
    }
    missing=[
      tag for tag in REQUIRED_TAGS
      if tag not in tags
    ]
    if missing:
      findings.append({
        "resource_id": instance["InstanceId"],
                "resource_type": "ec2_instance",
                "reason": f"missing tags: {','.join(missing)}",
                "age_days": 0,
                "estimated_monthly_cost_usd": 0,
                "tags": tags,
                "suggested_action": "add_tags",
                "safe_to_auto_delete": False
      })   

#Generate JSON Report
report={
  "scan_timestamp":datetime.now(timezone.utc).isoformat(),
  "account_id": "000000000000",
  "region": "us-east-1",
  "summary":{
    "total_orphans": len(findings),
    "estimated_monthly_waste_usd":sum(
      item["estimated_monthly_cost_usd"]
      for item in findings
      )
  },
  "findings": findings
}

#Saved report as report.json
with open("report.json","w") as f:
  json.dump(report,f,indent=2)

#Created Markdown Summary
with open("summary.md", "w") as f:
    f.write("# Cost Janitor Report\n\n")
   
    f.write(
        f"Total Findings: "
        f"{len(findings)}\n\n"
    )

    for finding in findings:

        f.write(
            f"## {finding['resource_type']}\n"
        )
        f.write(
            f"- Resource: "
            f"{finding['resource_id']}\n"
        )
        f.write(
            f"- Reason: "
            f"{finding['reason']}\n"
        )
        f.write(
            f"- Cost: $"
            f"{finding['estimated_monthly_cost_usd']}\n\n"
        )
          

#agar waste resource mila to pipeline break hojayega

if findings and args.dry_run:
    print(
        "[red]Orphans detected[/red]"
    )

    sys.exit(1)

print("[green]No issues found[/green]")

#Adding Scan Summary
print(
    f"[yellow]Total findings:"
    f" {len(findings)}[/yellow]"
)  