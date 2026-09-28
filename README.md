# CMC Skillhub Composer

This repository contains the agent-facing Composer skill for CMC Skill Hub, covering crypto, derivatives, onchain assets, U.S. equities, and cross-asset research.

The skill teaches an agent how to:

- discover CMC Crypto Skill Hub capabilities with `find_skill`;
- match Hub services to the requested fields, asset identity, granularity, and time window;
- validate parameters against each returned `input_schema`;
- execute selected capabilities with `execute_skill`;
- parse wrapped `raw_output` responses;
- handle blocked, partial, stale, and failed tool results;
- verify asset identity, units, time windows, provenance, and evidence coverage;
- render research summaries with the original template router and Markdown format, in the user's language; honor explicitly requested alternative formats.

Connect the CMC Skill Hub MCP server separately. Composer discovers and executes Hub services through `find_skill` and `execute_skill`, including services backed by FastAPI or SQL; it does not automatically select separate data providers or invent backend queries. Missing Hub coverage is reported explicitly; external sources require an explicit user request. Domain references are loaded only when service contracts need clarification. The original Output Template Router, Standard Report Format, language rules and output self-check remain directly in `SKILL.md`. Successful Hub results use that router by default, including short daily overviews and macro reads. The five original report template files are unchanged. Standalone equity research uses the Standard Report Format (or an existing matching template); the equity-context template applies only when the user asks for a crypto connection.

For derivatives, the skill distinguishes market-wide snapshots from venue/instrument data and realized liquidations from heatmaps. For onchain research, it checks chain and contract identity and separates holders, transfers, exchange flows, and swaps. Native U.S. equity data is not interchangeable with tokenized-stock data.

## Repository Layout

The installable skill is in the `cmc-skillhub-composer/` subdirectory:

```text
cmc-skillhub-composer/
  SKILL.md
  reference/
    derivatives.md
    onchain.md
    equities.md
    template-overview.md
    template-macro.md
    template-scanner.md
    template-comparison.md
    template-attribution.md
    template-equity-context.md
    startup/
      README.md
      claude-code.md
      claude-desktop.md
      cursor.md
      codex.md
      openclaw.md
      chatgpt-web.md
      claude-web.md
  scripts/
    inspect_result.py
```

The directory name matches the `name` field in `SKILL.md`.

`scripts/inspect_result.py` is an optional offline Python helper for inspecting wrapped Hub JSON responses while preserving numeric lexemes and separate execution/business states. Agents can follow the response checks directly without running it; parsing does not validate financial evidence.

## Compatibility validation

Run `python3 tests/verify_report_compatibility.py` to check preservation against the original main. See [report regression evidence](tests/report-regression/README.md) for the fixed-data agent comparisons, final outputs, observed failures and limitations. These development tests do not establish live data coverage or a token-cost improvement.

## MCP server install docs (`reference/startup/`)

`reference/startup/` holds per-platform instructions for connecting the **CMC Skill
Hub MCP server** itself (separate from installing this skill). Each file is
self-contained and is meant to be fetched on demand by its raw URL: a local agent
`curl`s the file for its platform and follows it; a web-hosted chat AI reads the same
URL. `reference/startup/README.md` is the index that maps each platform to its file
and lists the shared connection parameters. Raw URL pattern:

```text
https://raw.githubusercontent.com/openCMC/CMC-Skillhub-Composer/<ref>/cmc-skillhub-composer/reference/startup/<file>
```

## Compatibility

This is a standard `SKILL.md` bundle. It works with any host that supports installable agent skills. Install it as the `cmc-skillhub-composer` directory in the host's skills location:

| Host | Install path |
|---|---|
| Claude Code | `$HOME/.claude/skills/cmc-skillhub-composer/` |
| Codex | `$HOME/.agents/skills/cmc-skillhub-composer/` |
| Cursor | `$HOME/.cursor/skills/cmc-skillhub-composer/` (also reads `~/.agents/skills/`) |
| VS Code (Copilot) | `$HOME/.copilot/skills/cmc-skillhub-composer/` (also reads `~/.claude/skills/`, `~/.agents/skills/`) |
| Hermes | `$HOME/.hermes/skills/cmc-skillhub-composer/` |
| OpenClaw | `$HOME/.openclaw/skills/cmc-skillhub-composer/` (also reads `~/.agents/skills/`) |
| Claude Desktop | No folder install — zip the `cmc-skillhub-composer/` folder and upload it via Settings -> Capabilities -> Skills |

