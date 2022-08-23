title=Services Gatekeeper 6 installed in fifteen minutes, is it possible? - Part 2
date=2015-08-30
type=post
tags=OCSG,ServicesGatekeeper,ServiceDelivery,Oracle
status=published
---------

This is the continuation of how to install and test OCSG, you can find the part 1 [here](/blog/2015/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible-Part-1.html).


## Platform Test Environment (PTE) Installation

1. Login to [Oracle Software Delivery Cloud](https://edelivery.oracle.com/), choose *Oracle Communications* in **Select a Product Pack** and *Linux x86-64* and click on **Go**. Click on *Oracle Communications Services Gatekeeper 6.0*.

2. Download Oracle Communications Services Gatekeeper 6.0 Platform Test Environment, V73999-01.zip and copy it into the VM.

3. Unzip the file and execute the installer:

```sh
unzip V73999-01.zip
java -jar ocsg_pte_generic.jar
```

4. In the first window, accept the default Inventory Directory pressing **OK**.

5. The Welcome screen appears, press **Next**.

6. Introduce */opt/ocsg6* in the Oracle Home field and press **Next**.

7. Let **PTE Installation** selected and press **Next**.

![PTE Installation](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/installationPTE.png)

REPLACE_WITH_READ_MORE
8. Review the Installation Summary and press **Install**. It may take a while. Press **Next** when available and **Finish**.

![PTE Installation Done](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/installationPTEDone.png)

## Start the PTE

1. Open a new Terminal and execute the following commands. 

```sh
cd /opt/ocsg6/ocsg_pte/
./run.sh
```

2. The PTE should appear:

![The PTE](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/PTE.png)

3. Go to **Tools -> Variables Manager** or press **Ctrl+3**.

![Variables Manager Menu](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/VariablesManagerMenu.png)

4. Change the following fields and press **OK**:
  * **at.host:** *ocsg*
  * **nt.host:** *ocsg*

![Variables Manager Screen](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/VariablesManager.png)

5. Click on **Server** and change the following fields:
  * **Hostname:** *ocsg*
  * **Port:** *8001*
  * **Username:** *weblogic*
  * **Password:** *welcome1*

![Server Credentials](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/ServerCredentials.png)

6. Go to **Tools -> SLA Manager** or press **Ctrl+1**.

![SLA Manager Menu](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/SLAManagerMenu.png)

7. Select **default_app_group** and click on the pencil icon.

![Default App Group SLA](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/default_app_group.png)

8. Click on the globe icon with a green arrow pointing up and press **Local**. The message *The SLA was succesfully uploaded to OCSG* should appear. Press **OK** twice.

![Default App Group SLA Done](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/default_app_group_done.png)

9. Select **default_sp_group** and click on the pencil icon. Click on the globe icon with a up arrow and press **Local**. The message *The SLA was succesfully uploaded to OCSG* should appear. Press **OK** twice.

10. Go to **Simulators -> SMPP** and click on **Start**. The button will change to **Stop**.

![SMPP Simulator](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/SMPPSimulator.png)

## Final test: send SMS

1. In the PTE, go to **Clients -> Login** and press **Login** (green arrow). The button should change to **Logout** (red square).

![Client Login](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/login.png)

2. Go to **Messaging -> Short Messaging -> Application-initiated** and change the message to *Hello SaNE!*. Click on **Send** (green arrow).

![Send SMS](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/sendSMS.png)

3. Go to the **Map**, click on the second button over the phone **1234** and choose *Read messages*. Here it is!!

![SMS Sent](/images/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible/SMS.png)

## Conclusion

Probably you have spent more than fifteen minutes to arrive here... but it's also true most of the actions are part of the configuration, not the installation. The process is straightforward and it can be easily explained. Even if you don't have advanced knowledge of Weblogic or Linux, it's possible to do it. So, as we can see in this article, OCSG is very easy to install now and it has a lot of features deployed out-of-the-box. Because it's a so extensive application supporting a huge number of business possibilities (Service API Exposure, Direct Carrier Billing, Policy Gateway, etc. ), a basic fresh installation is a very powerful way to focus in the functionality and forget problems with databases, OS and other technical questions and now we can have it in only 15 minutes!

