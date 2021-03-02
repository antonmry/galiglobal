title=Flink Event Time
date=2021-02-28
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

## Use case example

Let's illustrate this with an example. Our flink job will receive readings from
different sensors. Every sensor will send the measure each 100ms.  We would
like to detect when a measure from a particular sensor is missing, for example
because it was off-line.

Sensors send a json file like this one:

```json
{
  "id": "sensor0",
  "timestamp": 0,
  "measure": 0.1
}
```

The job will generate a normal event but measure will have value -1 when the
event was missed.

## First try with periodic watermark generators

We'll have to choose a [WatermarkStrategy]. We have several options, let's
start with Periodic WatermarkGenerator:

- WatermarkStrategy.[forBoundedOutOfOrderness]: this is a periodic generator
  which allows to deal with records out of order when it's inside a defined
  range.
- WatermarkStrategy.[forMonotonousTimestamps]: this is exaclty the same as
  [forBoundedOutOfOrderness] but the out-of-order tolerance is zero.

In both cases, the framework invokes periodically the Strategy which generates
the watermark. `setAutoWatermarkInterval` allows lo define that periodicity:

```java
env.getConfig().setAutoWatermarkInterval(Duration.ofMillis(100).toMillis());
```

The problem with this approach is we are mixing processing and event time so the
result won't be deterministic, or even correct depending of the circumstances.

For example, [BoundedOutOfOrdernessStrategyJob]. It starts defining the
watermark interval each 100 ms.

```java
env.getConfig().setAutoWatermarkInterval(Duration.ofMillis(100).toMillis());
```

Then we create the DataStream with the watermarks:

```java
DataStream<SensorData> sensorStream =
    env.addSource(source)
        .returns(TypeInformation.of(SensorData.class));

var sensorEventTimeStream =
    sensorStream.assignTimestampsAndWatermarks(
        WatermarkStrategy.<SensorData>forBoundedOutOfOrderness(
            Duration.ofMillis(100)
        ).withTimestampAssigner(
            (event, timestamp) -> event.getTimestamp()
        )
    );
```

To detect missing events, we used a timer so we need a keyed stream and
a KeyedProcessFunction:

```java
sensorEventTimeStream
    .keyBy((event) -> event.getId())
    .process(new TimeoutFunction())
    .addSink(sink);
```

[TimeoutFunction] stores each event in the state and creates a timer for each
one. It cancels the timer if the next event arrives on time. If not, `onTimer`
should be invoked and the event in the state identifying the missing sensor is
emitted.

## Testing and debugging the first implementation

Let's create a simple test: two sensors and one of them misses one of the
measures. When we launch the test [testBoundedOutOfOrdernessStrategyJob], we
obtain the following result:

> Timer: 500 -> sensor0  
> Timer: 500 -> sensor1  
> SensorData{id='sensor0', timestamp=0, measure=0.1}  
> SensorData{id='sensor1', timestamp=0, measure=0.2}  
> SensorData{id='sensor0', timestamp=100, measure=0.3}  
> SensorData{id='sensor1', timestamp=100, measure=0.4}  
> SensorData{id='sensor0', timestamp=200, measure=0.5}  
> SensorData{id='sensor0', timestamp=300, measure=0.7}  
> SensorData{id='sensor1', timestamp=300, measure=0.8}  
> SensorData{id='sensor0', timestamp=400, measure=0.9}  
> SensorData{id='sensor1', timestamp=400, measure=1.0}  
> SensorData{id='sensor0', timestamp=500, measure=-1.0}  
> SensorData{id='sensor1', timestamp=500, measure=-1.0}  

The job doesn't detect the missing event but it detects the end of the stream.
Why? It's time to do some debugging. Debug watermarks issues isn't easy. There
are three options:

- Check the current watermark metric. See [my previous article about the Flink
  setup]. This is ideal for real jobs but a bit more complicated with tests
  because the finish almost immediately.
- Check the current watermark in the Flink UI: as with the previous one, it
  doesn't work with tests if they finish too quickly.
- Introduce a custom operator which has access to the current watermark. I used
  this one which allows also to play with some more advanced operators.

[StreamWatermarkDebugFilter] is basically the internal class [StreamFilter] with
some minor modifications:

- Do nothing, we don't want to filter any event. This could be improved a bit
  avoiding the filtering but because it's a class only for debugging, I didn't
  care too much.
- In the method `processWatermark`, emit the watermark to be consumed for the
next operator and print it for debugging purposes.

We apply the new operator to the job:

```java
sensorEventTimeStream
    .transform("debugFilter", sensorEventTimeStream.getType(), new StreamWatermarkDebugFilter<>())
    .keyBy((event) -> event.getId())
    .process(new TimeoutFunction())
    .addSink(sink);
```

Executing the test again, we can see the watermarks generated:

> Watermark: 9223372036854775807..

Only one watermark is generated: `Long.MAX_VALUE`. This watermark seems to be
executed in the end of the job because it's the bigger possible watermark. This
is consequent with the last two timers we see. They are launched with timestamp
500 but there is no watermark with that value: it's just the end of the job.

So the Watermark generator isn't generating watermark. The only reason I see
for that it's because the job is ending before any any watermark is generated.
We could set the periodic generation with an smaller value but the problem
remains: we are mixing processing and event time so it's really hard to know
how the pipeline is going to proceed in some conditions.

## Final implementation with a Punctuated WatermarkGenerator

We are going to create a generator which will be able to generate watermarks
based in the elements of the stream: a [Punctuated WatermarkGenerator]. So
we create a new job [CustomStrategyJob]:

