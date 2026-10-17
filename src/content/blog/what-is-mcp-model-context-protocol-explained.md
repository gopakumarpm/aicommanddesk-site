---
title: "What Is MCP? The Model Context Protocol Explained (With Stick Figures)"
description: "MCP is the open standard that lets AI assistants like Claude and ChatGPT connect to your tools and data. Watch a 68-second stickman explainer, then read the plain-English breakdown."
date: 2026-10-17
author: "AI Command Desk"
category: "Tutorials"
tags: ["mcp", "claude", "chatgpt", "ai agents", "explainer"]
image: "/videos/mcp-explainer-poster.jpg"
imageAlt: "Stick figure diagram showing an AI host with MCP clients connected to GitHub, Files and Database servers"
featured: false
draft: false
---

You have probably seen the letters **MCP** next to Claude, ChatGPT and a growing list of AI tools. It stands for **Model Context Protocol**, and it is the reason an AI assistant can do more than chat: read your files, check your calendar, or look up a pull request.

Watch the 68-second explainer first, then use the notes below as a cheat sheet.

<video controls preload="metadata" poster="/videos/mcp-explainer-poster.jpg" style="width:100%;border-radius:12px;margin:1.5rem 0">
  <source src="/videos/mcp-explainer.mp4" type="video/mp4">
  Your browser does not support the video tag. <a href="/videos/mcp-explainer.mp4">Download the video</a>.
</video>

## The problem: AI is smart but locked out

An AI model on its own only knows what it was trained on and what you paste into the chat. It cannot see your files, your apps or your company data.

Before MCP, connecting an AI to a tool meant writing a custom integration. Two assistants and three tools meant six separate connectors, each one built, tested and maintained by hand.

## The fix: one open standard

MCP is a shared language for that connection. Think of it as **USB-C for AI**: build each side once, and everything plugs in. With MCP, two assistants and three tools need two plugs on one side and three on the other, instead of six custom cables.

## The three parts

- **Host:** the app you use, such as Claude or ChatGPT.
- **MCP client:** a component inside the host that talks to one server. The host runs one client per server.
- **MCP server:** a small program that wraps a tool or data source, such as GitHub, your files or a database.

A server can offer three kinds of things:

- **Tools:** actions the AI can ask for, like "list pull requests".
- **Resources:** data the AI can read, like a document.
- **Prompts:** reusable templates for common tasks.

The client and server exchange JSON-RPC messages.

## One request, step by step

Say you ask: *"Summarise my open pull requests."*

1. **Discover:** the client asks the GitHub server what it can do and gets a list of tools.
2. **Decide:** the model reads that menu and picks the tool it needs.
3. **Call:** the client sends the call to the server, usually after you approve it.
4. **Fetch:** the server talks to GitHub and sends the result back.
5. **Answer:** the model turns the raw data into a clear summary for you.

## Why it matters

- **Build once, use anywhere:** the same server works with any MCP-capable assistant, including Claude and ChatGPT.
- **You stay in control:** assistants typically ask before running a tool, so you approve what happens.
- **Less glue code:** teams spend time on useful tools instead of rebuilding connectors.

## Key takeaways

- MCP is an open standard that connects AI assistants to tools and data.
- Hosts run clients, clients talk to servers, servers wrap your tools.
- The flow is always discover, decide, call, answer.
- A server written once can be reused across assistants.

If you are new to all of this, start with our guide to [using AI without writing code](/blog/how-to-use-ai-without-coding), then see the [non-technical guide to ChatGPT at work](/blog/non-technical-guide-to-chatgpt-at-work).

---

*Get practical AI tips every week. Subscribe to the AI Command Desk newsletter.*
