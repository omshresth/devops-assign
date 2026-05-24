terraform {
    required_providers{
        aws={
            source="hashicorp/aws"
            version="~> 5.0"

        }
    }
}

provider "aws" {
    region = var.aws_region
    access_key = "test"
    secret_key = "test" 

    skip_credentials_validation= true
    skip_metadata_api_check=true
    skip_requesting_account_id=true 

    s3_use_path_style = true
    
    endpoints{
        ec2="http://localhost:4566"
        s3="http://localhost:4566"
    }
    
}



module "network" {
    source="./modules/network"
    project     = var.project
    environment = var.environment
    owner       = var.owner
}



resource "aws_security_group" "my_sg"{
 name="my-sg"
 vpc_id= module.network.vpc_id
 
 ingress{ 
    from_port =80
    to_port=80
    protocol="tcp"
    cidr_blocks=["0.0.0.0/0"]
      }

 ingress{
    from_port=443
    to_port=443
    protocol="tcp"
    cidr_blocks=["0.0.0.0/0"]
      }

ingress{
    from_port=22
    to_port=22
    protocol="tcp"
    cidr_blocks=["0.0.0.0/0"]
     }

}

resource "aws_instance" "Myserver"{
    count= 2
    ami="ami-12345678"
    instance_type = "t3.micro"
    subnet_id = module.network.public_subnet1
    vpc_security_group_ids=[aws_security_group.my_sg.id]

tags={
  Name ="Myserver-${count.index}"
  Project     = var.project
  Environment = var.environment
  Owner       = var.owner
  ManagedBy   = "terraform"
   }    
}

resource "aws_s3_bucket" "logs" {
    bucket ="nimbuskart-logs"

tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
   }
}

resource "aws_s3_bucket_versioning" "versioning"{
    bucket=aws_s3_bucket.logs.id

    versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "lifecycle" {
  count = var.enable_lifecycle ? 1 : 0
  bucket = aws_s3_bucket.logs.id

  rule {
    id     = "cleanup"
    status = "Enabled"
    filter {}

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}


resource "aws_ebs_volume" "orphan"{
  availability_zone = "us-east-1a"
  size = 10

  tags = {
    Name = "orphan-volume"
  }
}

