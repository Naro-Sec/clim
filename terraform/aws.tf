terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
  required_version = ">= 0.14.9"
}

provider "aws" {
  region     = "us-east-1"
}

resource "aws_security_group" "clim_sg" {
  name = "Allow_all_traffic"
  vpc_id = "vpc-0c39fa89a428572a6"
  egress = [
    {
      cidr_blocks      = [ "0.0.0.0/0", ]
      description      = ""
      from_port        = 0
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      protocol         = "-1"
      security_groups  = []
      self             = false
      to_port          = 0
    }
  ]
  ingress                = [
   {
     cidr_blocks      = [ "0.0.0.0/0", ]
     description      = ""
     from_port        = 0
     ipv6_cidr_blocks = []
     prefix_list_ids  = []
     protocol         = "-1"
     security_groups  = []
     self             = false
     to_port          = 0
  }
  ]
}

# creating public key
resource "aws_key_pair" "clim" {
  key_name   = "clim_key"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC06dmTMtG0nP4iXGWivibTy/yf0mOqen2eQMgvX0Mq5Z+QbOp4BgpoSmuqXQw7OPR8v29Kcf0RN16v/M4FdKDgIpsm2c1mP7O5ot+bG5faOW5yuhPWzqExPjt+ylwkiiyerdDnCEunTN9gWdy6w5BER8KHQwMNY4HglrB+aLmMmM59zNwr3jx/mYaklM5LTM9nt3rSTNEOVxRK8XMthClMjvCq9NMHJx8seNgKpe9TF/Ue7xtwnSMgK5jr9a5u0Kbe+7Io16s3zs7IYMWN/Al3y/O9XHGGhYEfeqnN6PUiuspqsxd0m6ihBnptm6dan/+NP44jnhz5oIsqNe1YT3O9 furkan@LAPTOP-EPVA9UP1"
}

#creation of ubuntu instance this is the DNS server
resource "aws_instance" "dns_server" {
  ami             = "ami-007855ac798b5175e"
  instance_type   = "t2.micro"
  key_name        = "clim_key"
  private_ip      = "172.31.1.5"
  subnet_id       = "subnet-0d00cc0538b609973"
  security_groups = [aws_security_group.clim_sg.id]

  connection {
    type        = "ssh"
    host        = self.public_dns
    user        = "ubuntu"
    private_key = file("/home/narek/.aws/furkan_aws_private_key.pem")
    timeout     = "4m"
  }
  tags = {
    Name = "ns1.clim.test"
  }

  provisioner "file" {
    source      = "/home/narek/config_files/named.conf.local"
    destination = "/tmp/named.conf.local"
  }
  provisioner "file" {
    source      = "/home/narek/config_files/named.conf.options"
    destination = "/tmp/named.conf.options"
  }
  provisioner "file" {
    source      = "/home/narek/config_files/db.clim.test"
    destination = "/tmp/db.clim.test"
  }
  provisioner "file" {
    source      = "/home/narek/config_files/resolved.conf"
    destination = "/tmp/resolved.conf"
  }
  provisioner "file" {
    source      = "/home/narek/requirements.txt"
    destination = "/tmp/requirements.txt"
  }
  provisioner "remote-exec" {
      inline = [
        "sudo apt-get update ",
        "sudo apt-get install bind9 bind9utils bind9-dnsutils bind9-doc bind9-host python3 python3-pip git -y",
        "pip3 install --upgrade pip",
        "pip3 install --upgrade setuptools",
        "cd /tmp && pip3 install -r requirements.txt",
        "sudo hostnamectl set-hostname ns1.clim.test",
        "sudo cp /tmp/named.conf.local /etc/bind/named.conf.local",
        "sudo cp /tmp/named.conf.options /etc/bind/named.conf.options",
        "sudo cp /tmp/db.clim.test /var/lib/bind/db.clim.test",
        "sudo cp /tmp/resolved.conf /etc/systemd/resolved.conf",
        "cd ~/ && git clone https://github.com/furkkzz/CLIM.git",
        "sudo systemctl enable bind9",
        "sudo systemctl start bind9",
        "sudo ufw allow in from 172.31.0.0/20 to any port 53",
        "sudo systemctl restart systemd-resolved",
        "sudo ufw allow Bind9",
        "sudo systemctl restart bind9"
      ]
  }
}

#creation of ubuntu instance
resource "aws_instance" "client1" {
  ami             = "ami-007855ac798b5175e"
  instance_type   = "t2.micro"
  key_name        = "clim_key"
  subnet_id       = "subnet-0d00cc0538b609973"
  security_groups = [aws_security_group.clim_sg.id]
  private_ip      = "172.31.1.6"

  connection {
    type        = "ssh"
    host        = self.public_dns
    user        = "ubuntu"
    private_key = file("/home/narek/.aws/furkan_aws_private_key.pem")
    timeout     = "4m"
  }
  tags = {
    Name = "client1.clim.test"
  }

  provisioner "file" {
    source      = "/home/narek/config_files/resolv.conf"
    destination = "/tmp/resolv.conf"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo hostnamectl set-hostname client1.clim.test",
      "sudo cp /tmp/resolv.conf /etc/resolv.conf"
    ]
  }
}

#creation of ubuntu instance
resource "aws_instance" "client2" {
  ami                    = "ami-007855ac798b5175e"
  instance_type          = "t2.micro"
  key_name               = "clim_key"
  subnet_id              = "subnet-0d00cc0538b609973"
  security_groups        = [aws_security_group.clim_sg.id]
  private_ip             = "172.31.1.7"

  connection {
    type        = "ssh"
    host        = self.public_dns
    user        = "ubuntu"
    private_key = file("/home/narek/.aws/furkan_aws_private_key.pem")
    timeout     = "4m"
  }
  tags = {
    Name = "client2.clim.test"
  }

  provisioner "file" {
    source      = "/home/narek/config_files/resolv.conf"
    destination = "/tmp/resolv.conf"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo hostnamectl set-hostname client2.clim.test",
      "sudo cp /tmp/resolv.conf /etc/resolv.conf"
    ]
  }
}

resource "aws_instance" "client3" {
  ami             = "ami-0e38fa17744b2f6a5"
  instance_type   = "t2.medium"
  key_name        = "clim_key"
  subnet_id       = "subnet-0d00cc0538b609973"
  security_groups = [aws_security_group.clim_sg.id]
  private_ip      = "172.31.1.8"

  tags = {
    Name = "client3.clim.test"
  }
}