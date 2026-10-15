---
name: pi-web-search
description: Uses the pi-web-access extension for resilient web search with Exa first and DuckDuckGo HTML as the fallback. Use when the user asks to search the web, look up current information, or wants free/no-key search behavior with automatic provider fallback.
---

# Web Search via pi-web-access: Exa first, DuckDuckGo fallback

Use the `web_search` tool provided by the `pi-web-access` extension. If the tool is not available, tell the user to install and load the extension first:

```bash
pi install npm:pi-web-access
```

Restart Pi after installing the extension.

## Default behavior

Do **not** use `provider: "auto"` or `provider: "all"` for this workflow. They bypass the requested Exa → DuckDuckGo behavior.

For each web-search request:

1. Try **Exa** first:

```js
web_search({
  query: "...",
  provider: "exa",
  workflow: "none"
})
```

Preserve the user's requested search options, such as `queries`, `numResults`, `recencyFilter`, `domainFilter`, and `includeContent`, unless the user asks otherwise. Use `workflow: "none"` by default so the tool returns results without opening the curator UI; only use `summary-review` or `auto-summary` if the user asks for a curator or generated summary.

If Exa returns usable results, answer from those results and indicate that the search used Exa.

2. If Exa fails, retries, or returns an error such as rate limit/quota, `429`, timeout, provider unavailable, authentication/configuration failure, invalid response, or empty/error output, retry the same search with DuckDuckGo HTML:

```js
web_search({
  query: "...",
  provider: "duckduckgo",
  workflow: "none"
})
```

Keep the same query and filters where possible. DuckDuckGo is explicit-only in `pi-web-access`, so it must be selected with `provider: "duckduckgo"`. Remind the user that DuckDuckGo HTML search has unreliable recency filtering and applies domain filters locally after results are returned.

3. After Exa has failed in the current session, use DuckDuckGo as the default provider for later searches in that same session unless the user explicitly asks to try Exa again. Mention the switch briefly, e.g. “Exa is erroring, so I’m using DuckDuckGo HTML search now.”

4. If both providers fail, report the failure clearly and suggest the next options:

```json
{
  "exaApiKey": "exa-..."
}
```

or a self-hosted SearXNG endpoint:

```json
{
  "searxngBaseUrl": "https://your-searxng-instance"
}
```

Do not silently fabricate search results.

## Batch searches

For multiple queries, first pass the full `queries` array to Exa:

```js
web_search({
  queries: ["query 1", "query 2"],
  provider: "exa",
  workflow: "none"
})
```

If the batch fails because Exa is unavailable or unhealthy, retry the batch with DuckDuckGo:

```js
web_search({
  queries: ["query 1", "query 2"],
  provider: "duckduckgo",
  workflow: "none"
})
```

If only individual queries fail after an otherwise successful response, retry just those failed queries with DuckDuckGo.

## Response style

When answering after a search, briefly include which provider supplied the results, especially after a fallback:

- “Found via Exa: …”
- “Exa errored, so this used DuckDuckGo HTML search: …”

Always preserve source URLs and summarize uncertainty when results conflict.