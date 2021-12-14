---
title: Ideas about hosted Blog and Notes search tool
description: ""
lead: ""
date: "2021-09-17T10:07:38-04:00"
lastmod: "2021-09-17T10:07:38-04:00"
tags:
  - blog
  - zettelkasten
draft: true
weight: 50
images: []
contributors:
  - Steve Sosik
---

# Questions for Meilisearch devs
- Can I contribute, and if so, how?
- data consistency, atomic writes, etags update-if-not-exist
- autoincrementing fields
- distinct attributes and sorting: how to ensure a specific version of a
    distinct document is returned for a search, e.g. latest
- word stemming
- supported date formats: just Unix Epoch, or RFC 3339 or ISO 8601?
- filtering on bools?
- sorting on a field plus non-empty query string 
- listen on unix domain socket?

# Ideas
- Hosted on vultr
- ona.little-fluffy.cloud
- nixos
- zola based content serving
    - or a wasm app?
    - or https://arctic-hen7.github.io/perseus/intro.html
- meilisearch backend
- all notes stored in meilisearch under "zettelkasten" index
- indexes for "blog" posts and "bookmarks" as well for actual blog posts and bookmarks
-

# TODOs
- Test with document bodies longer than 1000 words
- [X] tool to import markdown into running server
- github repos for parsing my markdown files and wikipedia backup processing
    - [X] markdown + frontmatter parsing
    - [ ] wikipedia backup processing
- operationalize a nixos vm on vultr
    - borg backups of data
- cli tool to query running server
    - order ASC/DESC by date, weight, revision
    - filter by authors, tags, links, revision, weight
    - render to Markdown and JSON
- cli to edit a specific doc and reindex new copy
    - fetch copy of file in TOML+Body format and save it under
        ~/.local/notes-wip with b64encoded title as filename
    - user edits the file
    - cli to upload the file back into meilisearch, increment `revision` field,
        and delete local file
    - can be used by vim to find a document and allows for editing
- add meilisearch stopwords, typos, synonyms, faceted search for date and tags
    - [X] stopwords
    - [ ] synonyms
    - [X] use facets to default return the latest revision of a document
- find pictures to use as backgrounds/header images

# Updated doc schema
- id: V1 UUID encoded with creation date #required
- authors: list of string #required
- background: path to image
- body: text #required
- links: list of string
- revision: "latest" or number
- subtitle: string
- tags: list of string
- title: string #required
- weight: int (use to count +1s to influence higher ranking) #defaults:0

# Index settings

