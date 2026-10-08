# Contributing

[简体中文](CONTRIBUTING.md) | **English**

Thanks for contributing! This repository keeps data separate from presentation:

- [`data.yaml`](data.yaml) contains metadata and category definitions, and references category files through `includes`.
- [`data/`](data/) stores paper entries by category (`driving.yaml`, `embodied.yaml`, and `general.yaml`).
- [`README.md`](README.md) and [`README.en.md`](README.en.md) are the Chinese and English homepages. Both are generated automatically; **do not edit them manually**.

## Adding or editing entries

1. Edit the appropriate `data/<category>.yaml` file (for example, `data/driving.yaml` for autonomous driving) and add an entry to its `papers` list:

```yaml
- title: "Full paper title"     # Required
  short: Acronym               # Optional; displayed in bold in the table
  org: Organization name       # Optional; Chinese or English
  org_en: Organization name    # Required if org contains Chinese; otherwise optional
  year: 2025                   # Required; year of first publication, displayed as (year)
  venue: Conference or journal # Required; use arXiv if unpublished; omit the year
  category: driving            # Required; see category IDs below
  links:
    arxiv: "2501.00000"         # arXiv ID, without the domain
    project: "https://..."      # Optional project page
    code: "https://..."         # Optional code repository
    demo: "https://..."         # Optional online demo
  features:                    # Use verified capabilities; may be empty {}
    action: true               # Action-conditioned generation
    realtime: true             # Real-time inference
    closedloop: true           # Closed-loop support
    longhorizon: true          # Long-horizon consistency
  tags: [tag1, tag2]            # Optional free-form keywords
  note: "Chinese summary"      # Required; describe the contribution and interactivity in Chinese
  note_en: "English summary"   # Required; preserve the same facts, numbers, and qualifications
```

2. Set `meta.updated` in `data.yaml` to today's date. The README's last-updated date comes from this field, rather than the Git commit date.

3. Regenerate both READMEs locally:

```bash
pip install pyyaml
python scripts/generate_readme.py
```

4. Include the changed `data/*.yaml`, `data.yaml`, `README.md`, and `README.en.md` in your pull request. CI checks both READMEs against the data. If an English summary or organization translation is missing, the generator identifies the affected entry.

English homepage text is stored in `meta.subtitle_en` and `meta.description_en` in `data.yaml`; category names use `name_en`. Update the corresponding translation whenever the source text changes.

To update both monthly paper-count charts, run:

```bash
pip install matplotlib
python scripts/generate_monthly_chart.py
```

Months are taken from arXiv IDs, with the cutoff month determined by `meta.updated`. Commit both generated `assets/monthly-paper-counts*.png` files.

## Maintaining the automatic scan

Configuration is in `scripts/arxiv_config.yaml`. After retries for a temporary API failure are exhausted, the scanner stops further API requests and tries the official daily Atom feed once. All requests share pacing and `Retry-After` cooldowns. If the server requests a wait longer than 300 seconds, the scan stops making requests for that run.

Runs are classified as complete success, partial scan, or total failure. Only a complete scan with zero candidates reports "No new candidate papers." The feed covers only the latest announcement, so it cannot fill a seven-day window. Matching uses `feed_keywords` against titles and abstracts, categories include cross-listings, and feed dates in the report are announcement dates.

For a partial scan, the workflow first tries to publish the candidates it obtained. After the Issue is created successfully, it commits the reported IDs, then marks the run as failed. If there are no candidates, the run summary still explains the coverage gap. A total failure does not update reported IDs.

When changing search terms, update both `search` and `feed_keywords` (OR within groups, AND between groups). Validate with:

```bash
python3 -m unittest discover -s tests
python3 -u scripts/fetch_arxiv.py --dry-run
```

After pushing an update, start a new run via **Actions → Daily arXiv scan → Run workflow → main**. Re-running an old job uses its original commit; the fetch step prints the actual commit hash.

## Inclusion criteria

- Work should predict or generate the world using a **learnable dynamics model** and serve autonomous driving or embodied AI.
- Prefer work supporting **action conditioning** or **interactive control**. For pure video prediction, explain its relationship to interactivity in both summaries.
- Ensure arXiv IDs and publication metadata are accurate. Omit uncertain information rather than guess.

## Categories

| Category ID | Scope |
| :--- | :--- |
| `driving` | World models for autonomous driving: data engines, neural simulation, prediction, and planning |
| `embodied` | World models for robots and embodied agents |
| `general` | General world models, world foundation models, neural game engines, and related work |
