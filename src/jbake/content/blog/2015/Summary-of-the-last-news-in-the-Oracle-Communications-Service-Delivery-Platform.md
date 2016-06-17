title=Summary of the last news in the Oracle Communications Service Delivery Platform
date=2015-05-21
type=post
tags=OCSG,OCCAS,OCWSC,OCECAS,OracleComms,ServicesGatekeeper,ServiceDelivery,ConvergedApplicationServer,WebRTCSessionController,EvolvedCommunicationsServer
status=published
~~~~~~

When I've started this blog, my main motivation was to provide a central place with information about Service Delivery Platforms, mainly related to the Oracle Communication suite because it's what I know. But I am failing in this goal. I am very busy from the beginning of the year and I don't find time enough to write posts and articles. Excuses. I should keep in mind the original idea and don't miss the opportunity to keep readers updated with the last news.

So, this post is going to be a summary of the releases and news in the Oracle Comms SDP.... and there are a lot!. Even a new product!. 

# Oracle Communications Services Gatekeeper (aka Gatekeeper)

I wrote about the new 6.0 version [here](/2015/01/23/OCSG-6-0v1-generally-available-new-features-introduction/) and even I've published [the first part of a how-to explaining the installation](/2015/04/30/Services-Gatekeeper-6-installed-in-fifteen-minutes-is-it-possible-Part-1/). But there are two very interesting updates.

## Oracle Communications Services Gatekeeper 6.0 Patch Set 1 Released

