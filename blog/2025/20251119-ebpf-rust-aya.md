# eBPF with Rust using Aya (and working on M2/M3/M4 mac devices!)

_19 November 2025_

---

I've been playing around with eBPF lately, what amazing technology. But it was
pretty frustrating in the beginning. First, I had to run it in a Mac Studio M3
Ultra, not in a Linux machine. Also, I've tried with Podman in a Linux machine
without much success. Finally, [Aya](https://github.com/aya-rs/aya)
dependencies are pretty heavy and ended up trying to use nightly version of
Rust and other over complicated setups.

The whole point of this article is to document what I did to make it work, so
I can reuse it in the future and, hopefully, it's useful for others.

## Initial setup

I found way easier in the end to use a VM instead of containers for this.
[Lima](https://lima-vm.io/) is a great software for that.

So basically, I retrieved the [CI Aya file from
Github](https://github.com/aya-rs/aya-template/blob/main/.github/workflows/ci.yml)
and used to create the Lima template. You can find it in [my GitHub
repository](https://github.com/antonmry/rust-playground/blob/main/ebpf-aya/lima-aya.yaml).
If you are following this in the future, it may be good to use the last updated
version of the CI file to create your own template.

After that, everything should be way easier:

```sh
limactl start --name aya-ci lima-aya.yaml
```

You can easily ssh into the VM with:

```sh
limactl shell aya-ci
```

The next step is to check that eBPF can be used:

```sh
limactl shell aya-ci sudo bpftrace -l
limactl shell aya-ci sudo sudo bpftool feature probe
```

## Create a new Aya project

Let's create the Aya project that detects when a SSL invocation happens. We can
test it first with the following command:

```sh
limactl shell aya-ci sudo bpftrace -e 'uprobe:/usr/lib/aarch64-linux-gnu/libssl.so.3:SSL_write { printf("SSL_write PID=%d\n", pid); }'
```

and in a different terminal:

```sh
limactl shell aya-ci curl -v https://www.galiglobal.com
```

The output should be something like this:

>  Attaching 1 probe...
> SSL_write PID=4304
> SSL_write PID=4304
> SSL_write PID=4304

Now let's create the project with the following command:

```sh
limactl shell cargo generate --git https://github.com/aya-rs/aya-template --branch main \
  --name ssl-write \
  --define uprobe_fn_name=SSL_write
```


Comments? You can find me in [BlueSky](https://bsky.app/profile/anton.galiglobal.com).

