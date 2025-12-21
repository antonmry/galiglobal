# Developing in RestComm? Docker to the rescue

*08 May 2016*

I'm not a RestComm expert but I like to document the steps when I do something.
It's quite schematic but yet, it may help someone. Start to contribute to
RestComm is really hard because the lack of documentation and all the team very
busy. But it's a interesting project and a nice community.

The idea is quite simple: show how how create two PRs: one for Restcomm-Docker,
another for Restcomm-Connect.

## What do you need?

1. Java 7 development environment
2. Ant and maven
3. docker

So, what is the first step to become a RestComm maniac?

## Download the source code

The easy part, I love github:

```sh
git clone git@github.com:antonmry/Restcomm-Connect.git
git clone git@github.com:antonmry/Restcomm-Docker.git
cd Restcomm-Docker/
git remote add upstream git@github.com:RestComm/Restcomm-Docker.git
cd ../Restcomm-Connect/
git remote add upstream git@github.com:RestComm/Restcomm-Connect.git
```

If you've done it previously, it's a good moment to sync with the official
respository:

```sh
git fetch upstream
git checkout master
git merge upstream/master
git push
```

## RestComm-Docker

Now we are going to set up the RestComm environment: docker to the rescue!

I always create a local branch to do my work:

```sh
cd ../Restcomm-Docker/
git checkout -b s3bucketRegion#1
git push -u origin s3bucketRegion#1
```

```sh
docker build -t restcomm/yourname:latest -f Dockerfile .

docker run -i -d -v /var/log/restcomm/:/var/log/restcomm/ -e VOICERSS_KEY="CREATE A NEW ONE" -e S3_ACCESS_KEY="ONLY IF YOU USE IT" -e S3_SECURITY_KEY="ONLY IF YOU USE IT" -e S3_BUCKET_NAME="ONLY IF YOU USE IT" -e STATIC_ADDRESS="YOUR ETH0 IP?" -e ENVCONFURL="https://raw.githubusercontent.com/RestComm/Restcomm-Docker/master/scripts/restcomm_env_locally.sh" -p 80:80 -p 443:443 -p 9990:9990 -p 5060:5060 -p 5061:5061 -p 5062:5062 -p 5063:5063 -p 5060:5060/udp -p 65000-65050:65000-65050/udp restcomm/yourname:latest
```

We "enter" inside the docker instance:

```sh
docker ps
docker exec -it bfed9c0195f51c089b5edc001e48c31f4fb374a90a781f02f9c514a691fa6933 /bin/bash
```

To copy the deployments folder:

```sh
cd /opt/Restcomm-JBoss-AS7/standalone/deployments/
tar -cvf /tmp/deployments.tar *
exit
```

We leave the container and extract the deployment folder in your system:

```sh
docker cp bfed9c0195f51c089b5edc001e48c31f4fb374a90a781f02f9c514a691fa6933:/tmp/deployments.tar .
mkdir deployments 
mv deployments.tar deployments
rm deployments.tar
```

Launch docker with the new folder as its deployment folder:

```sh
docker stop bfed9c0195f51c089b5edc001e48c31f4fb374a90a781f02f9c514a691fa6933

docker run -i -d -v /var/log/restcomm/:/var/log/restcomm/ -v /home/antonmry/Workspace/Telestax/deployments:/opt/Restcomm-JBoss-AS7/standalone/deployments -e VOICERSS_KEY="xxx" -e S3_ACCESS_KEY="xxx" -e S3_SECURITY_KEY="xxx" -e S3_BUCKET_NAME="xxx" -e STATIC_ADDRESS="your eth0 IP?" -e ENVCONFURL="https://raw.githubusercontent.com/RestComm/Restcomm-Docker/master/scripts/restcomm_env_locally.sh" -p 80:80 -p 443:443 -p 9990:9990 -p 5060:5060 -p 5061:5061 -p 5062:5062 -p 5063:5063 -p 5060:5060/udp -p 65000-65050:65000-65050/udp restcomm/yourname:latest
```

Time to make your changes in the Dockerfile. Once they are done, build the image
and test. To upload it to github, first upload to your repository:

```sh
git add file1 file2
git commit -m "Descriptive message please"
git push
```

