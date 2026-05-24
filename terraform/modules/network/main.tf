//VPC
resource "aws_vpc" "myvpc"{
    cidr_block = "10.20.0.0/16"
    tags={
        Environment=var.environment
        Project=var.project
        Owner=var.owner
        ManagedBy   = "terraform"
}
}

//SUBNETS
resource "aws_subnet" "public_subnet1"{
    vpc_id= aws_vpc.myvpc.id
    cidr_block="10.20.1.0/24"
    availability_zone="us-east-1a"

    tags= {
        name="public_subnet1"
    }
}

resource "aws_subnet" "public_subnet2"{
    vpc_id= aws_vpc.myvpc.id
    cidr_block="10.20.2.0/24"
    availability_zone="us-east-1b"
    
    tags={
        name="public_subnet2"
    }
}