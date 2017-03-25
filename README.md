[![Build Status](https://travis-ci.org/antonmry/galiglobal.svg)](https://travis-ci.org/antonmry/galiglobal)

This is the source for my [blog](http://www.galiglobal.com/). The content is rendered using [JBake](http://jbake.org/), source is in the master branch and output is pushed on the gh-pages branch.

To build the project:

```sh
./gradlew clean jbakeBuild
```

If you want to have it updated with any change:

```sh
./gradlew -t jbakeBuild
```

To publish it:

```sh
./gradlew publishGhPages
```

To run it locally:

```sh
./gradlew liveReload 
```

and open http://localhost:35729 with your browser. It should refresh with any change.

I've added a couple of customizations:

1. You can write REPLACE_WITH_READ_MORE to indicate you want to show a Read more link in the index instead of the full blog.
2. The gradle plugin is a branch of the original with the last version of JBake and a couple of new tasks.