In github, open a Request using as Base the official repository and as a Head
Fork your branch. Usually I add a "Closes #xx" to the end of the title, where xx
is the number of the issue you are solving. It helps if you are using
[Waffle](http://www.waffle.io), a great service to organize your issues
following agile methodologies.

## RestComm-Connect

Ok, we have our Restcomm-docker PR, let's got with ResComm-Connect. First you
need to create a file:

```sh
cd ../Restcomm-Connect/
vim restcomm-connect-build.sh
```

with the following content (change to your own values):

```text
#!/bin/bash
export RESTCOMM_HOME=/home/antonmry/Workspace/Telestax/Restcomm-Connect
export MAJOR_VERSION_NUMBER=7.6
export BUILD_NUMBER=0

JAVA_HOME=/home/antonmry/Software/jdk/jdk1.7.0_80
export JAVA_HOME

export WORKSPACE=$RESTCOMM_HOME
mkdir $WORKSPACE/dependencies
export DEPENDENCIES_HOME=$WORKSPACE/dependencies

ant release -f ./release/build.xml -Drestcomm.release.version=$MAJOR_VERSION_NUMBER.$BUILD_NUMBER -Drestcomm.branch.name=restcomm-release-$MAJOR_VERSION_NUMBER.$BUILD_NUMBER -Dcheckout.restcomm.dir=$RESTCOMM_HOME -Dworkspace.restcomm.dir=$RESTCOMM_HOME/restcomm -Dcheckout.dir=$DEPENDENCIES_HOME
```

Execute it:

```sh
chmod +x restcomm-connect-build.sh
./restcomm-connect-build.sh
```

Time to wait 5 minutes in a good laptop... after that, we should have our
customozied JBoss ready to be launched:

```sh
ls ./release/Restcomm-JBoss-AS7-7.6.0.zip
```

Now you can unzip it and start to play with it... but how to start to develop?

In the Intellij Idea, you can import the project as a Maven project. I've
imported the route **Restcomm-Connect/restcomm** which has the root pom.xml and
created a local branch as usual:

```sh
git checkout -b initTimeRVD#1
git push -u origin initTimeRVD#1
```

Now you can develop as much as you want. To build it:

```sh
cd restcomm
mvn install
```

Here you can do it with the different modules, you don't need to build
everything each time but the specific module you've changed. To deploy it and
test it:

```sh
docker ps
docker stop 06b117547bc5726fc74c42a61c6826342f04b9b194ebc0029f70be4ad1ef1a4f
rm -r /home/antonmry/Workspace/Telestax/deployments/restcomm.war
rm -r /home/antonmry/Workspace/Telestax/deployments/restcomm-rvd.war
cp -r restcomm.application/target/restcomm/ ~/Workspace/Telestax/deployments/restcomm.war
cp -r restcomm.application/target/restcomm.rvd/ ~/Workspace/Telestax/deployments/restcomm-rvd.war
```

```sh
docker run -i -d -v /var/log/restcomm/:/var/log/restcomm/ -v /home/antonmry/Workspace/Telestax/deployments:/opt/Restcomm-JBoss-AS7/standalone/deployments -e VOICERSS_KEY="xxx" -e S3_ACCESS_KEY="xxx" -e S3_SECURITY_KEY="xxx" -e S3_BUCKET_NAME="xxx" -e STATIC_ADDRESS="YOUR ETH0 IP?" -e ENVCONFURL="https://raw.githubusercontent.com/RestComm/Restcomm-Docker/master/scripts/restcomm_env_locally.sh" -p 80:80 -p 443:443 -p 9990:9990 -p 5060:5060 -p 5061:5061 -p 5062:5062 -p 5063:5063 -p 5060:5060/udp -p 65000-65050:65000-65050/udp restcomm/yourname:latest
```

Know, just open RestComm as usual in [https://eth0-ip](https://eth0-ip) or
[https://eth0-ip/olympus](https://eth0-ip/olympus) and test. Once you have
finished your changes, upload them to Github:

```sh
git add file1 file2
git commit "A good message #yourIssue"
git push
```

Create the PR in github and wait for the approbation ;-)

## Reference documentation

- [How to build Restcomm-Connect from source](http://documentation.telestax.com/connect/configuration/How%20to%20build%20Restcomm-Connect%20from%20source.html#build-from-source)
- [Restcomm – Docker Adding a Jar File to an Exiting Container](http://docs.telestax.com/restcomm-docker-adding-a-jar-file-to-an-exiting-container/)
