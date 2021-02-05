title=Flink Event Time
date=2021-02-07
type=post
tags=Flink
status=published
//~~~~~~

## Introduction

One of the most important concepts for stream-processing frameworks is the
concept of time. There are different concepts of time:

- **Processing time**: it's the time based in the clock of the machine where
  the event is being processed. It's easy to use because it's easy to retrieve
  but because that time changes each time the job executed, the result of the
  job isn't consistent. Each time you execute the job, you may have different
  results which it isn't acceptable for many use cases.
- **Event time**: it's the time based in some of the fields in the event,
  typically a timestamp field. Each time you execute the pipeline with the same
  input, you obtain the same result which it's a good thing. But it also tends
  to be a bit harder to work with it for several reasons we'll cover later in
  the article.
- **Ingestion time** is based in the time when the event was ingested in the
  streaming platform (Kafka) and it usually goes in the metadata. From a Flink
  perspective, we can consider it a particular case of Event Time.

[Apache Flink] has an excellent support for Event time, probably the best of
the different stream-processing frameworks available. For more information, you
can read [Notions of Time: Event Time and Processing Time] in the official
documentation. If you prefer videos, [Streaming Concepts & Introduction to
Flink - Event Time and Watermarks] is a good explanation.

In this article, we'll take a look to Event time pipeline and also to some
common problems and misunderstandings working on this type of pipelines.

## Timestamps and watermarks

When we speak about timestamp in Flink, we are referring to a particular field
in the event.  We can extract it and make it available to Flink so it knows
what's the actual time from the pipeline perspective. The format expected by
Flink is [Unix-time], specified as milliseconds since the Java epoch of
1970-01-01T00:00:00Z, so we may need to do some type of conversion. To do that,
Flink expects an implementation of the [TimestampAssigner]. We'll see later an
example.

Once Flink knows what time it is, it's the moment to generate a watermark. This
is one of the most surprising and genial thinks working with Flink. A watermark
is an special type of event. That means, it flows through your job and it's
processed under the hood for each task. This is a clever way to propagate
a change through the entire pipeline and it's used for more things in flink,
like for example [savepoints].

Generate watermarks is the way to tell the system about progress in event time.
To do it, you use a [WatermarkGenerator]. We'll see later an example.

Both together, [TimestampAssigner] and [WatermarkGenerator] form
a [WatermarkStrategy] which defines how to generate Watermarks in the stream
sources.

## Watermarks

## Summary and next steps

TODO

Did I miss something? You can comment on [GitHub] or just drop me a note on
[Twitter]!

[Getting Started]: https://ci.apache.org/projects/flink/flink-docs-release-1.12/try-flink/local_installation.html
[Hands-on Training]:https://ci.apache.org/projects/flink/flink-docs-release-1.12/learn-flink/
[Flink Web Dashboard]: http://localhost:8081/
[using breakpoints]: https://www.jetbrains.com/help/idea/using-breakpoints.html
[Testing Flink Jobs]: https://ci.apache.org/projects/flink/flink-docs-stable/dev/stream/testing.html
[test complete jobs]: https://ci.apache.org/projects/flink/flink-docs-stable/dev/stream/testing.html#testing-flink-jobs
[official Flink training tests]: https://github.com/apache/flink-training/blob/master/ride-cleansing/src/test/java/org/apache/flink/training/exercises/ridecleansing/RideCleansingTest.java
[Profiling Tools and IntelliJ IDEA Ultimate]: https://blog.jetbrains.com/idea/2020/03/profiling-tools-and-intellij-idea-ultimate/
[VisualVMLauncher plugin]: https://github.com/krasa/VisualVMLauncher/
[VisualVM MBeans Browser]: https://visualvm.github.io/plugins.html
[Flink metrics]: https://ci.apache.org/projects/flink/flink-docs-release-1.12/ops/metrics.html#metrics
[GitHub repository]: https://github.com/antonmry/flink-playground

[Apache Flink]: https://flink.apache.org/
[GitHub]: https://github.com/antonmry/galiglobal/pull/37
[Twitter]: https://twitter.com/antonmry

[Notions of Time: Event Time and Processing Time]: https://ci.apache.org/projects/flink/flink-docs-release-1.12/concepts/timely-stream-processing.html#notions-of-time-event-time-and-processing-time
[Unix time]: https://en.wikipedia.org/wiki/Unix_time
[Streaming Concepts & Introduction to Flink - Event Time and Watermarks]: https://www.youtube.com/watch?v=QVDJFZVHZ3c

[TimestampAssigner]: https://ci.apache.org/projects/flink/flink-docs-stable/api/java/org/apache/flink/api/common/eventtime/TimestampAssigner.html
[savepoints]: https://ci.apache.org/projects/flink/flink-docs-stable/ops/state/savepoints.html
[WatermarkGenerator]: https://ci.apache.org/projects/flink/flink-docs-master/api/java/org/apache/flink/api/common/eventtime/WatermarkGenerator.html
[WatermarkStrategy]: https://ci.apache.org/projects/flink/flink-docs-release-1.12/api/java/org/apache/flink/api/common/eventtime/WatermarkStrategy.html
