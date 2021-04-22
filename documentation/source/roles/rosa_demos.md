# Ansible Role ROSA Demos

Set of Ansible scripts and execution environment that can be used to setup AWS resources that will be used as part of the [ROSA](https://aws.amazon.com/rosa/) demos.

You can do the following with this Ansible role:

- [x] Setup AWS OIDC Provider

- [x] Setup AWS DynamoDb Provider

- [x] Setup AWS RDS PostgreSQL Database with its own VPC

- [x] Setup VPC Peering with AWS RDS PostgreSQL and ROSA

__NOTE__
  
  For Windows it's recommended to use Windows Subsystem for Linux (WSL)

## Role Variables


| Variable Name| Description   | Default value |
| :---        |    :---   |         :----: |
| aws_region | The default AWS region to use for creating the resources | us-west-2
| oidc_bucket_name | The s3 bucket used for holding the OpenId connect provider assets | rosa-demos-oidc
| rosa_demo_role_name | The AWS IAM role that will be used as part of the Demos | ROSADemosRole
| rosa_demo_policy_name | The AWS IAM policy that will be used to control what the Kubernetes Service Accounts can do | ROSADemosPolicy |
| rollback | Clean up all the created AWS resources | False |
| iam | Create OpenId Connect Provider and create IAM resources | False |
| create_aws_credentials_file | Create AWS Credential file | True |
| dynamodb | Create AWS DynamoDB  | false |
| dynamodb_table_name | The DynamoDB Table name to use  | Fruits |
| rds | Create AWS RDS | false |
| rds_database_name | The RDS Database name | fruitsdb |
| rds_instance_id | The RDS Instance id  | rosa-demos |
| rds_database_user_name | The RDS Database user name to connect to  | rosademosrole |
| rds_vpc_name | The RDS Database VPC name  | rosa-demos-rds-vpc |
| rds_vpc_host | The RDS Database VPC Host  | "192.168.0.0" |
| rds_vpc_cidr | The RDS Database VPC Host CIDR  | "192.168.0.0/16" |
| rds_vpc_subnet_prefix | The RDS Database VPC subnet prefix | "24" |
| rds_db_engine | The RDS Database DB Engine | postgres |
| rds_db_engine_version | The RDS Database DB Engine version | "12.5" |
| rds_master_username | The RDS Database DB master user | postgres |
| rds_master_password | The RDS Database DB master user password | postgres123 |
| rds_db_instance_type | The RDS Database DB instance type | db.t2.micro |
| rds_subnet_group | The RDS Database DB subnet group | rosa-demos-rds-vpc-subnets-group |
| rds_vpc_peering | Enable VPC peering between RDS and ROSA | true |
| rds_iam_database_authentication| Enable RDS IAM authentication | true |
| rosa_to_rds_vpc_peering | Enable ROSA - RDS VPC peering | true |
| rosa_cluster_name | The ROSA cluster name. The scripts will fail when `rosa_cluster_name` is not defined |  |

## Example Playbooks

The [examples](https://github.com/kameshsampath/kameshampath.demos/tree/master/roles/rosa_demos/examples) directory has various playbook examples to get started using this role:

e.g. 

If you want to set up OpenId Connect Provider with a Policy and Role:

```shell
  ansible-playbook examples/oidc_setup.yml
```

If you don't have Ansible installed locally, you can use the project [OpenShift Demos Ansible EE](https://github.com/kameshsampath/openshift-demos-ansible-ee) to run the playbooks using Docker and [Ansible Runner](https://ansible-runner.readthedocs.io/en/latest/).
