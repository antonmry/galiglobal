title=Introduction to Go kit
date=2017-01-08
type=post
tags=development,microservices,go,go-kit
status=published
~~~~~~

## Microservices don't fit all use cases

When I've started [my Leanmanager bot](https://github.com/antonmry/leanmanager), I've chosen to use the same approach (well, really it's a framework but that word seems to be censured if you are a gopher so I will use *approach*) as the kubernetes project: if it's good for k8s, it should be good for me and also a good way to learn a bit more about kubernetes. So I've implemented all the REST APIs using [github.com/emicklei/go-restful](https://github.com/emicklei/go-restful).

Then I had the opportunity to work a bit with [go-kit](https://gokit.io/). A framework, ups, no, sorry, a toolkit to create microservices. My initial opinion was too complicated and too much boilerplate. Yet I would like to give it another opportunity, there are some interesting things useful for bots (support many transports, RPC approach, instrumentation) and my main motivation with the bot is to test new technologies and ideas so... why not?

If you visit the [Go-kit website](https://gokit.io), and then, you will jump very soon into the [stringsvc tutorial](https://gokit.io/examples/stringsvc.html). The tutorial is awesome but it isn't a five minutes read and it's a bit too complicated to start to work with Go-kit. I recommend an approach a bit different. First, watch [Go + Microservices = Go Kit](https://www.youtube.com/watch?v=JXEjAwNWays) from [Peter Bourgon](https://peter.bourgon.org/). This is an awesome talk explaining microservices and their use cases. Clearly Peter knows a lot about the subject: microservices aren't for everyone.

If after the video, you think microservices fit your case, go ahead and may the Force be with you.

## Go-kit addsvc example

First step, download Go-kit:

```sh
go get github.com/go-kit/kit
```

Then, just copy the [addsvc example](https://github.com/go-kit/kit/tree/master/examples/addsvc) and download the dependencies (this may take a while depending of what you've already in the GOPATH).

```sh
cp -r ../../go-kit/kit/examples/addsvc/ .
go get ./...
```

The plan is simple, modify it to fit your use case while you are becoming more familiar with go-kit. But first, let's try the example. Launch the server:

```sh
cd cmd/addsvc/
go run main.go
```

And in a different shell, launch the client:

```sh
cd cmd/addcli/
go run main.go -http.addr=:8081 1 2
```

If everything goes well, you will obtain something like:

> 1 + 2 = 3

Or you can use `curl` directly:

```sh
curl -H "Content-Type: application/json" -X POST -d '{"A":"xyz","B":"abc"}' http://localhost:8081/concat
```

There are some things to note now. First, the example has two methods, one for add numbers and another one to concat strings. Also, it supports many transport protocols, not only http, so you can launch the client using gRPC:

```sh
go run main.go -grpc.addr=:8082 1 2
```

## Show me the code!

It's time to go deeper. Open `service.go`. This is the file where the service definition is described and also implemented for this example.

Note: I may continue this in the future if I resume my work with go-kit.
