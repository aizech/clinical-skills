# Installing Clinical Skills for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed

## Installation

### Option 1: Remote Install (Recommended)

Add clinical-skills to the `plugin` array in your `opencode.json` (global or project-level):

```json
{
  "plugin": ["clinical-skills@git+https://github.com/aizech/clinical-skills.git"]
}
```

Restart OpenCode. The plugin auto-installs and registers all 26 clinical skills.

### Option 2: Local Install (for development)

Clone the repository and add the local plugin path:

```bash
git clone https://github.com/aizech/clinical-skills.git ~/.config/opencode/clinical-skills
```

Then add to your `opencode.json`:

```json
{
  "plugin": ["~/.config/opencode/clinical-skills/.opencode/plugins/clinical-skills.js"]
}
```

Restart OpenCode.

### Verify Installation

Ask: "Read radiology-context skill" or "Analyze this CT report for pulmonary nodules"

## Migrating from the old symlink-based install

If you previously installed clinical-skills using `git clone` and symlinks, remove the old setup:

```bash
# Remove old symlinks
rm -f ~/.config/opencode/plugins/clinical-skills.js
rm -rf ~/.config/opencode/skills/clinical-skills

# Optionally remove the cloned repo
rm -rf ~/.config/opencode/clinical-skills

# Remove skills.paths from opencode.json if you added one for clinical-skills
```

Then follow the installation steps above.

## Usage

Use OpenCode's native `skill` tool:

```
use skill tool to list skills
use skill tool to load clinical-skills/radiology-context
```

Always load `radiology-context` first — it configures your clinical environment and ensures other skills work correctly.

Then use any clinical skill:

```
Analyze this CT report for key findings
Query my PACS for recent chest CTs
Find recent literature on lung nodule AI detection
```

## Updating

Clinical-skills updates automatically when you restart OpenCode.

To pin a specific version:

```json
{
  "plugin": ["clinical-skills@git+https://github.com/aizech/clinical-skills.git#v1.0.1"]
}
```

## Troubleshooting

### Plugin not loading

1. Check logs: `opencode run --print-logs "hello" 2>&1 | grep -i clinical`
2. Verify the plugin line in your `opencode.json`
3. Make sure you're running a recent version of OpenCode

### Skills not found

1. Use `skill` tool to list what's discovered
2. Check that the plugin is loading (see above)
3. Ensure you've loaded `radiology-context` first

### Tool mapping

When skills reference Claude Code tools:
- `TodoWrite` → `todowrite`
- `Task` with subagents → `@mention` syntax
- `Skill` tool → OpenCode's native `skill` tool
- File operations → your native tools

## Getting Help

- Report issues: https://github.com/aizech/clinical-skills/issues
- Full documentation: https://github.com/aizech/clinical-skills/blob/main/README.md

> ⚠️ **Security Notice**: These skills work with healthcare concepts. Never input patient-identifiable information (PHI). Use de-identified or synthetic data only.
