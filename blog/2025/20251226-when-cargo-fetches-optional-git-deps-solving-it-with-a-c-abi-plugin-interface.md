# When Cargo fetches “optional” Git deps: solving it with a C-ABI plugin interface

*26 December 2025*

---

## The problem

I've been working on a new public CLI tool. Fascinating project that I can't
wait to publish. One of things I needed was to reuse some of our backend code
in the tool itself, but I can't to publish that code at the moment. So what can
we do?

## Naïve approach and why it fails

My first approach was to use a [Cargo
feature](https://doc.rust-lang.org/cargo/reference/features.html) with a
dependency to [a private git
repository](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#specifying-dependencies-from-git-repositories)
with the crate. We could build internally the tool with that feature, and
external users could do the same without it. With this approach, I would need
to add some secrets to our CI systems to download the crate. Not great but
expected.

I checked with an LLM this approach and confirmed it was the way go with one
caveat. We would need an "adapter crate" in the public crate so the dependency
wasn't direct and the crate wasn't needed when building without the feature
enabled. Something about this felt wrong but the cost of trying it was low, so I
did.

## Constraints you must respect

Turns out that this option didn't work at all. Cargo always try to resolve the
dependency. There's [a GitHub
issue](https://github.com/rust-lang/cargo/issues/15834) about it and it seems
pretty popular.

When consulting options, the LLM insisted on modifying Cargo.toml in the CI
system or when an internal user wanted to build with the feature, but that
options seems a quite ugly workaround. Another option would be to have two
different Cargo.toml but that's also pretty ugly and keeping both files in sync a pain.

## The workable solution: runtime plugin with a C ABI

After a bit of research, I ended evaluating to use a C Application Binary
Interface (C ABI). This is a pretty interesting Rust feature:

The private crate is compiled as a runtime plugin
([cdylib](https://doc.rust-lang.org/reference/linkage.html#r-link.cdylib)) with
libloading in runtime. With this approach, the CLI will shows the feature only
if the plugin has been downloaded and it's placed in predefined path.

This allows users to build the tool without the private dependencies, but also
have control of what features use. I just added a subcommand `plugin` to allow
the user to discover, download and enable plugins. It has also simplified the
setup: there's no dependency in the CI system except for distribution (if you
install the CLI via a package mangers, the plugins are also included).

As usual, it's a trade-off. This approach is less performant (but that's ok for
this CLI tool) and there are some limitation about what you can pass through
the ylib boundary safely.

During the planning phase, the code agent was summarizing the pros and cons and
I remember myself thinking if this would be a huge rabbit hole on its own. I
used similar approaches with Java modules in the past, and it was a very useful
pattern but I wasn't sure how mature would this in Rust Again, I decided to
give it a try. Any of the alternatives were appealing at all and, at least, I
would learn about C ABI in Rust.

## Implementation walkthrough

TODO

## Developer experience

## Testing and CI

## Tradeoffs and alternatives

## Conclusion
