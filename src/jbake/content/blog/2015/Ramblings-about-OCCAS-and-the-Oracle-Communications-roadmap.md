title=Ramblings about OCCAS and the Oracle Communications roadmap
date=2015-02-11
type=post
tags=OCCAS,OracleComms,NFV
status=published
~~~~~~

This is going to be a different type of post. I usually write about technical things but today I am going to try something different. Well, maybe not so different, I have more questions than answers, but at least, I will try to explain as I see the Oracle Comms portfolio and its evolution. Just for the record, I don't work inside Oracle, I don't have privileged information and if you do any business decision based in this article, you are a fool.

## Context

In 2006, [Oracle acquired MetaSolv](http://www.oracle.com/us/corporate/acquisitions/metasolv/index.html), recognized leader in service fulfillment operations support system (OSS) solutions for next-generation communications service providers. Two years later, [Bea Systems... and with it, Weblogic Server](http://www.oracle.com/us/corporate/acquisitions/bea/index.html), the Application Server leader of the market. After that, Oracle has build a strong position in the OSS market, no only from a business perspective, also from a technical point of view. All the products are similar (from the CRM to the Inventory) and they share the same architectural principles. As consequence, CSPs enjoy some advantages. For example, after the first deployment, they have the knowledge and experience to continue deploying the rest of the suite. 

In February 2013, [Oracle bought Acme Packet](http://www.oracle.com/us/corporate/press/1903221), the leading global provider of session border control technology. One month later [Oracle bought Tekelec](http://www.oracle.com/us/corporate/acquisitions/tekelec/index.html), a leading provider of network signaling, policy control, and subscriber data management solutions for communications networks. All the analysts saw this as a big movement to the Network market. Me too.

## Oracle Comms Converged Application Server

Most of people didn't realize Oracle had a previous portfolio of Networks Applications before the acquisition. Even if this suite is no so big as the OSS and BSS suites, it has importance and business share inside the firm... and something more important, a very intelligent roadmap based in OCCAS as network platform for everything. But.... what is OCCAS? The [Oracle Communications Converged Application Server](http://www.oracle.com/us/products/applications/communications/unified-communications/converged-application-server-edition/overview/index.html) is a Weblogic with Telecom Network capabilities (mainly SIP and Diameter) and oriented to real-time applications. As product, it's very small. It's not easy to find a CSP asking for it, because the business case is not so clear. OCCAS is more like a Framework, something you are going to use to develop other things. And, in fact, most of the SDP portfolio is based in OCCAS, for instance, OCSG and the Unified Communications suite. 

The Converged Application Server [Service Creation Environment](https://docs.oracle.com/cd/E27702_01/doc.51/e27705/tpd_developing.htm#autoId1) (SCE) consists of a faceted framework that supplements the [Oracle Enterprise Pack for Eclipse](http://www.oracle.com/technetwork/developer-tools/eclipse/downloads/index.html) (OEPE). The SCE provides tools and resources you can use to develop converged applications, including wizards, simulators, and templates. And also it provides the [Service Foundation Toolkit](https://docs.oracle.com/cd/E27702_01/doc.51/e27707/sip_sft_overview.htm) (SFT), a converged application Java development framework. It provides APIs that abstract the details of the communication protocol for the application, enabling to focus on the service value provided by converged SIP and HTTP applications. The idea is simple: if you are a developer with Java and Eclipse knowledge, you can start to develop Telecom applications without knowledge about Telecom protocols. And those applications will run in the leader platform: Weblogic. So they will be carrier-grade with all the performance, security and scalability requirements.

![The Converged Application Server Service Creation Environment](https://docs.oracle.com/cd/E27702_01/doc.51/e27705/img/sce_overview.gif)

## Oracle Comms Roadmap

A roadmap with all the Network products based in OCCAS makes sense for several reasons. Some of them are:
* **Contrasted technologies**: Java, Weblogic, the Oracle Database, Linux, Eclipse and so on. You are not reinventing the wheel. All those technologies are familiar to the CSPs, they trust them. 
* **Cloud and virtualization**: CSPs want to be ready for the near future. They know about the advantages of virtualization and cloud strategies. And OCCAS is the perfect choice for that. You can run it in several platforms, deploy it, scale it and so on. It's flexible and modern.
* **Learn one, use many**: you start deploying one application, and after that, you will have the knowledge and resources to deploy the rest of the suite (if you want). You will save a lot of time learning complex systems or technologies so you will be more flexible and faster delivering new products to the market.
* **Easy support**: the Operation team needs to know about basic technologies: no more, no less. As you need a DBA, you will need a Weblogic expert who can work with all the systems. In short, the daily support will be easier because the level of complexity is smaller.
* **Maintenance and upgrade**: all the products are going to do it in the same way and it's out-of-the-box in Weblogic. Converged Applications Server's upgrade feature ensures that no calls are dropped while during the upgrade of a production application. The upgrade process also enables you to revert or rollback the process of upgrading an application. If, for example, you determine that there is a problem with the newer version of the deployed application, you can undeploy the newer version and activate the older version.
* **High availability and geographic redundancy**: it's provided out-of-the-box, so you don't need worry about that.
* **The BSS/OSS suite**: it's based on the same technologies. Any CSP with some of those products installed has the experience and knowledge to start to work with OCCAS or any OCCAS-based product and the integration between BSS/OSS and Network would be easier.

As we saw before in the OSS suite, this is a winner strategy. And it doesn't end here. After have everything running in the same platform, Oracle can start to work in the integration between the products, something like the [Oracle Application Integration Architecture (AIA)](http://www.oracle.com/us/products/applications/application-integration-architecture/overview/index.html) but oriented to the network. Any network vendor in the market can compete with something like that.

## The future

The final question: is Oracle going to migrate the ACME and Tekelec products to the OCCAS platform?. We know the advantages but there are also problems. Migrate part of the portfolio to this platform requires a lot of resources and it's very time-consuming. And of course, not all the products are valid (specific hardware systems doesn't have sense in OCCAS) or they are not going to have enough Return of Investment. So, I don't have an answer for that. After two years, I didn't see movements in this direction but I also know the acquisitions take a lot of time and it's soon yet. Oracle did a great job combining OCCAS and [Application Session Controller](http://docs.oracle.com/cd/E50379_01/index.htm) (ASC) to launch the [WebRTC Session Controller](http://www.oracle.com/us/products/applications/communications/web-rtc-session-controller/overview/index.html) (WSC). That is for sure [the path to follow](https://blogs.oracle.com/COMMSINFODEV/entry/new_tech_new_challenges_the) but they are just two products running independently and integrated using a REST interface and we are speaking about have the ASC capabilities running on OCCAS. 

On the other hand, Oracle has announced recently the [Oracle Communications Network Service Orchestration Solution](http://www.oracle.com/us/corporate/press/2418407). This is the mainly Oracle NFV bet but it doesn't look based in OCCAS or even Weblogic. And we know, Oracle can buy some specific NFV/SDN company, they don't need to develop their own solution... but with more acquisitions the path to have only one platform will be even more complicated.

This year we probably will see a new version release of OCCAS. That will be the moment to know about the future of this excellent platform. 