`$HOME/.agents/skills/` is a shared skills directory honored by Codex, Cursor, VS Code, and OpenClaw, so it works as a single target for those hosts.

Install the contents of this directory into the skill folder:

```text
cmc-skillhub-composer/
```

The installed folder must remain:

```text
cmc-skillhub-composer
```

Do not install the repository root as the skill. The repository root contains project documentation and is not the skill directory.

`SKILL.md` is the entry point; the `reference/` directory holds the output report templates the skill loads on demand (overview, macro, scanner, comparison, attribution). Both hosts load the skill from `SKILL.md`. Configure the CMC Crypto Skill Hub MCP server separately in the host so that its `find_skill` and `execute_skill` tools are available; the skill resolves whatever id the connected server is registered under and does not require a fixed server name.

## Codex Skill Installer

Use the GitHub directory URL:

```text
$skill-installer install https://github.com/openCMC/CMC-Skillhub-Composer/tree/main/cmc-skillhub-composer
```

Equivalent explicit installer arguments:

```bash
python install-skill-from-github.py \
  --repo openCMC/CMC-Skillhub-Composer \
  --path cmc-skillhub-composer
```

## Send To Agent

Copy the prompt below into Codex, Claude Code, or another local coding agent:

```text
Install the CMC Skillhub Composer skill from https://github.com/openCMC/CMC-Skillhub-Composer/tree/main/cmc-skillhub-composer.

Use the `cmc-skillhub-composer/` directory as the skill source.

Steps:

1. Clone the repository into a temporary directory.
2. Verify that `cmc-skillhub-composer/SKILL.md` exists and that its frontmatter name is `cmc-skillhub-composer`.
3. Install `cmc-skillhub-composer/` as folder `cmc-skillhub-composer` into the current host's skills directory:
   - Claude Code: `$HOME/.claude/skills/`
   - Codex: `$HOME/.agents/skills/`
   - Cursor: `$HOME/.cursor/skills/`
   - VS Code (Copilot): `$HOME/.copilot/skills/`
   - Hermes: `$HOME/.hermes/skills/`
   - OpenClaw: `$HOME/.openclaw/skills/`
   - Claude Desktop: there is no folder install — zip the `cmc-skillhub-composer/` folder and upload it via Settings -> Capabilities -> Skills.
   - If unsure which host you are, `$HOME/.agents/skills/` is honored by Codex, Cursor, VS Code, and OpenClaw.
4. Copy only the contents of `cmc-skillhub-composer/`, preserving the `reference/` subdirectory.
5. If an existing `cmc-skillhub-composer` folder is present, move it to a timestamped backup before installing.
6. Do not install the repository root as the skill.
7. After installation, report the installed path or paths and remind me to restart the host agent so it can load the skill.

Use shell commands where appropriate. Stop and explain the error if the repository cannot be cloned or the expected skill directory is missing.
```

## Manual Install

For Codex:

```bash
tmp_dir="$(mktemp -d)"
git clone --depth 1 https://github.com/openCMC/CMC-Skillhub-Composer "$tmp_dir"
install_dir="$HOME/.agents/skills/cmc-skillhub-composer"
if [ -e "$install_dir" ]; then
  mv "$install_dir" "${install_dir}.bak.$(date +%Y%m%d%H%M%S)"
fi
mkdir -p "$install_dir"
cp -R "$tmp_dir/cmc-skillhub-composer/." "$install_dir/"
```

For other hosts (Cursor, VS Code, Hermes, OpenClaw), use the same steps with `install_dir` set to that host's path from the Compatibility table above. For Claude Desktop, zip `cmc-skillhub-composer/` and upload it via Settings -> Capabilities -> Skills instead.

For Claude Code:

```bash
tmp_dir="$(mktemp -d)"
git clone --depth 1 https://github.com/openCMC/CMC-Skillhub-Composer "$tmp_dir"
install_dir="$HOME/.claude/skills/cmc-skillhub-composer"
if [ -e "$install_dir" ]; then
  mv "$install_dir" "${install_dir}.bak.$(date +%Y%m%d%H%M%S)"
fi
mkdir -p "$install_dir"
cp -R "$tmp_dir/cmc-skillhub-composer/." "$install_dir/"
```

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE) for details. The skill bundle in `cmc-skillhub-composer/` carries its own copy of the license so it stays licensed when installed standalone.
