	<!-- Fixed navbar -->
    <div class="navbar navbar-default navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="<%if (content.rootpath) {%>${content.rootpath}<% } else { %><% }%>">GaliGlobal</a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="<%if (content.rootpath) {%>${content.rootpath}<% } else { %><% }%>index.html">Home</a></li>
            <li><a href="<%if (content.rootpath) {%>${content.rootpath}<% } else { %><% }%>archive.html">Archive</a></li>
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">Conferences<b class="caret"></b></a>
              <ul class="dropdown-menu">
                <li><a href="/blog/2017/20170306-My-experience-in-the-Refugal.html">2017 Refu.gal</a></li>
                <li><a href="/blog/2015/Oracle-Preworkshop-and-TADSummit-2015.html">2015 TADSummit</a></li>
                <li><a href="/blog/2015/A-look-back-to-Geecon-2015.html">2015 Geecon</a></li>
                <li><a href="/blog/2015/SpringIO-2015-a-great-event-for-a-great-community.html">2015 SpringIO</a></li>
                <li><a href="/blog/2014/Oracle-Preworkshop-TADSummit-2014.html">2014 TADSummit</a></li>
              </ul>
            <li><a href="<%if (content.rootpath) {%>${content.rootpath}<% } else { %><% }%>about.html">About</a></li>
            </li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>
    <div class="container">
