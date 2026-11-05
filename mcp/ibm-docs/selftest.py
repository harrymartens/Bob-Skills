#!/usr/bin/env python3
"""Spawn server.py over stdio as an MCP client and exercise every tool against the live sites.
Exit 1 on any failure. Usage: python3 selftest.py"""
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

SERVER = Path(__file__).with_name("server.py")


def _text(result):
    return "".join(getattr(c, "text", "") for c in result.content)


async def main():
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    fails = 0
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = {t.name for t in (await s.list_tools()).tools}
            print("tools:", sorted(tools))
            need = {"search_ibm_docs", "fetch_ibm_doc", "list_ibm_products", "get_ibm_toc", "search_bob_docs", "fetch_bob_doc"}
            if not need <= tools:
                print("FAIL missing tools", need - tools); fails += 1

            out = json.loads(_text(await s.call_tool("list_ibm_products", {"query": "Bob"})))
            print("products:", [p["key"] for p in out][:5])
            if not any(p.get("key") == "SSRD57H" for p in out):
                print("FAIL: Bob product key not found"); fails += 1

            out = json.loads(_text(await s.call_tool("search_ibm_docs", {"query": "backup", "product_key": "SSEPGG_12.1.0", "limit": 3})))
            print("search hits:", out.get("hits"), "first:", out["topics"][0]["title"] if out.get("topics") else None)
            if not out.get("topics") or not all(t["product_key"] == "SSEPGG_12.1.0" for t in out["topics"]):
                print("FAIL: scoped search"); fails += 1
            href = out["topics"][0]["href"]

            doc = json.loads(_text(await s.call_tool("fetch_ibm_doc", {"href_or_url": href, "max_chars": 3000})))
            print("fetch:", doc.get("title"), doc.get("chars"), "chars")
            if "error" in doc or doc.get("chars", 0) < 200 or "backup" not in doc["text"].lower():
                print("FAIL: fetch content"); fails += 1

            bad = json.loads(_text(await s.call_tool("fetch_ibm_doc", {"href_or_url": "https://www.ibm.com/docs/en/db2/12.1.x?topic=no-such-topic-xyz"})))
            print("bad topic ->", bad.get("error"))
            if "error" not in bad:
                print("FAIL: landing page not detected"); fails += 1

            toc = json.loads(_text(await s.call_tool("get_ibm_toc", {"product_key": "SSRD57H_3.0.0", "depth": 1})))
            print("toc entries:", toc.get("entries"))
            if not toc.get("entries"):
                print("FAIL: toc"); fails += 1

            bob = json.loads(_text(await s.call_tool("search_bob_docs", {"query": "mcp server transports", "limit": 3})))
            print("bob search:", [b["path"] for b in bob])
            if not bob:
                print("FAIL: bob search"); fails += 1
            page = json.loads(_text(await s.call_tool("fetch_bob_doc", {"url": bob[0]["url"], "max_chars": 2000})))
            print("bob fetch:", page.get("title"), page.get("chars"), "chars")
            if "error" in page or page.get("chars", 0) < 200:
                print("FAIL: bob fetch"); fails += 1
    print("SELFTEST", "FAILED" if fails else "OK")
    sys.exit(1 if fails else 0)


asyncio.run(main())
