# Add components to OpenShift

Ansible to configure https://try.openshift.com[OpenShift] cluster for Red Hat Developer Workshops and Demos.

The role can also be used to install and configure:

- [x] Red Hat OpenShift Serverless both Serving and Eventing

- [x] [Red Hat OpenShift Pipelines](https://www.openshift.com/learn/topics/pipelines)

- [x] [Argo CD](https://argoproj.github.io/argo-cd/)

- [x] [Red Hat OpenShift Service Mesh](https://www.openshift.com/learn/topics/service-mesh)

- [x] [Red Hat AMQ Streams](https://www.redhat.com/en/resources/amq-streams-datasheet)

- [x] [Red Hat Advanced Cluster Management for Kubernetes]
(https://www.redhat.com/en/technologies/management/advanced-cluster-management)
- [x] [Apache Camel-K](https://camel.apache.org/docs/#camel-k)

- [ ] [Red Hat Code Ready Workspaces](https://www.redhat.com/en/technologies/jboss-middleware/codeready-workspaces)

## Role Variables

| Variable Name| Description   | Default value |
| :---        |    :---   |         :----: |
| download_clients | Download OpenShift clients oc, kubectl and openshift-install | True|
|ocp_bin_dir| Directory to download and install Openshift clients. The directory will be created if not exist| $HOME/openshift/bin |
|ocp_version|The minimum OpenShift version to use | 4.5.6 |
| deploy_serverless| Deploy OpenShift Serverless| True |
| serverless_subcription_channel| The Operator Channel for the Serverless Subscription| 4.5 |
| knative_serving_cr | The Knative Serving Custom Resource| serverless/cr/serving.yaml |
| knative_eventing_cr | The Knative Eventing Custom Resource | serverless/cr/eventing.yaml |
| deploy_pipelines | Deploy OpenShift Pipelines | False |
| deploy_argocd | Deploy Argo CD | False |
| argocd_cr | The Argo CD Custom resource | argocd/cr.yaml |
| argocd_release_channel | The Argo CD Release Channel | alpha |
| deploy_acm | Deploy Advanced Cluster Management for Kubernetes(ACM) | False |
| acm_cr | The ACM Custom resource | acm/cr.yaml |
| acm_release_channel | The ACM Release Channel | release-2.0 |
| deploy_servicemesh | Deploy OpenShift Pipelines | False |
| servicemesh_es_channel | The Operator Channel for the Red Hat Elastic Search Subscription| 4.5 |
| servicemesh_cr | The Red Hat Servicemesh Custom resource | servicemesh/cr.yaml |
| servicemesh_members | Create and add projects Servicemesh | |
| deploy_kafka | Deploy Apache Kafka using Strimzi | False |
| kakfa_cluster_name | The Apache Kafka cluster name | my-cluster |
| kakfa_cluster_namespace | The Apache Kafka cluster namespace | kafka |
| strimzi_kafka_cr | Apache Kafka Strimzi Custom Resource | kafka/cr.yaml |
| knative_eventing_kafka_cr | Knative Eventing KafkaSource Custom Resource | kafka/eventing/cr.yaml |
| deploy_camel_k | Deploy Apache Camel-K | False |
| deploy_che | Deploy Eclipse Che | False |
| eclipse_che_cr | The Eclipse Che Custom resource | che/cr.yaml |
| deploy_acm | Deploy RedHat Advanced Cluster Management for Kubernetes | False |
| users | Create OpenShift users and Cluster Administrator | |

## Example Playbooks

The [examples](https://github.com/kameshsampath/kameshsampath.demos/tree/master/roles/openshift_spices/examples) directory has various playbook examples to get started using this role:

e.g. 

If you want to deploy OpenShift Serverless with Pipelines run:

```shell
ansible-playbook examples/serverless_pipelines.yml
```
----

If you don't have Ansible installed locally, you can use the project [OpenShift Demos Ansible EE](https://github.com/kameshsampath/openshift-demos-ansible-ee) to run the playbooks using Docker and [Ansible Runner](https://ansible-runner.readthedocs.io/en/latest/).
