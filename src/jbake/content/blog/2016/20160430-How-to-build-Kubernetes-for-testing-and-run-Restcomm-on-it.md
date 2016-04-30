title=How to build Kubernetes for testing and run Restcomm on it
date=2016-04-30
type=post
tags=Kubernetes, Go, Restcomm
status=published
~~~~~~

In this post I'm going to show how to create a Kubernetes Development Environment and deploy Restcomm on it for testing. If you want just deploy RestComm, it's better for you use the [Kubernetes Docker option](http://kubernetes.io/docs/getting-started-guides/docker/), instead of doing all this process.

# Install Go Development Environment

```sh
curl -O https://storage.googleapis.com/golang/go1.6.linux-amd64.tar.gz
tar -zxvf go1.6.linux-amd64.tar.gz
mv go ~/Software/
echo "GOROOT=~/Software/go" >> .bash_profile 
echo "export GOROOT" >> .bash_profile 
echo "PATH=\$GOROOT/bin:\$PATH" >> ~/.bash_profile
echo "export PATH" >> ~/.bash_profile
echo "GOPATH=~/Workspace/Telestax/go_kubernetes" >> ~/.bash_profile
echo "export GOPATH" >> ~/.bash_profile
source ~/.bash_profile
mkdir -p $GOPATH
```

# Basic Kubernetes installation

## Clone and download

```sh
mkdir -p $GOPATH/src/k8s.io
cd $GOPATH/src/k8s.io
git clone https://github.com/antonmry/kubernetes.git
cd kubernetes
git remote add upstream 'https://github.com/kubernetes/kubernetes.git'
```

## Build and unit test

```sh
./hack/build-go.sh && notify-send "Compilation done"
```

Note! Integration test take a long time.

```sh
./hack/test-go.sh && notify-send "Test done"
```

## Integration test

We need etcd to run the integration test, Docker to the rescue?

```sh
docker run -d --name etcd quay.io/coreos/etcd:v2.3.3
alias etcdctl="docker exec etcd /etcdctl"
alias etcd="docker exec etcd /etcd"
```

Nop, it fails because kubernetes look for it in the PATH :-(

So,

```sh
curl -O  https://github.com/coreos/etcd/releases/download/v2.3.3/etcd-v2.3.3-linux-amd64.tar.gz 
tar xzvf etcd-v2.3.3-linux-amd64.tar.gz
mv etcd-v2.3.3-linux-amd64/ ~/Software/
echo "PATH=~/Software/etcd-v2.3.3-linux-amd64:\$PATH" >> ~/.bash_profile
echo "export PATH" >> ~./bash_profile
source ~./bash_profile
```
And now, time to test. Be careful, I think it uses your Google Cloud account :-S

```sh
go run hack/e2e.go -v --build --up --test --down && notify-send "Integration test done"
```

# Running the Restcomm image

## Creating and launching the cluster

It will ask for sudo permission, you have to be quick, or relaunch.

```sh
hack/local-up-cluster.sh
```

Let this terminal open and create a new one (tmux's time?)

## Running the container

We don't have any container running:

```sh
cluster/kubectl.sh get pods
cluster/kubectl.sh get services
cluster/kubectl.sh get deployments
```

Time to launch RestComm:

```sh
curl -O https://gist.githubusercontent.com/antonmry/0ab69e95e61617eb957a79beb25ba30b/raw/c5c2979be63297571968f7db88c27e714e557fca/restcomm_rc.yml
vim restcomm_rc.yml 
```

Change STATIC_ADDRESS to your own IP address.

```sh
cluster/kubectl.sh create -f restcomm_rc.yml
```

Now we should be able to see our docker instance working, pods and so on.

```sh
cluster/kubectl.sh get services
cluster/kubectl.sh get deployments
cluster/kubectl.sh get pods
```

We have to wait the STATUS pod become running instead of ContainerCreating.

After that, we can see our RestComm containers running:


```sh
docker images
docker ps
```

Once it's running, we can expose the ports to access our instance:

```sh
wget -O https://gist.githubusercontent.com/antonmry/0ab69e95e61617eb957a79beb25ba30b/raw/77c4eea558fcba9a1ad09d9b89221fdbe3a263fe/restcomm_service.yml
vim restcomm_service.yml
```

Change externalIPs to your own IP address.

```sh
cluster/kubectl.sh create -f restcomm_service.yml
```

With the following command we can check the status:

```sh
./cluster/kubectl.sh get svc
```

# Test Restcomm!

```sh
chromium-browser https://CHANGE_WITH_YOUR_IP/olympus
```

Login as alice, call +1234 and you should listen the message ;-)

# Stop all

```sh
./cluster/kubectl.sh delete service restcomm-service
./cluster/kubectl.sh delete rc restcomm-core-controller
```

And Ctrl+C in the terminal running the cluster.

# Reference documentation

- [Creating a Custom Cluster from Scratch](http://kubernetes.io/docs/getting-started-guides/scratch/)
- [Kubernetes Development Guide](https://github.com/kubernetes/kubernetes/blob/master/docs/devel/development.md)
- [Running Kubernetes Locally with No VM](http://kubernetes.io/docs/getting-started-guides/locally/)
- [Kubernetes and RestComm by adimania](https://github.com/adimania/Restcomm-Docker/blob/master/kubernetes/README.md)
