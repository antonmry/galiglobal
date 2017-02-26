title=How to persist your configuration in GKE
date=2017-01-09
type=post
tags=development,devops,gke,terraform
status=published
~~~~~~

In my previous post, [Deploy on Kubernetes GKE with Terraform](https://antonmry.github.io/post/deploy-on-kubernetes-gke-with-terraform/), we've seen how to start to use kubernetes but in a very simple way. The next thing we would like to do is persist the configuration, so we don't need to reconfigure our bot each time we start the cluster. This post explain how to do it from the configuration created in the previous one.

Again we'll use [Leanmanager bot](https://github.com/antonmry/leanmanager) but everything applies to any other system which needs to store configuration or data in a database. In the case of [Leanmanager](https://github.com/antonmry/leanmanager) we are using [Boltdb](https://github.com/boltdb/bolt), a pure Go key/value store. [Boltdb](https://github.com/boltdb/bolt) is great for development but it doesn't support to have more than one process opening the same database file, so it may be problematic if we want to have more than one Docker instance at the same time. Yet it's enough for our purposes and the process is similar for [Consul](https://www.consul.io/) which it's already in the Roadmap.

## Create your persistent disks

If we want to persist data, we are going to need a disk, that's common sense. In GCE we can do it very easily:

```sh
gcloud compute disks create --size 1GB leanmanager-disk
```

But again, we want to do it in an automated way with Terraform. Use the following file `leanmanager-disk.tf`:

```
variable "disk_name" {
  default = "leanmanager-disk"
}

resource "google_compute_disk" "default" {
name  = "${var.disk_name}"
  type  = "pd-ssd"
  zone = "${var.region}"
  size  = "1"
}
```

If you want to know more about it, visit the [Terraform Google_Compute_Disk reference documentation](https://www.terraform.io/docs/providers/google/r/compute_disk.html).

## Tell the container about the disk

In our previous post, we've launched the bot using `kubectl run`. This is OK for simple configuration but if we need to have something more complex, it doesn't scale. We can create a [pod](http://kubernetes.io/docs/user-guide/pods/), a group of one or more containers, using a YAML file like this:

```
apiVersion: v1
kind: Pod
metadata:
  name: leanmanager
  labels:
    name: leanmanager
spec:
  containers:
    - image: antonmry/leanmanager:latest
      name: leanmanager
      env:
        - name: LEANMANAGER_TOKEN
          value: LEANMANAGER_TOKEN_TEMPLATE
        - name: LEANMANAGER_PATHDB
          value: /mnt
      volumeMounts:
          # This name must match the volumes.name below.
        - name: leanmanager-persistent-storage
          mountPath: /mnt
  volumes:
    - name: leanmanager-persistent-storage
      gcePersistentDisk:
        # This disk must already exist.
        pdName: leanmanager-disk
        fsType: ext4
```

The file is auto-explanatory except the value `LEANMANAGER_TOKEN_TEMPLATE`. I don't want to hardcode the Token here because the file will be uploaded to Github. Instead of that, I want to use my local environment variable LEANMANAGER_TOKEN but this isn't supported yet in K8s, see [Kubernetes equivalent of env-file in Docker](http://stackoverflow.com/questions/33478555/kubernetes-equivalent-of-env-file-in-docker). 

So I've created a YAML template and in the Terraform file changed the last `local-exec` to:

```
  provisioner "local-exec" {
    command = "cp leanmanager-pod-template.yaml leanmanager.tmp.yaml && sed -i -- 's/LEANMANAGER_TOKEN_TEMPLATE/${var.LEANMANAGER_TOKEN}/g' leanmanager.tmp.yaml"
  }

  provisioner "local-exec" {
    command = "kubectl create -f leanmanager.tmp.yaml"
  }

  provisioner "local-exec" {
    command = "rm -f leanmanager.tmp.yaml"
  }
```

Basically, I'm replacing strings with `sed`. Other more sophisticate approaches are possible as K8s secrets or Ansible, but this is simple and enough for the task we want to do.

## Create the pod and test

Time to create the cluster and the pod:

```sh
terraform plan
terraform apply -var LEANMANAGER_TOKEN=$LEANMANAGER_TOKEN
```

The bot should connect. Now we can do some changes in the configuration, delete the pod:

```sh
kubectl delete pod leanmanager
```

Create it again:

```sh
kubectl create -f leanmanager.yaml
```

And check the status with the following commands and, once it's in *Running* state, see if everything has been persisted:

```sh
kubectl get pod leanmanager
kubectl logs leanmanager
```

## Conclusion

Persist data in Kubernetes is quite easy, even if you are going to do it automatically.

If you want to check all the files, the full project and the associated PR are in [Github](https://github.com/antonmry/leanmanager/pull/27/commits/ffea981b5deca5376b7bb8de1ed797da9aa282b0).

## Not already linked but useful resources

* [Kubernetes persistent volumes](http://kubernetes.io/docs/user-guide/persistent-volumes/)
* [Using Persistent Disks with WordPress and MySQL](https://cloud.google.com/container-engine/docs/tutorials/persistent-disk/)