```java
var sensorEventTimeStream =
    sensorStream
        .assignTimestampsAndWatermarks(
            new WatermarkStrategy<SensorData>() {
                @Override
                public WatermarkGenerator<SensorData> createWatermarkGenerator(
                    WatermarkGeneratorSupplier.Context context) {
                    return new BoundedOutOfOrdernessWatermarks<>(
                        Duration.ofMillis(0)
                    ) {
                        @Override
                        public void onEvent(
                            SensorData event,
                            long eventTimestamp,
                            WatermarkOutput output) {
                            super.onEvent(event, eventTimestamp, output);
                            super.onPeriodicEmit(output);
                        }
                    };
                }
            }
                .withTimestampAssigner((event, timestamp) -> event.getTimestamp())
        );
```

It's basically `BoundedOutOfOrdernessWatermarks` but we modify the method
`onEvent` to invoke `onPeriodicEmit` which emits the watermark. So, instead of
being invoked by the framework, now it emits a new watermark each time it
receives an event. 

The test gives the following output now:

> Watermark: -1  
> Watermark: -1  
> Watermark: 99  
> Watermark: 99  
> Watermark: 199  
> Watermark: 299  
> Watermark: 299  
> Watermark: 399  
> Watermark: 399  
> Watermark: 9223372036854775807  
> Watermark: 9223372036854775807  

This seems a lot better but there is a problem. We don't have a watermark generated
for the sensor 0 at 199. The problem here it's our stream is keyed, so it's being
processed by two different tasks. Watermark work per task so they don't advance at
the same time. To solve this, the easier way is to set parallelism to 1.

Relaunching the test, we obtain the expected result:

> SensorData{id='sensor0', timestamp=0, measure=0.1}  
> SensorData{id='sensor1', timestamp=0, measure=0.2}  
> SensorData{id='sensor0', timestamp=100, measure=0.3}  
> SensorData{id='sensor1', timestamp=100, measure=0.4}  
> SensorData{id='sensor0', timestamp=200, measure=0.5}  
> SensorData{id='sensor0', timestamp=300, measure=0.7}  
> SensorData{id='sensor1', timestamp=200, measure=-1.0}  
> SensorData{id='sensor1', timestamp=300, measure=0.8}  
> SensorData{id='sensor0', timestamp=400, measure=0.9}  
> SensorData{id='sensor1', timestamp=400, measure=1.0}  
> SensorData{id='sensor0', timestamp=500, measure=-1.0}  
> SensorData{id='sensor1', timestamp=500, measure=-1.0}  

## Summary and next steps

[Apache Flink] is a great framework and it supports Event time in a really nice
way. The concept of watermarks as events in the pipeline is superb and full of
advantages over other frameworks. But it's also quite complex to understand
because:

1. The official documentation is scarce.
2. APIs have changed a lot between versions. It's hard to find examples even
   in GitHub.
3. Debug Even Time is tricky.

I wrote this article to contribute in these points. But I have yet some doubts
about different points in Event Time so take my conclusions with scepticism and
draw your own conclusions. If they are different, I would appreciate to know
more about it.

There are some resources which helped me a lot and if you are reading this
probably will help you too:

- Book [Stream Processing with Apache Flink: Fundamentals, Implementation, and
  Operation of Streaming Applications]: chapter 6 provides the better
  explanation I found about watermarks with some nice diagrams. It's a bit
  outdated now but the general concepts apply in the same way.
- Flink mail list: there are some very interesting discussions about this
  particular topic and people tend to help. I recommend two particular threads
  which I found very illustrative:
  - [Timers not firing until stream end].
  - [assignTimestampsAndWatermarks not work after Keyed]

All the code shown is on this [GitHub repository].

Did I miss something? You can leave a comment on [GitHub] or just drop me
a note on [Twitter]!

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
[forMonotonousTimestamps]: https://ci.apache.org/projects/flink/flink-docs-stable/dev/event_timestamp_extractors.html#monotonously-increasing-timestamps
[forBoundedOutOfOrderness]: https://ci.apache.org/projects/flink/flink-docs-stable/dev/event_timestamp_extractors.html#fixed-amount-of-lateness
[BoundedOutOfOrdernessStrategyJob]: TODO
[TimeoutFunction]: TODO
[testBoundedOutOfOrdernessStrategyJob]: TODO
[my previous article about the Flink setup]: https://www.galiglobal.com/blog/2021/20210130-Flink-setup.html#metrics
[StreamWatermarkDebugFilter]: TODO
[StreamFilter]: https://ci.apache.org/projects/flink/flink-docs-master/api/java/org/apache/flink/streaming/api/operators/StreamFilter.html
[Punctuated WatermarkGenerator]: https://ci.apache.org/projects/flink/flink-docs-stable/dev/event_timestamps_watermarks.html#writing-a-punctuated-watermarkgenerator
[CustomStrategyJob]: TODO
[Stream Processing with Apache Flink: Fundamentals, Implementation, and Operation of Streaming Applications]: https://www.goodreads.com/book/show/34431411-stream-processing-with-apache-flink
[Timers not firing until stream end]: http://apache-flink-user-mailing-list-archive.2336050.n4.nabble.com/Timers-not-firing-until-stream-end-td41015.html
[assignTimestampsAndWatermarks not work after Keyed]: http://apache-flink-user-mailing-list-archive.2336050.n4.nabble.com/assignTimestampsAndWatermarks-not-work-after-KeyedStream-process-td27364.html