```bash
# Read all settings: https://docs.meilisearch.com/reference/api/settings.html#get-settings
curl http://localhost:7700/indexes/notes/settings

# Add sortable attributes; https://docs.meilisearch.com/reference/features/sorting.html#configuring-meilisearch-for-sorting-at-search-time
curl http://localhost:7700/indexes/notes/settings/sortable-attributes --data '["date", "revision"]' -XPOST

# Sort by revision and date descending: https://docs.meilisearch.com/reference/api/ranking_rules.html
curl http://localhost:7700/indexes/notes/settings/ranking-rules -d'["words","typo","proximity","attribute","sort","exactness","revision:desc","date:desc"]' -XPOST

# Stop words, from https://www.ranks.nl/stopwords; https://docs.meilisearch.com/reference/api/stop_words.html#get-stop-words
cat <<EOF | curl http://localhost:7700/indexes/notes/settings/stop-words -XPOST -d@-
["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]
EOF

# filterable-attributes: https://docs.meilisearch.com/reference/api/filterable_attributes.html#get-filterable-attributes
curl http://localhost:7700/indexes/notes/settings/filterable-attributes -XPOST -d'["date", "tags", "author"]'

# Distinct attribute for only returning latest revision: https://docs.meilisearch.com/reference/features/distinct.html#example
curl http://localhost:7700/indexes/notes/settings/distinct-attribute -d'"origid"'

# All settings in one shot
cat <<EOF | curl http://localhost:7700/indexes/notes/settings -XPOST -d@-
{
  "displayedAttributes": [
    "*"
  ],
  "searchableAttributes": [
    "*"
  ],
  "filterableAttributes": [
    "author",
    "date",
    "tags"
  ],
  "sortableAttributes": [
    "date",
    "revision",
    "weight"
  ],
  "rankingRules": [
    "words",
    "typo",
    "proximity",
    "attribute",
    "sort",
    "exactness",
    "weight:desc",
    "date:desc",
    "revision:desc"
  ],
  "stopWords": [
    "a",
    "about",
    "above",
    "after",
    "again",
    "against",
    "all",
    "am",
    "an",
    "and",
    "any",
    "are",
    "aren't",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "below",
    "between",
    "both",
    "but",
    "by",
    "can't",
    "cannot",
    "could",
    "couldn't",
    "did",
    "didn't",
    "do",
    "does",
    "doesn't",
    "doing",
    "don't",
    "down",
    "during",
    "each",
    "few",
    "for",
    "from",
    "further",
    "had",
    "hadn't",
    "has",
    "hasn't",
    "have",
    "haven't",
    "having",
    "he",
    "he'd",
    "he'll",
    "he's",
    "her",
    "here",
    "here's",
    "hers",
    "herself",
    "him",
    "himself",
    "his",
    "how",
    "how's",
    "i",
    "i'd",
    "i'll",
    "i'm",
    "i've",
    "if",
    "in",
    "into",
    "is",
    "isn't",
    "it",
    "it's",
    "its",
    "itself",
    "let's",
    "me",
    "more",
    "most",
    "mustn't",
    "my",
    "myself",
    "no",
    "nor",
    "not",
    "of",
    "off",
    "on",
    "once",
    "only",
    "or",
    "other",
    "ought",
    "our",
    "ours",
    "ourselves",
    "out",
    "over",
    "own",
    "same",
    "shan't",
    "she",
    "she'd",
    "she'll",
    "she's",
    "should",
    "shouldn't",
    "so",
    "some",
    "such",
    "than",
    "that",
    "that's",
    "the",
    "their",
    "theirs",
    "them",
    "themselves",
    "then",
    "there",
    "there's",
    "these",
    "they",
    "they'd",
    "they'll",
    "they're",
    "they've",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "until",
    "up",
    "very",
    "was",
    "wasn't",
    "we",
    "we'd",
    "we'll",
    "we're",
    "we've",
    "were",
    "weren't",
    "what",
    "what's",
    "when",
    "when's",
    "where",
    "where's",
    "which",
    "while",
    "who",
    "who's",
    "whom",
    "why",
    "why's",
    "with",
    "won't",
    "would",
    "wouldn't",
    "you",
    "you'd",
    "you'll",
    "you're",
    "you've",
    "your",
    "yours",
    "yourself",
    "yourselves"
  ],
  "synonyms": {},
  "distinctAttribute": "origid"
}
EOF
```

# Simulated doc adds with document revisions

```bash
function api {
    curl http://localhost:7700/$@
}

cat <<EOF | api indexes/notes/documents -XPOST -d@-
[
  {
        "id":"1234-5678-9012",
        "origid":"1234-5678-9012",
        "authors":["steve"],
        "body":"\nsome content\n",
        "date":"2021-09-17T09:28:33-04:00",
        "revision": 1,
        "tags":["test123"],
        "title":"test document"
  },
  {
        "id":"1235-5678-9012",
        "origid":"1234-5678-9012",
        "authors":["steve"],
        "body":"\nsome content\n",
        "date":"2021-09-18T09:28:33-04:00",
        "revision": 2,
        "tags":["test123"],
        "title":"test NEW 1 document"
  },
  {
        "id":"1236-5678-9012",
        "origid":"1234-5678-9012",
        "authors":["steve"],
        "body":"\nsome content\n",
        "date":"2021-09-20T09:28:34-04:00",
        "revision": 3,
        "tags":["test123"],
        "title":"test NEW 2 document"
  },
  {
        "id":"1237-5678-9012",
        "origid":"1234-5678-9012",
        "authors":["steve"],
        "body":"\nsome content\n",
        "date":"2021-09-20T09:28:34-04:00",
        "revision": 4,
        "tags":["test123"],
        "title":"test NEW 3 document"
  }
]
EOF
```


# Search queries

```bash
# Get all tags
api indexes/notes/search -XPOST -d'{"facetsDistribution": ["tags"]}' | jq .

# Basic search
api indexes/notes/search -XPOST -d'{"q": "foobar"}' | jq .

# Search with sorting, need to figure out how to make this work
api indexes/notes/search -XPOST -d'{"q": "foobar","sort": ["date:asc"]}' | jq '.hits[].date'
# Seems to only work when no query string is supplied
api indexes/notes/search -XPOST -d'{"sort": ["date:asc"]}' | jq '.hits[].date'

# https://docs.meilisearch.com/reference/features/filtering_and_faceted_search.html#using-filters

# add a filter on a tag
api indexes/notes/search -XPOST -d'{"q": "foobar", "filter": "tags = dbattery"}' | jq .

```
