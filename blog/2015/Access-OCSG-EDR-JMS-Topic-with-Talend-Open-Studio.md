# Access OCSG EDR JMS Topic with Talend Open Studio

*13 February 2015*

I've been using [Talend Open Studio](https://www.talendforge.org/tutorials/tutorial.php?idTuto=14) for a long time. It's an impressive software to do automated tasks, it works well and the development is quite fast. Furthermore, the TtHW (Time to Hello World) is really short. As you can see, I like it.

In this tutorial, I am going to show how to use it Talend Open Studio to access the JMS Topic where OCSG shows all the runtime information: the Event Data Records (EDRs). This is the main place for debugging so it's really important. The article is based in the offical documentation [Creating EDR Listeners](http://docs.oracle.com/cd/E50778_01/doc.60/e50771/pds_edrlistener.htm#SGPDS627) but adapted to TOS.

## Pre-requisites

You will need an OCSG 6 or 5.1 running and also the [TOS Data Integration](http://www.talend.com/download/talend-open-studio?qt-product_tos_download=3#qt-product_tos_download) installed in your computer.

## Talend Open Studio development

Drop a tJMSInput component in the canvas and double click over it.

![tJMSInput component](/blog/2015/Talend-Open-Studio-images/tJMSInput.png)

Configure all the fields as you can see in the following picture:

![tJMSInput fields](/blog/2015/Talend-Open-Studio-images/tJMSInput_form.png)

Some important notes:

- You have to import the library *wlthint3client.jar* before to use the component. You can find it in *<OCSG Installation folder>/wlserver/server/lib/wlthint3client.jar*. To import it, there are several ways, for instance, the tLibraryLoad component.
- Change the **Server URL** to your environment configuration. It must be a Node, not an Admin. In this case it's an standalone configuration with Admin and Node in the same Weblogic instance.
- Change the **Message from** to your environment configuration. If you don't know it, go to the Console,in the Domain Structure, **Services -> Messaging -> JMS Servers**.

## Weblogic configuration

There is a missing point, and it's the key. In the Weblogic console:

1. Go to the Domain Structure and Select **Services -> Messaging -> JMS-Modules**.
2. Click on **WLNGJMSResource -> EdrTopic -> Advanced**.
3. Find **Create Destination Identifier** and introduce *com.bea.wlcp.wlng.edr.EdrTopic* and Save.
4. Reboot the Weblogic.

![Weblogic JMS Configuration](/blog/2015/Talend-Open-Studio-images/WeblogicJMSConfiguration.png)

This step is mandatory because of the tJMSInput component but it can be avoided if you are accessing the JMS Topic in another way.

## The end

That's all. Click on Run in the Talend Open Studio and you should be subscribed to the Topic. Send an SMS from the PTE and you should start to generate EDRs. The next step would be create the Java classes to access the EDR information and start to work with it.
