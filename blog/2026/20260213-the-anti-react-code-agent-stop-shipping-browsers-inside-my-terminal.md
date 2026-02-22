# The anti-React Code Agent: stop shipping browsers inside my terminal

*13 February 2026*

---

Code agents are fun. I use them every day. They fit neatly into the tools
I already use: [Bash](https://www.gnu.org/software/bash/),
[Zellij](https://zellij.dev/), [Git](https://git-scm.com/), etc. But if you
live in a terminal, a lot of "code agents" feel like a hostile port of a
web app.

Take Claude Code. I run Claude Opus through it a lot. The model is excellent.
The client is one of the worst terminal experiences I've seen: slow, buggy, and
somehow eating ~400 MB of RAM per instance for what is essentially a cloud API
wrapper. React in a terminal is a self-inflicted wound.

Opencode isn't much better either: basic UX like copy/paste breaks inside a VM.
At least it lets you switch models and it's open source. Codex is the best of
the bunch: faster and lighter, but still bloated. It amazes me how much these
tools struggle with something the terminal does natively: scrolling.

Here's the part that hurts the most: being forced to use a particular model if I
want to use a model. Anthropic models are great for agentic tasks. They're more
decisive, more willing to take risks, and more proactive than OpenAI or Google
models. For code quality, I still find OpenAI better, but only with way too much
human guidance. Google Gemini shines in non-coding tasks.

But if I want Claude Opus on a subscription, I'm forced into Claude Code. That's
not good. Yes, I can use the API instead, but why should I pay 10x more just to
use the tools I like? That's absurd.

The other trend that annoys me is that they're starting to babysit power users.
The best example is compaction: automatic summarization to save tokens. It's
useful when I ask for it. It's infuriating when it happens on its own and
discards the constraints I just spent time setting. This might help
non-technical users. For power users, it's counterproductive and frustrating,
especially given how buggy it is.

So I started thinking about how to make code agents fit my workflow without
fighting the terminal. I wanted something that follows the
[Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy): small pieces
you can compose. The answer was simple: headless mode.

You can run `claude` with `-p` and it will take the prompt, do its magic, and
exit. Everything else in Claude Code is just layers on top. Most code agents
work the same way.

So what happens if you stop using the TUI and just drive the headless mode?
Turns out: it's not only possible, it's surprisingly effective. And it forces
you to learn what "agentic engineering" actually means when the TUI isn't doing
the thinking for you.

Before I knew it, I'd built [BREO](https://github.com/antonmry/breo): the
Browserless React-free Execution Operator. It's meant for my workflow, but the
patterns are portable. The goal of this post is simple: show that you can run
code agents headlessly and still do pretty amazing things.

What [BREO](https://github.com/antonmry/breo) does:

- Runs Claude Code, Codex, and Gemini headlessly. No React TUIs. Subscriptions,
  not API keys.
- Defaults to YOLO mode inside a sandbox ([LimaVM](https://github.com/lima-vm/lima)
  for now) because that's how I usually work with agents.
- Persists conversations in Git for fuzzy search, renaming, and history.
- Lets me decide when compaction happens.
- Saves full state (conversation, agent, model, sandbox) so sessions resume
  cleanly in any folder.

I usually start a conversation with:

```sh
breo -c new_data_api "Let's plan a new data API for my service"
```

It prints a response and then I just continue the conversation with another
command. It remembers and persists the thread:

```sh
breo "Let's run an E2E test to validate that the feature works as expected"
```

I can run other tools between messages and I can also change the agent or the
model in the next message:

```sh
breo -a codex "Let's update the SPEC with our findings"
```

BREO saves the last conversation, agent, model, and sandbox per folder, so I
don't have to think about it. At any moment, `breo status` tells me what's being
used:

```text
directory:     /Users/antonmry/Workspace/Galiglobal/breo
config:        /Users/antonmry/.config/breo
conversations: /Users/antonmry/.config/breo/conversations/breo
conversation:  2026-02-18_20-09-40
agent:         claude
sandbox:       default
```

The nicest thing is that it enables stronger workflows. For example, I always
use a verification loop, so I built `breo loop`. It takes `PLAN.md` (what to
build) and `VERIFICATION.md` (how to prove it works). It lets me select
different agents for implementation and verification.

I usually like Codex for implementation because the code is less verbose, and
Claude Code for verification because it doesn't stop when it hits an environment
problem. And since everything runs inside a VM, I don't care if it nukes the
sandbox along the way. This workflow uses the strengths of both models while
minimizing the weaknesses.

In summary, there's a lot of noise and marketing around code agents right now.
And as usual, when something goes mainstream, it gets worse and more bloated.
But don't forget the fundamentals: understand how code agents work, master
headless mode, identify the powerful patterns, and wire them into your
workflow. That's what drives personal productivity, not the latest tool with a
shiny, bloated UI that you'll forget in three days.

![Anti-React](anti-react.jpg)
