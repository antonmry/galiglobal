title=Gentle (and practical) introduction to Apache Avro
date=2020-08-13
type=post
tags=Kafka, Avro
status=published
~~~~~~

## Introduction

This post is a gentle introduction to [Apache Avro]. After several discussions
with [Dario Cazas] about what's possible with [Apache Avro], he did some research
and summarize it in an email. I found myself looking for that email several times
to forward it to different teams to clarify doubts about Avro. After a while, I
thought it could be useful for others and this is how this post was born.

In summary, [Apache Avro] is a binary format with the following characteristics:

- It's a binary protocol what means it's very efficient (the keys of your data 
aren't copied several times as with JSON) but you can't read it in your text
editor.
- It's a row format so each record is stored independently (for example, Parquet
is a columnar format) so it's bad for aggregations but quite good to send data
independently from one place to other.
- It has a great support to manage the schema of the data. The schema is
typically defined in JSON format.

These characteristics make [Apache Avro] very popular in Event Streaming
architectures based in [Apache Kafka] but it isn't the only possible use.

If you have more interest in [Apache Avro], take a look to the [Apache Avro
Wikipedia Page]






[Apache Avro]: https://avro.apache.org/
[Dario Cazas]: https://www.linkedin.com/in/dcazas/
[Apache Avro Wikipedia Page]: https://en.wikipedia.org/wiki/Apache_Avro

