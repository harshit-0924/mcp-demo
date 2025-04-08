# MCP Server Demo

## Dynamics of the MCP
The POC illustrates the efficient implementation of MCP as a transparent layer over essential resources, tools, and protocols.

### Installing via Smithery

To install MCP Server Demo for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@harshit-0924/mcp-demo):

```bash
npx -y @smithery/cli install @harshit-0924/mcp-demo --client claude
```

## Getting Started
You can clone the repo and then run
```bash
npm install 
```
To ensure that the dependencies are installed properly.
In order to start the MCP server locally
```bash
npm run start
```
## Available Tools
We have made some tools available in the sample server that you can fork and edit according to needs and requirements. The tools are highly customizable and tweaking them is as easy as modifying the code within.
## Resources
MCP protocol also outlines how a resource can be registered and its relationship with the tools that this or other servers might be providing. Since resources act as storage for the data which can later be used by triggers/tools and MCP server is preferred to be a single source of truth, there are certain ways in which clients can interact with the resources.
</readme>