title=Kubernetes installation with Route 53 DNS and HTTPS load balancer
date=2019-04-04
type=post
tags=Kubernetes, Amazon, Docker
status=published
~~~~~~

## Introduction

This post explains how to deploy a Kubernetes cluster in Amazon. We want to automatically update Route 53 to use our own domain and use [AWS ELB](https://aws.amazon.com/elasticloadbalancing/) to have Load Balancing to our pods. We'll use also [AWS Certificate Manager (ACM)](https://aws.amazon.com/certificate-manager/) so our pods open internally HTTP endpoints but externally they expose HTTPS with a proper certificate.

## Installation

Install awscli and [kops](https://github.com/kubernetes/kops#installing).

```
export bucket_name=test-kops
export KOPS_CLUSTER_NAME=k8s.test.net
export KOPS_STATE_STORE=s3://${bucket_name}

aws s3api create-bucket --bucket ${bucket_name} --region eu-west-1 --create-bucket-configuration LocationConstraint=eu-west-1
aws s3api put-bucket-versioning --bucket ${bucket_name} --versioning-configuration Status=Enabled

kops create cluster \
--node-count=1 \
--node-size=t2.medium \
--zones=eu-west-1a \
--dns-zone test.net \
--cloud-labels="Department=TEST" \
--name=${KOPS_CLUSTER_NAME}

kops edit cluster --name ${KOPS_CLUSTER_NAME}
```

Add to the end:

```yaml
  additionalPolicies:
     node: |
       [
           {
               "Effect": "Allow",
               "Action": "route53:ChangeResourceRecordSets",
               "Resource": "*"
           },
           {
               "Effect": "Allow",
               "Action": "route53:ListHostedZones",
               "Resource": "*"
           },
           {
               "Effect": "Allow",
               "Action": "route53:ListResourceRecordSets",
               "Resource": "*"
           }
       ]
```

and create the cluster executing: 

```
kops update cluster --name ${KOPS_CLUSTER_NAME} --yes
kops rolling-update cluster
``` 

It takes some time. Use `kops validate cluster` to validate it. More options:

 * validate cluster: kops validate cluster
 * list nodes: kubectl get nodes --show-labels
 * ssh to the master: ssh -i ~/.ssh/id_rsa admin@api.k8s.test.net
 * the admin user is specific to Debian. If not using Debian please use the appropriate user based on your OS.
 * read about installing addons at: https://github.com/kubernetes/kops/blob/master/docs/addons.md.

### Deploy the dashboard
 
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/aio/deploy/recommended/kubernetes-dashboard.yaml
kubectl proxy &
kops get secrets kube --type secret -oplaintext
```
 
Open http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login
 
Click on Token and introduce the following output:
 
 ```
kops get secrets admin --type secret -oplaintext
 ```

### Configure DNS

Note: avoid route53-mapper, it's deprecated. The kops documentation is outdated.

Obtain the zone ID for your Hosted Zone (you should create a new one if you don't have one, consult
[here](https://github.com/kubernetes-incubator/external-dns/blob/master/docs/tutorials/aws.md#set-up-a-hosted-zone) how to do it):

```
aws route53 list-hosted-zones-by-name --output json --dns-name "test.net." | jq -r '.HostedZones[0].Id'
```

In our case, it returns `/hostedzone/AAAAAA`.

Create a new file external-dns.yml and update your data in the end: 

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: external-dns
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
  name: external-dns
rules:
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get","watch","list"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get","watch","list"]
- apiGroups: ["extensions"] 
  resources: ["ingresses"] 
  verbs: ["get","watch","list"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["list"]
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: external-dns-viewer
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: external-dns
subjects:
- kind: ServiceAccount
  name: external-dns
  namespace: default
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: external-dns
spec:
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: external-dns
    spec:
      serviceAccountName: external-dns
      containers:
      - name: external-dns
        image: registry.opensource.zalan.do/teapot/external-dns:latest
        args:
        - --source=service
        - --source=ingress
        - --domain-filter=test.net 
        - --provider=aws
          #- --policy=upsert-only # would prevent ExternalDNS from deleting any records, omit to enable full synchronization
        - --aws-zone-type=public # only look at public hosted zones (valid values are public, private or no value for both)
        - --registry=txt
        - --txt-owner-id=AAAAAA
```

and deploy it:

```
kubectl apply -f external-dns.yml
```

## Test your configuration with an example:

Create an AWS certificate for the service:

```
aws acm request-certificate \
--domain-name nginx.test.net \
--validation-method DNS \
--idempotency-token 1234 
```

and save the `CertificateArn`. We'll use it later.

You will need to validate it. The easier way it's from the AWS web console as explained [in the official documentation](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html).

Create `nginx-d.yml`:

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx
spec:
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx
        name: nginx
        ports:
        - containerPort: 80
          name: http
```

and `nginx-svc.yml` with the domain you would like to use and the ACM certificate.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  annotations:
    external-dns.alpha.kubernetes.io/hostname: nginx.test.net.
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: arn:aws:acm:eu-west-1:888888:certificate/AAAAAA-BBBBB-CCCCC-DDDDD
    service.beta.kubernetes.io/aws-load-balancer-backend-protocol: http
    service.beta.kubernetes.io/aws-load-balancer-ssl-ports: "443"
spec:
  type: LoadBalancer
  ports:
  - port: 80
    name: http
    targetPort: 80
  - name: https
    port: 443
    targetPort: http
  selector:
    app: nginx
```

and deploy them:

```
kubectl apply -f nginx-d.yml -d nginx-svc-yml
```

It would take some minutes. Once the pods are ready, you should be able to open in your browser on `http://nginx.test.net`
and `https://nginx.test.net` and see the nginx welcome page.

##  Clean everything

Delete the ACM certificate and execute:

```
kops delete cluster --name k8s.test.net --yes
```

## Resources

- [Kops IAM roles](https://github.com/kubernetes/kops/blob/master/docs/iam_roles.md)
- [Setting up ExternalDNS for Services on AWS](https://github.com/kubernetes-incubator/external-dns/blob/master/docs/tutorials/aws.md)
- [How to Create a Kubernetes Cluster on AWS in Few Minutes](https://medium.com/containermind/how-to-create-a-kubernetes-cluster-on-aws-in-few-minutes-89dda10354f4)
- [External HTTP/HTTPS Server on Kubernetes in AWS](https://medium.com/@jkinkead/external-http-https-server-on-kubernetes-in-aws-9b182328fff1)

