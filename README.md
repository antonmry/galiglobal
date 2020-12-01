# GaliGlobal

This is the source for my [blog](http://www.galiglobal.com/). The content is
rendered using [JBake](http://jbake.org/), source is in the master branch and
output is pushed on the gh-pages branch.

## Build

```sh
./gradlew bake
```

If you want to have it updated with changes in real-time:

```sh
./gradlew -t bake
```

To run it locally:

```sh
./gradlew liveReload 
```

and open http://localhost:35729 with your browser. It should refresh with any change.

## Deploy

To publish it:

```sh
./gradlew publishGhPages
```

