# ibm-docs MCP server

Search and read IBM product documentation (www.ibm.com/docs) and IBM Bob docs (bob.ibm.com/docs)
from Bob, so research answers come from fetched pages instead of memory.

Evidence that the endpoints exist and behave as used here: `../../docs/ibm-docs-mcp-feasibility.md`.
The www.ibm.com/docs API is undocumented and its robots.txt disallows crawling `/docs/api`; this
server makes single, cached, low-volume requests on the user's behalf with an honest User-Agent.
If IBM changes or closes the API the tools return an `error` field rather than guessing.

## Tools

| Tool | What it does |
|---|---|
| `search_ibm_docs(query, product_key="", limit=10, start=0)` | JSON search; scope with a versioned key like `SSEPGG_12.1.0` |
| `fetch_ibm_doc(href_or_url, max_chars=20000)` | one topic as clean text, with canonical URL; detects landing-page fallbacks |
| `list_ibm_products(query)` | product name -> key (`SSRD57H` = Bob Premium Package for Z, `SSGUM3` = watsonx Code Assistant) |
| `get_ibm_toc(product_key, section="", depth=2)` | table of contents subtree with hrefs |
| `search_bob_docs(query, limit=10)` | keyword match over bob.ibm.com/docs sitemap paths (the site has no search API) |
| `fetch_bob_doc(url, max_chars=20000)` | one bob.ibm.com/docs page as text |

## Try it from a terminal (no Bob needed)

```bash
pip install "mcp>=1.2"
cd mcp/ibm-docs
python3 server.py --call search_bob_docs '{"query": "skills"}'
python3 server.py --call search_ibm_docs '{"query": "db2 backup", "limit": 3}'
python3 server.py --call fetch_ibm_doc '{"href_or_url": "<href from the search result>"}'
python3 selftest.py        # full stdio round-trip through the MCP protocol
```

The server does not run in the background. Bob (or any MCP client) launches it over stdio when a
tool is called and stops it afterwards. There is no local copy of the docs; results come from
IBM's live API and are cached for an hour in `~/.cache/ibm-docs-mcp`.

## Install into Bob

```bash
pip install "mcp>=1.2"            # 1.x or 2.x both work
python3 mcp/ibm-docs/selftest.py   # live test: spawns the server over stdio and calls every tool
bob mcp add ibm-docs -- python3 /ABSOLUTE/PATH/Bob-Skills/mcp/ibm-docs/server.py
# or paste the block from ../../bob/mcp.json into ~/.bob/settings/mcp.json or <project>/.bob/mcp.json
```

Cache: `~/.cache/ibm-docs-mcp` (override with `IBM_DOCS_CACHE`), one hour TTL (`IBM_DOCS_CACHE_TTL`).

## Self-test result

`python3 selftest.py` on 2026-11-05 from this repo's build environment: all six tools registered,
scoped search returned 764 hits for "backup" in Db2 12.1, `fetch_ibm_doc` returned the 6,616-char
"Backup overview" topic, an unknown topic was detected as a landing page, the Bob Z TOC returned
10 top-level entries, and `search_bob_docs("mcp server transports")` led to a 10,827-char page.
