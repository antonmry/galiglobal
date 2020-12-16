title=Gentle (and practical) introduction to Apache Avro - Part 2
date=2020-12-07
type=post
tags=Kafka, Avro, Schema Registry
status=published
//~~~~~~

## What's the problem with the Schema Registry (SR)

<!-- TODO: add link to the previous part -->

In the previous part we reviewed the best way to work with [Apache Avro] in
Event Streaming architectures. It's efficient and improves data quality
but, as usual, there is a problem. What happens when consumers don't have
access to the SR? They can't deserialize the message!

This usually happens in two different scenarios:

- Multi-datacenter architecture: you have more than one datacenter and they are
  too far away to have an extended cluster between them. In that case, you need
  to move messages from one datacenter to another, typically using [MirrorMaker
  2] or [Confluent Replicator].
- Hybrid architecture: on-prem Kafka cluster which it's replicating data to
  cloud services (not necessarily Kafka based).

For the first scenario, Confluent provides a [Multi-datacenter setup] but it's
based in primary and "only-for-read" follower registries so producers in other
Datacenters have to write in the primary registry out of their network. In many
cases, that's a big issue in terms of high availability, security, etc.

RedHat is working in a feature to publish updates in their SR in Kafka so it can
be replicated in a different location. It seems promising but it's quite new yet.
See [How to detect changes to schema from outside registry?] for more info.

Another option would be don't publish new schemas using producers but using
some type of higher governance tool, typically CI/CD. This may work because you
always write in the primary registry but it's a problem for several use cases,
for example, Change Data Capture, where the producer should evolve the schema
following the evolution of database tables.

All these inconveniences become much worse in the second scenario where we
could have different technologies and service registries involved. If you take
a look to the schema management offerings of the principal cloud providers, you
will easily discover Event Streaming and asynchronous schema management is
a discipline quite young with many unsolved problems.

## Simplest solution: don't use an schema registry

Given the current state-of-the-art of the technology, one simple solution would
be avoid the Schema Registry. We could simply produce in a different format or
transform it before to move data outside of the cluster. We loose both main
advantages of the SR: we can't enforce schema compatibility anymore and our
messages aren't so efficient, which it's critical when moving big amounts of
data between datacenters / clouds... but it's simple and it works.

If we take this approach, we should choose what format to use to the upload.
[JSON] is a quite popular option but very inefficient in terms of size of the
message and CPU requirements to parse it. Another option would be [Apache
Parquet].  It's more efficient than JSON but it's a columnar storage so it
isn't a good choice if we need to manage every message independently.

A good option is to use [Apache Avro] with the schema embedded. To do that, we
should write our own serializer. We can do it extending
[org.apache.kafka.common.serialization.Serializer] as you can see in
[AvroEmbeddedSerializer] example.

<!-- TODO: compare Avro+schema with JSON

> docker-compose exec broker kafka-log-dirs --bootstrap-server localhost:9092 \
--topic-list test  --describe
-->

{"version":1,"brokers":[{"broker":1,"logDirs":[{"logDir":"/var/lib/kafka/data","error":null,"partitions":[{"partition":"test-0","size":960,"offsetLag":0,"isFuture":false}]}]}]}
{"version":1,"brokers":[{"broker":1,"logDirs":[{"logDir":"/var/lib/kafka/data","error":null,"partitions":[{"partition":"test2-0","size":910,"offsetLag":0,"isFuture":false}]}]}]}



[Apache Avro]: https://avro.apache.org/
[MirrorMaker 2]: https://cwiki.apache.org/confluence/display/KAFKA/KIP-382%3A+MirrorMaker+2.0
[Confluent Replicator]: https://docs.confluent.io/platform/current/multi-dc-deployments/replicator/index.html
[Multi-datacenter setup]: https://docs.confluent.io/6.0.0/schema-registry/multidc.html#multi-datacenter-setup
[How to detect changes to schema from outside registry?]: https://github.com/Apicurio/apicurio-registry/issues/823
[JSON]: https://en.wikipedia.org/wiki/JSON
[Apache Parquet]: https://parquet.apache.org/
[org.apache.kafka.common.serialization.Serializer]: https://kafka.apache.org/082/javadoc/org/apache/kafka/common/serialization/Serializer.html
[org.apache.kafka.common.serialization.Deserializer]: https://kafka.apache.org/082/javadoc/org/apache/kafka/common/serialization/Deserializer.html
[AvroEmbeddedSerializer]: TODO
