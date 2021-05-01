title=Deploy on kubernetes GKE with Terraform
date=2017-01-06
type=post
tags=kubernetes,gke,terraform,devops
status=published
---------

Writing a new post after six months and in Christmas... New year, new promises, old projects. I've been quite busy the second half of 2016, but also very happy and satisfied with some personal and professional projects. No more excuses and let's focus in this post.

## Introduction

I want to deploy my [leanmanager Docker image](https://hub.docker.com/r/antonmry/leanmanager) so the bot is available all the time for the team, but you can choose any Docker image you want to use. I want to use [Google Container Engine](https://cloud.google.com/container-engine/docs/quickstart) Kubernetes implementation and do it everything as much automatic as possible using Terraform.

## GCE installation

First step, make sure you've created previously a project in the Google Cloud console. If you don't have the Cloud SDK, you are going to need it. It's quite easy to install following [the Google instructions](https://cloud.google.com/sdk/docs/quickstart-linux):

```sh
cd ~/Software
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-138.0.0-linux-x86_64.tar.gz
tar -zxvf google-cloud-sdk-138.0.0-linux-x86_64.tar.gz
rm google-cloud-sdk-138.0.0-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh
```

**Note**: be careful, last command modifies your .bashrc and it may cause problems.

Now, it's time to log in:

```sh
gcloud init
```

And now, install kubectl, the client to manage kubernetes:

```sh
gcloud components install kubectl
```

## Launching the service

The first step is to create the cluster. It may take some time.

```sh
gcloud container clusters create leanmanager-cluster
```

Ensure kubectl can access to the service:

```sh
gcloud auth application-default login
```

And now, it's time to launch the leanmanager image:

```sh
kubectl run leanmanager-node --image=antonmry/leanmanager:latest --env="LEANMANAGER_TOKEN=$LEANMANAGER_TOKEN"
```

**Note:** I have an environment variable `LEANMANAGER_TOKEN` with the token to authenticate to Slack. The bot automatically connects using Websocket but if you want to expose any service, add `--port=8080` to allow access to it. You will need also to create a Load Balancer, the steps are explained [here](https://cloud.google.com/container-engine/docs/quickstart).


## Clean the service

To stop the service and delete the cluster:

```sh
gcloud container clusters delete leanmanager-cluster
```

## Install Terraform

Our next step it's going to be to automate all the process. To do it, we'll use [Terraform](https://www.terraform.io).

If you don't have it, first step is download it from [here](https://www.terraform.io/downloads.html) and install it. For linux:

```sh
curl -O https://releases.hashicorp.com/terraform/0.8.2/terraform_0.8.2_linux_amd64.zip
unzip terraform_0.8.2_linux_amd64.zip
```

Now move it to a folder which is in your PATH, in my case:

```sh
terraform ~/bin/
echo terraform >> ~/bin/.gitignore
```

Last command is executed because I've `~/bin` in github but I don't want upload a so big file as `terraform` executable.

Now you should be able to use `terraform` in your system. If you've never used before, it's a good moment to read the [Getting started guide](https://www.terraform.io/intro/getting-started/build.html).

## Download GKE credentials

Follow these instructions to download the credentials file:

1. Log into the [Google Developers Console](https://console.cloud.google.com) and select a project.
2. Click the menu button in the top left corner, and navigate to "IAM & Admin", then "Service accounts", and finally "Create service account".
3. Provide a name and ID in the corresponding fields, select "Furnish a new private key", and select "JSON" as the key type.
4. Clicking "Create" will download your credentials.
5. Rename it to `account.json`. Make sure you don't publish this file, for instance in Github (add it to `.gitignore`).

## Create the cluster using Terraform

In the same folder you have your `account.json`, create a Terraform file like `leanmanager.tf`:

```
variable "region" {
  default = "europe-west1-d"
}

provider "google" {
  credentials = "${file("account.json")}"
  project     = "wwwleanmanagereu"
  region      = "${var.region}"
}

resource "google_container_cluster" "primary" {
  name = "leanmanager-cluster"
  zone = "${var.region}"
  initial_node_count = 1

  master_auth {
    username = "mr.yoda"
    password = "testTest1"
  }

  node_config {
    oauth_scopes = [
      "https://www.googleapis.com/auth/compute",
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring"
    ]
  }
}
```

Check what it's going to create:

```sh
terraform plan
```

Review the output and if it's ok, launch it!.

```sh
terraform apply
```

If everything goes well, you will see a message like this:

> Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

And you can check it with:

```sh
gcloud container clusters list
```

If you want to access with `kubectl` you need to login first:

```
gcloud container clusters get-credentials leanmanager-cluster --zone europe-west1-d
kubectl cluster-info
```

This step can be added to the `leanmanager.tf` inside the `resource` block:

```
provisioner "local-exec" {
    command = "gcloud container clusters get-credentials ${var.cluster_name} --zone ${google_container_cluster.primary.zone}"
}
```

## Launch our Docker instance

Once you are logged in with `kubectl`, it's exactly the same as before:

```sh
kubectl run leanmanager-node --image=antonmry/leanmanager:latest --env="LEANMANAGER_TOKEN=$LEANMANAGER_TOKEN"
```

But you can also do it with Terraform adding this snippet in the beginning: 

```
variable "LEANMANAGER_TOKEN" {
      default = "USE YOUR OWN TOKEN"
}
```

And after the previous `local-exec`:

```
provisioner "local-exec" {
    command = "kubectl run leanmanager-node --image=antonmry/leanmanager:latest --env=LEANMANAGER_TOKEN=${var.LEANMANAGER_TOKEN}"
}
```

And executing terraform passing the variable:

```sh
terraform apply -var LEANMANAGER_TOKEN=$LEANMANAGER_TOKEN
```

Other option would be read the variable directly but you have to change the name to fit the terraform requirements and I'm using it for other things. More info [here](https://www.terraform.io/docs/configuration/variables.html).

## Clean everything

With Terraform is really easy, just:

```sh
terraform destroy
```

## Not already linked but useful resources

* [Simple GCE setup Terraform](http://container-solutions.com/simple-gce-setup-terraform/)
* [terraform-gke](https://github.com/l337ch/terraform-gke)
* [kubestack](https://github.com/kelseyhightower/kubestack)
* [Automated Image Builds with Jenkins, Packer, and Kubernetes](https://cloud.google.com/solutions/automated-build-images-with-jenkins-kubernetes)
