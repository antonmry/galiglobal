# Time to start a Go blog with Hugo

*16 June 2016*

**UPDATE**: I finally merged both blogs, so this blog post doesn't make sense. I
prefer Hugo to JBake but because I've been doing more Java/Groovy development, I
will stay with JBake.

Well, this is embarrassing. I'm launching another blog!. Why?. Some time ago
I've started to write a blog, in the beginning for corporate news but it has
become a place where to write or document interesting things I do in my work,
most of them related to Java, Groovy and Oracle technologies. The blog is
generated with [JBake](http://jbake.org/) with the
[gradle plugin](https://github.com/antonmry/jbake-gradle-plugin), I like to use
related technologies and I'm quite happy with the result, but to be honest, I
don't write frequently.

Six months ago I've started to learn and use [Go](https://golang.org/). I was
very impressed with the simplicity of the language and I've started to read a
lot of articles, books, etc., watch videos and develop some projects. I
discovered [Hugo](https://gohugo.io/), a site generator similar to JBake but
written in Go. I was tempted to migrate my previous blog, but today I'm going to
continue writing about not Go subjects, so it's simpler to open a new one only
for Go, bots, DevOps, concurrency and perfomance. In another post I will write
more about Go and why I find it so interesting.

As the first post, let's see how to configure [Hugo](https://gohugo.io/). I've
to say it was really easy, I really impressed with piece of software. I can
compare with other site generators as Jekyll, Hexo or JBake, and I have to say
Hugo is my favourite.

First of all, I've created a new repo in my Gihub account and cloned it in my
laptop:

```sh
git clone git@github.com:antonmry/antonmry.github.io.git
cd antonmry.github.io
```

Because I'm going to use my github user page, the source code of the page must
be in master branch. For your Hugo code, you can have a separate repo or just a
different branch. I choose the second option with a branch named source, I
prefer it in that way, it's simpler and this is the main difference with the
procedure you can find in
[the excellent Hugo documentation](https://gohugo.io/tutorials/github-pages-blog):

```sh
git checkout -b source
git push -u origin source
```

Inside the source code folder, we are going to create a folder linking to the
master branch:

```sh
git subtree add --prefix=public git@github.com:antonmry/antonmry.github.io.git master --squash
git subtree pull --prefix=public git@github.com:antonmry/antonmry.github.io.git master
```

It's time to generate the site. First you have to install Hugo, plenty of
options in the [the Hugo website](https://gohugo.io/overview/installing/). I've
chosen the Fedora package, updates will be easier.

```sh
hugo new site antonmry.github.io
mv antonmry.github.io/* .
rm -r antonmry.github.io
```

Choose your theme, there are very nice options, I've chosen beatifulhugo:

```sh
cd themes
git clone https://github.com/halogenica/Hugo-BeautifulHugo.git beautifulhugo
cd ..
echo "theme = \"beautifulhugo\"" >> config.toml
```

Create your first blog and start the server:

```sh
hugo new post/hugo-site-created.md
hugo server --buildDrafts
```

Open in your browser [http://localhost:1313/](http://localhost:1313/) and enjoy your first post with Hugo ;-)

Let's move the post from draft to publised: edit the file
content/post/hugo-site-created.md and change the draft line from true to false
if exists.

Now it's time to upload it to Gihub and make it public:

```sh
hugo
git add -A
git commit -m "Initial version"
git push
git subtree push --prefix=public git@github.com:antonmry/antonmry.github.io.git master
```

Oh, really, can it be so easy?. Just go to
[https://antonmry.github.io](https://antonmry.github.io) (or your equivalent
site)

I was thinking in create a travis job to do the publishing in master (I did it
before for jbake) but to be honest, this method is simple enough. I've added to
my .bash_alias the last command and that's all I need.

Enjoy!

PS: if you do a rebase in `source`, you will need to do it a bit more tricky to
push to master because you can't use `--force` with the `subtree` option:

```sh
git push origin `git subtree split --prefix public source`:master --force
```

More info can be found in Stackoverflow
[Git subtree - subtree up-to-date but can't push](http://stackoverflow.com/questions/13756055/git-subtree-subtree-up-to-date-but-cant-push).