New patch solving more than 20 bugs: [Doc ID 1993751.1](https://support.oracle.com/epmos/faces/DocumentDisplay?_afrLoop=447946421774684&id=1993751.1&_afrWindowMode=0&_adf.ctrl-state=1de1letpct_4). Whatever you are doing with OCSG, the installation of this patch should be mandatory.

It provides also patches for JDK [Patch 20347164](https://support.oracle.com/epmos/faces/ui/patch/PatchDetail.jspx?parent=DOCUMENT&sourceId=1993751.1&patchId=20347164), Weblogic [Patch 19637454](https://support.oracle.com/epmos/faces/ui/patch/PatchDetail.jspx?parent=DOCUMENT&sourceId=1993751.1&patchId=19637454) and Coherence [Patch 20164069](https://support.oracle.com/epmos/faces/ui/patch/PatchDetail.jspx?parent=DOCUMENT&sourceId=1993751.1&patchId=20164069), be sure to apply them!

## Oracle Communications Services Gatekeeper Statement of Direction - May 2015 

Oracle has published recently a SoD for OCSG. It's always interesting to know what Oracle is working on. Here, [Doc ID 1081178.1](https://support.oracle.com/epmos/faces/DocumentDisplay?_afrLoop=448644669159009&id=1081178.1&_afrWindowMode=0&_adf.ctrl-state=1de1letpct_78), you can find it. The document deserves a special post for it!.

# Oracle Communications Application Server (aka OCCAS)

A new version for our favorite AS... from 5.1 to 7.0. A lot of new changes!. The most important item, it's the first implementation of the recently released [JSR 359: SIP Servlet 2.0](https://www.jcp.org/en/jsr/detail?id=359). There are also other things, for instance, new (and more modern!) versions of the JDK and Weblogic. This is not a release with a lot of new features but with a lot of improvements for developers. Here it's the announcement:  

> Oracle Communications Converged Application Server (OCCAS) 7.0 release is now available to customers/partners for download. OCCAS 7.0 is the industry’s first JSR 359 (SIP Servlet 2.0) compliant SIP Application Server/Communications Middleware based on Java EE 6/Java EE 7.  OCCAS 7.0 also introduces Coherence based in-memory, distributed cache data architecture that enables the customers to dynamically scale mission-critical applications.  OCCAS 7.0 also introduces a flexible overload framework and monitoring functions which along with the auto scaling capabilities makes it Cloud/NFV ready. 
>
> Here are some key capabilities of the release:
>
> ** SIP Servlet 2.0/ JSR 359 Compliance **
>    * Makes SIP Servlet Development more agile  (Java EE 6/7, CDI, POJOs, Annotations etc)
>    * Meets most demanding requirements of communications middleware (Converged container, abstraction, portability, standards compliance etc)
>    * Fosters decentralized ecosystem  (Extensibility, Pluggability etc)
>
> ** Coherence based data architecture **
>    * Elasticity – Scale in/out
>    * Reliability/fault tolerance/HA
>    * Performance
>
> ** Monitoring and Overload Protection **
>    * Overload Framework/ Custom KPI policies and threshold configuration
>    * Memory Based Overload Protection
>
> ** Enhanced Diameter Support **
>    * SIP Application Interworking with Diameter
>
> ** Virtualization Technologies Support **
>    * OVM & KVM Certification
>
> ** Platform Upgrade **
>    * Based on WebLogic 12.1.3  (latest release)

Source: [Oracle Community](https://community.oracle.com/docs/DOC-913298?sr=inbox&ru=831131)

# Oracle Communications WebRTC Session Controller (aka WSC)

## New version of Oracle Communications WebRTC Session Controller

WSC 7.1 was announced on December 2014 [here](http://www.oracle.com/us/corporate/press/2391012?rssid=rss_ocom_pr) but it wasn't Generally Available until March 2015. Bugs fixed and some interesting features as invoke REST interfaces from the Groovy scripts or some improvements in the registrar. Check the [Release note](http://docs.oracle.com/cd/E55119_01/doc.71/e55133/toc.htm) for more info.

## iOS SDK and Android SDK finally available

Recently the SDKs for Android and iOS have been published. You can find them [here](http://www.oracle.com/technetwork/developer-tools/webrtc-2525637.html). Also there are some excellent how-to wrote by Leif Lourie [here](https://apexapps.oracle.com/pls/apex/f?p=44785:2:109737384896297:::2,CIR,RIR:P2_PRODUCT_ID,P2_RELEASE_ID:3479). As usual, great work from Leif.

# Oracle Communications Evolved Communications Application Server (aka eCAS)

The most important news for the end: a new product based in OCCAS. Here the note:

>As mobile operators drive their networks toward an all-IP and virtualized state, they require the means to design and deliver compelling high definition voice, video and multimedia offers via Voice over LTE (VoLTE) and Voice over WiFi (VoWiFi). Oracle Communications Evolved Communications Application Server (OCECAS) brings a sophisticated, yet easy-to-use network service design and delivery product to satisfy that need. OCECAS works out of the box; it is NFV-enabled and standards compliant; and it provides network-grade speed and reliability with the cost profile of an IT product. 
>
>Beyond service delivery, OCECAS accelerates the operator's move to better network cost performance by driving subscribers to offers that engage IP assets, allowing the operator to retire more traditional components. This drive toward the single IP network also facilitates spectrum reuse for increased monetization opportunity. OCECAS is a significant step forward in the journey to the all-IP, virtualized network destination. 
>
> Operators will also enjoy lower service update costs as the flexible user interface allows service changes to be implemented without costly, time-consuming software coding or vendor customizations.
>
> The Oracle Communications Evolved Communications Application Server includes:
>
> ** Key Capabilities **
> - Out of the box VoLTE and VoWiFi application designed for GSMA standards for immediate productivity
> - Built from the ground up to support NFV
> - Standards-compliant IMS interfaces built with SIP, Diameter and Java
> - Easy to use, yet powerful session design center providing intuitive drag and drop application configuration
> - Continuous design-time validation enforcement and version control to ensure quality
> - Automated deployment across testing, staging and production environments
> - Flexible data federation across multiple sources to prevent costly custom integrations
> - Productized integration with Oracle Communications Core Session Manager (OCCSM)
> - Runtime powered by the Oracle Communications Converged Application Server (OCCAS) 7.0
> - Interoperability testing underway with Radisys and Dialogic Media Resource Functions
> - Integration of inbound third-party services, enabling differentiated offers
>
> ** Benefits **
> - Productive from the first day
> - Delivers true service agility for improved time to market
> - Enables attractive, differentiated offer creation
> - Freedom from vendor-specific customizations
> - Virtualized, interoperable, standards-compliant
> - Robust, network-grade operation on industry-standard platforms
> - Low TCO

Source: [Oracle Community](https://community.oracle.com/docs/DOC-913067?sr=inbox&ru=831131) and also check the Press note [here](http://www.oracle.com/us/corporate/press/2526355?rssid=rss_ocom_pr). There is also a [webinar](https://eventreg.oracle.com/profile/web/index.cfm?PKwebID=0x22479021e2&varPage=home), don't miss it if you are interested.

For me it's really good to have a release like this. Being OCCAS based, it's very easy for us to learn the new product and there are some interesting integration with ACME products. I will build a laboratory very soon and I hope to find time to write more about this new product.

Stay tunned!
