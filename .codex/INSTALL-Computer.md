# Installing Clinical Skills for Codex

Enable clinical skills in Codex via native skill discovery. Just clone and symlink.

## Prerequisites

- Git

## Installation

1. **Clone the clinical-skills repository:**
   ```bash
   git clone https://github.com/aizech/clinical-skills.git ~/.codex/clinical-skills
   ```

2. **Create the skills symlink:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/clinical-skills/skills ~/.agents/skills/clinical-skills
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   cmd /c mklink /J "$env:USERPROFILE\.agents\skills\clinical-skills" "$env:USERPROFILE\.codex\clinical-skills\skills"
   ```

3. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

## Migrating from old bootstrap

If you installed clinical-skills before native skill discovery, you need to:

1. **Update the repo:**
   ```bash
   cd ~/.codex/clinical-skills && git pull
   ```

2. **Create the skills symlink** (step 2 above) — this is the new discovery mechanism.

3. **Remove the old bootstrap block** from `~/.codex/AGENTS.md` — any block referencing `clinical-skills bootstrap` is no longer needed.

4. **Restart Codex.**

## Verify

```bash
ls -la ~/.agents/skills/clinical-skills
```

You should see a symlink (or junction on Windows) pointing to your clinical-skills skills directory.

## Updating

```bash
cd ~/.codex/clinical-skills && git pull
```

Skills update instantly through the symlink.

## Uninstalling

```bash
rm ~/.agents/skills/clinical-skills
```

Optionally delete the clone: `rm -rf ~/.codex/clinical-skills`.

## Getting Started

Once installed, load the radiology context first:

```
Read radiology-context skill
```

Then use any clinical skill:

```
Analyze this CT report for pulmonary nodules
```

> ⚠️ **Security Notice**: These skills work with healthcare concepts. Never input patient-identifiable information (PHI). Use de-identified or synthetic data only.
