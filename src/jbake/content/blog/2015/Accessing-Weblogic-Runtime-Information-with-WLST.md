title=Accessing Weblogic Runtime Information with WLST
date=2015-01-19
type=post
tags=OCSG, Weblogic, Services Gatekeeper, Java
status=published
~~~~~~

Deal with java.lang.OutOfMemoryError: PermGen space errors is always tricky. Most of the times it's something related to the chosen JVM, probably not supported for the hosting OS (for example, using a 32bits JVM in a 64bits OS is a typical issue).

Here I provide two interesting ways to check the JVM configuration:

<script src="https://gist.github.com/antonmry/efe307a587388c3ecdfb.js"></script>

For example, perhaps we could want to increase the PermSize, so we edit the  &lt;Domain dir &gt;/ &lt;Server Name &gt;/bin/setDomainEnv.sh to add something like this in the beginning:

```
# USER_MEM_ARGS   - The variable to override the standard memory arguments
#                   passed to java.

USER_MEM_ARGS="-Xms1024m -Xmx1024m -XX:CompileThreshold=8000 -XX:PermSize=256m"
export USER_MEM_ARGS
```
Now it's time to reboot the weblogic and check everything again using the same commands I showed previously.

More info:
- [Invoking WLST](http://docs.oracle.com/cd/E13222_01/wls/docs100/config_scripting/using_WLST.html#wp1093952)
- [Getting Runtime Information](http://docs.oracle.com/cd/E13222_01/wls/docs100/config_scripting/monitoring.html)
- [WLST Scripting Introduction](https://blogs.oracle.com/practicalbpm/entry/wlst_scripting_to_get_weblogic)
