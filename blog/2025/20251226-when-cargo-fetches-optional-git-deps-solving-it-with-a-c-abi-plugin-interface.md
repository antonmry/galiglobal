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
enabled. Something about this felt wrong but the cost of trying it was low, so
I did.

Turns out that this option didn't work at all. The core problem is that Cargo
may still resolve and fetch Git dependencies even when they are behind disabled
features, which breaks public builds that don’t have access to private
repositories. There's [a GitHub
issue](https://github.com/rust-lang/cargo/issues/15834) about it and it seems
pretty popular.

When consulting options, the LLM insisted on modifying Cargo.toml in the CI
system or when an internal user wanted to build with the feature, but that
options seems a quite ugly workaround. Another option would be to have two
different Cargo.toml but that's also pretty ugly and keeping both files in sync
a pain.

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

I created a demo implementation in [my rust-playground git repo](TODO). There
are two crates:

- `public-cli`: a public CLI that loads a plugin if a shared library exists.
- `private-plugin`: a private crate compiled as a `cdylib` exposing a C-ABI
  function.

The CLI looks for the plugin next to the executable by default (e.g.
`target/debug/libprivate_plugin.so` on Linux,
`target/debug/libprivate_plugin.dylib` on macOS,
`target/debug/private_plugin.dll` on Windows).

If you compile and run the CLI:

```bash 
cargo build -p public-cli 
cargo run -p public-cli
```

It will print:

> running without private feature

If you compile the plugin and because it search for it in the same folder where
the CLI tool is executed:

```bash 
cargo build -p private-plugin 
cargo run -p public-cli
```

It will print:

> plugin says: hello from the private plugin

That's it: adding new functionality to the CLI tool without recompiling it.

### The private plugin (`cdylib`)

`private-plugin/Cargo.toml` declares a `cdylib` crate type so Rust produces a
shared library suitable for dynamic loading:

```toml 
[lib]
crate-type = ["cdylib"]
```

`private-plugin/src/lib.rs` exposes a single C-ABI symbol:

```rust
use std::os::raw::c_char;

#[no_mangle] 
pub extern "C" fn plugin_message() -> *const c_char { 
    b"hello from the private plugin\0".as_ptr() as *const c_char 
}
```

Notes:

- `#[no_mangle]` keeps the symbol name stable for dynamic loading.
- `extern "C"` gives the C ABI.
- The returned string is a static, NUL-terminated byte string so the CLI can
  read it safely as a `CStr`.

### The public CLI (runtime loading)

`public-cli/src/main.rs` looks for the plugin and loads the symbol if found:

```rust
fn plugin_filename() -> String {
    let base = "private_plugin";
    let prefix = env::consts::DLL_PREFIX;
    let ext = env::consts::DLL_EXTENSION;
    format!("{prefix}{base}.{ext}")
}
```

This picks the correct shared library name for the current OS.

```rust
unsafe {
    let lib = libloading::Library::new(path).map_err(|e| e.to_string())?;
    let func: libloading::Symbol<unsafe extern "C" fn() -> *const c_char> =
        lib.get(b"plugin_message").map_err(|e| e.to_string())?;
    let ptr = func();
    if ptr.is_null() {
        return Err("plugin returned null".to_string());
    }
    let c_str = CStr::from_ptr(ptr);
    let message = c_str.to_string_lossy().into_owned();

    Ok(message)
}
```

If the plugin is missing, the CLI prints a fallback message and continues.

## Developer experience

The code in my tool is far more complicated. Plugins are published in Object
Storage and downloaded by the CLI tool. But there's a solid contract between
the CLI tool and the plugins and that makes things easier. Also, I've created a
wrapper over the private crates, so they can be imported internally as
dependencies or externally as plugins. This is convenient to make sure the
external use doesn't cause any issue.

What's even better is that now users can easily create their own plugins and
share them. This isn't a small thing. Modularity is an important piece of
open-source projects and I'm glad it was so easy and quick to add it to the
project so soon.

## Conclusion

I glad I've implemented this pattern. I'm aware this may be overkill and that
there are issues because Rust types and ABI are unstable across compiler
versions. But it's perfect for my CLI tool: solved my problem of how to add
private features to public software and enabled new use cases allowing users to
extend the functionality without having to build the whole project. Let's see
how this evolves with time and if I don't regret this approach.
