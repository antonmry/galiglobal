title=SpringIO 2015: a great event for a great community
date=2015-05-14
type=post
tags=WebRTC,ServiceDelivery,SpringIO,Groovy
status=published
~~~~~~

I had the opportunity to participate in [SpringIO as speaker](http://www.springio.net/using-groovy-to-empower-webrtc-network-systems/) in April (Barcelona). It was quite scary to participate in a conference about Spring, I am not a web developer, and, in fact, when I have to develop or design any web system based in Java, I prefer just to use EJB3 and Servlet 3.2, avoiding any framework. But there is something more in this conference: [Groovy](http://en.wikipedia.org/wiki/Groovy_%28programming_language%29). And we are using Groovy in a lot of cool things, specially in the WebRTC domain. So the idea was simple: introduce WebRTC and show an interesting Groovy use case.

Unfortunately, Groovy is not in a good moment right now. Yes, there are a lot of people speaking about it... but after Strachan (Groovy's creator) wrote on his blog, "I can honestly say if someone had shown me the Programming in Scala book by Martin Odersky, Lex Spoon & Bill Venners back in 2003 I'd probably have never created Groovy." and Pivotal is not hosting the project any more... well, uncertain future for Groovy... and it's a pity. Because sometimes we need a scripting language and Groovy is a great choice if you are a Java developer, as I am. It's dynamically compiled to Java Virtual Machine (JVM) bytecode, so the performance is good, even for network system. Also it can interoperate with other Java code and libraries.

For all these reasons, I would like to see Oracle more involved in the Groovy project, for instance reviving the [JSR-241](https://jcp.org/en/jsr/detail?id=241) and ending with [jython](http://en.wikipedia.org/wiki/Jython)... If you are working with [Weblogic Scripting Tool (WLST)](https://docs.oracle.com/cd/E29542_01/nav/wlst.htm), you probably hate Jython as much I do.  Other important point is [gradle](https://gradle.org/), it looks a great tool even if I didn't have opportunity to test it yet. Anyway, I am quite happy with Maven, specially now with the [new Maven Oracle Repository](https://blogs.oracle.com/WebLogicServer/entry/weblogic_server_and_the_oracle). And I have also [Spock](https://code.google.com/p/spock/) in the "thing to review" list, a testing framework also based in Groovy. 

Even if my talk wasn't successful and my interest in the Spring framework is limited, I've really enjoyed the event. First, because it was very well organized. Second, the quality of the speakers was awesome, the technical quality of some talks was superb. And not only because of the speakers, also because of the audience. I envy Spring having a so good community, it would we so great to have something similar with Telecom Application Developers. That's one of the reasons because I'm so excited with the [TADHack](http://tadhack.com/2015/) and all the work [Alan Quayle](http://alanquayle.com) is doing. It is a long road yet but a good start. 

Here my slides. I've covered WebRTC, then Groovy and I've finished with some TADHack references.

<iframe src="https://www.slideshare.net/slideshow/embed_code/key/bKBppeBAK8rQze" width="476" height="400" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

There is also a project in GitHub with the source code if you are interested: [SpringIOWebRTCSampleApp](https://github.com/antonmry/SpringIOWebRTCSampleApp).
