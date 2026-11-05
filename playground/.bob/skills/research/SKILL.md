---
name: research
description: Use when asked to research, investigate, compare, fact-check, "find out whether", summarise what the docs say, or write anything whose value depends on claims about the outside world being true (memos, briefs, recommendations, competitive comparisons, "does X support Y").
---

# Research that survives a hostile reader

The failure this skill prevents: an answer that sounds authoritative, cites a URL that
returns 200, and is wrong, because the claim came from memory and the URL was never read.
The remedy is mechanical: every claim carries a tag, every tag maps to a fetched page and
an exact quote from it, and `scripts/check_citations.py` refuses the document otherwise.

## Workflow

1. **Decompose.** Turn the request into numbered questions. For each, write what evidence
   would settle it (an official doc page, a changelog, a spec section, a benchmark table).
   Put the list in your todo tool before searching.
2. **Search wide, fetch deep.** Search to find candidate pages; then fetch every page you
   intend to cite with `python scripts/fetch_page.py URL --tag S1 --cache sources/`.
   Prefer primary sources: vendor docs, the spec itself, the repository, the paper.
   A blog post summarising the spec is not the spec.
3. **Quote, don't paraphrase, into Sources.** For each tag, copy one full sentence verbatim
   from the fetched text (use `--grep "phrase"` to find it). This is the sentence that
   proves the claim. If no sentence on the page proves it, the page does not support it.
4. **Write claims with tags.** Each factual bullet ends with its tag(s): `... loads from ~/.bob/skills [S2]`.
   Separate what the source says from what you infer: inference gets the word "inferred" and no tag.
5. **Red-team pass.** For every conclusion, write one line starting "This is wrong if..."
   and try to find that evidence. Search for the opposite claim, a newer version, a
   deprecation notice, or a caveat in the same doc. Record what you found under
   `## Counter-evidence`, even when it is "searched for X, found nothing".
6. **Run the checker.** `python scripts/check_citations.py research.md --cache sources/`.
   Fix every ERROR: a quote that is not on the page means you misremembered; go back to step 3.
7. **Report with confidence per question**, not per document: High (primary source quoted),
   Medium (secondary source, or primary source but older than the product version), Low
   (inference, or sources disagree). State what you could not verify and why.

## Document contract (the checker depends on it)

```markdown
# <Question>

## Answer
- <claim sentence> [S1]
- <claim sentence> [S1][S3]
- Inferred: <your reasoning, no tag>

## Counter-evidence
- This is wrong if <condition>. Searched <where>; found <what> [S4] / found nothing.

## Confidence
| Question | Level | Why |
|---|---|---|

## Sources
[S1] https://exact.url/page — "one full sentence copied verbatim from that page"
[S2] https://exact.url/other — "another full sentence copied verbatim"
```

A source line needs the URL, an em dash or hyphen, and a quote of at least six words in
straight or curly double quotes. One tag per line. Tags are numbered in first-use order.

## Fetching inside Bob

Bob has no built-in web tool unless `experiments.webFetch` is enabled in settings. The reliable
path is `execute_command` running `python scripts/fetch_page.py` (curl under the hood). For IBM
product docs and Bob's own docs, prefer the `ibm-docs` MCP server if it is configured
(`search_ibm_docs` then `fetch_ibm_doc`; `search_bob_docs` then `fetch_bob_doc`): it returns clean
text and the canonical URL. Save what it returns to `sources/S<n>.txt` so the checker can verify
the quote offline.

## When the page cannot be fetched

- Try the raw form: GitHub `raw.githubusercontent.com`, docs sites' `.md` mirror, or `?format=text`.
- If a site blocks automated fetches, say so, cite it as **unverified**, give the URL,
  and do not put a quote you did not read into Sources.
- Never fabricate a URL. If you cannot remember one exactly, search for it.

## Red flags in your own behaviour

| Thought | Reality |
|---|---|
| "I know this, no need to fetch" | Memory is the source of the wrong answers this skill exists to stop. Fetch it. |
| "The URL returned 200, so the citation is good" | 200 means the page exists, not that it says what you claim. Quote it. |
| "I'll paraphrase the quote so it reads better" | The checker compares verbatim text. Paraphrase goes in the claim, not in Sources. |
| "The user is in a hurry, skip the red-team pass" | The red-team pass is where "does not support X" turns into "supports X since v2". It is the value. |
| "Sources disagree, I'll pick the one that fits" | Report the disagreement with both tags and the dates. That is the finding. |
