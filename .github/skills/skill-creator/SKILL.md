---
name: skill-creator
description: Guide for creating effective, universal Agent Skills that work across multiple AI coding platforms (Claude, GitHub Copilot, Cursor, Windsurf, Aider). Use when creating new skills, updating existing skills, or learning skill creation best practices. Includes specifications, examples, and quality standards.
license: MIT
metadata:
  version: "1.0"
  category: ai-assistant-configuration
  author: ziltorian
---

# Skill Creator Guide

Comprehensive guide for creating professional, reusable Agent Skills following the open standard specification.

## Overview

This skill teaches you to create universal Agent Skills that work across multiple AI agent platforms. Skills are structured instruction sets that enable AI agents to perform specialized tasks consistently across projects.

## When to Use This Skill

- Creating a new Agent Skill from documentation or SDK
- Updating an existing skill to follow best practices
- Converting project-specific code into reusable skills
- Learning proper skill structure and formatting
- Validating skill quality before deployment

## Core Principles

### 1. Universal and Reusable

**DO:**

- Create skills that teach "how to work with X"
- Focus on platform/tool/library workflows
- Make skills work in any project context

**DON'T:**

- Create project-specific skills ("how to deploy our app")
- Hardcode project paths, credentials, or URLs
- Assume specific project structure

### 2. Clear and Discoverable

**Description Field is Critical:**
The `description` field determines when agents activate your skill. Include:

- What the skill does (primary capabilities)
- When to use it (trigger keywords)
- Specific terms users might mention

**Example:**

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF documents, extracting data, filling forms, combining PDFs, or when user mentions PDFs, forms, or document processing.
```

### 3. Progressive Disclosure

Structure content for efficient context usage:

**Level 1 - Metadata (~100 tokens):**

- `name` and `description` in YAML frontmatter
- Loaded for all skills at startup
- Enables skill discovery

**Level 2 - Instructions (<5000 tokens):**

- Main SKILL.md body
- Loaded when skill activates
- Keep under 500 lines
- Core workflows and examples

**Level 3 - Resources (on-demand):**

- Files in `references/`, `scripts/`, `assets/`
- Loaded only when needed
- Unlimited detail allowed

## SKILL.md Structure

### Required YAML Frontmatter

```yaml
---
name: skill-name-here
description: Comprehensive description with what it does and when to use it
---
```

### Optional Frontmatter Fields

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files...
license: MIT
compatibility: Requires Python 3.8+ with pdfplumber package
metadata:
  author: your-name
  version: "1.0"
  category: document-processing
---
```

### Markdown Body Structure

Organize instructions for clarity and actionability:

**1. Overview** (1-2 sentences)

- Brief explanation of skill capabilities

**2. When to Use This Skill** (bullet list)

- Specific scenarios where skill applies

**3. Core Workflows** (step-by-step)

- Primary use cases with detailed steps
- Start simple, progress to advanced
- Include code examples

**4. Common Patterns** (examples)

- Reusable code snippets
- Best practices for typical scenarios

**5. Edge Cases** (bullet list)

- Known limitations
- Handling strategies for unusual situations

**6. Examples** (concrete scenarios)

- Input → Process → Expected output
- Real-world use cases

**7. References** (optional)

- Links to supporting files in references/
- External documentation

## Field Specifications

### name (required)

**Constraints:**

- 1-64 characters
- Only lowercase letters, numbers, hyphens (`a-z`, `0-9`, `-`)
- Cannot start/end with hyphen
- No consecutive hyphens (`--`)
- Must match directory name

**Valid:** `pdf-processing`, `data-analysis`, `api-client`
**Invalid:** `PDF-Processing`, `-pdf`, `pdf--processor`

### description (required)

**Constraints:**

- 1-1024 characters (aim for 150-300)
- Must describe BOTH what it does AND when to use it
- Include specific keywords for discovery

**Template:**

```
[What it does]. Use when [scenarios], [tasks], or when user mentions [keywords], [terms], or [phrases].
```

### compatibility (optional)

Use only if skill has specific requirements:

- Required system packages
- Programming language version
- Network access needs

**Examples:**

```yaml
compatibility: Python 3.8+ with pandas and numpy packages
compatibility: Requires git, docker, and internet access
```

### license (optional)

License under which the skill is distributed. Use standard SPDX identifiers.

**Recommended licenses:**

- `MIT` - Maximum adoption, permissive
- `Apache-2.0` - Patent protection
- `CC0-1.0` - Public domain
- `Proprietary` - Custom terms (include LICENSE.txt)

**Examples:**

```yaml
license: MIT
license: Apache-2.0
license: Proprietary. See LICENSE.txt for complete terms
```

**When to use:** Public skills, open-source contributions, community projects  
**When to omit:** Private repos, internal skills, repo-level license covers all

For detailed guidance, see [License Guide](references/license-guide.md).

### metadata (optional)

Arbitrary key-value pairs for additional info:

```yaml
metadata:
  author: team-name
  version: "1.2"
  category: data-processing
  tags: analysis,visualization
```

## Directory Structure

### Minimal Structure

```
skill-name/
└── SKILL.md          # Required
```

### Complete Structure

```
skill-name/
├── SKILL.md          # Required: Main instructions
├── scripts/          # Optional: Executable code
│   ├── process.py
│   └── helper.sh
├── references/       # Optional: Detailed docs
│   ├── REFERENCE.md
│   ├── API_DOCS.md
│   └── EXAMPLES.md
└── assets/           # Optional: Static resources
    ├── template.json
    └── schema.yaml
```

## Using Supporting Directories

### scripts/

**Use for:**

- Self-contained executable code
- Deterministic operations
- Complex logic benefiting from pre-testing
- Code that would be rewritten repeatedly

**Best practices:**

- Document dependencies clearly
- Include helpful error messages
- Handle edge cases gracefully
- Make scripts standalone (don't require other scripts)

**Supported languages:** Python, JavaScript/Node.js, Bash

### references/

**Use for:**

- Detailed API documentation (`REFERENCE.md`)
- Extended examples (`EXAMPLES.md`)
- Domain-specific knowledge
- Technical specifications
- Troubleshooting guides

**Best practices:**

- Keep each file focused on one topic
- Reference from SKILL.md so agents know when to load
- Use clear section headings
- Include concrete examples

### assets/

**Use for:**

- Document templates
- Configuration templates
- Lookup tables and data files
- Images and diagrams (not loaded into context)

**Note:** Assets are NOT loaded into agent context. They're used as input/output templates.

## Quality Checklist

Before finalizing a skill, verify:

**Structure:**

- [ ] `name` follows naming rules and matches directory
- [ ] `description` is comprehensive (150-300 chars ideal)
- [ ] SKILL.md is under 500 lines
- [ ] YAML frontmatter is valid

**Content:**

- [ ] Instructions are actionable with clear steps
- [ ] Examples include inputs, process, outputs
- [ ] Edge cases are documented
- [ ] No hardcoded secrets or credentials
- [ ] No project-specific paths or assumptions

**Universality:**

- [ ] Skill works across different projects
- [ ] Teaches "how to work with X" not "how to configure Y"
- [ ] Multiple focused skills instead of one large skill
- [ ] Can compose with other skills naturally

**Progressive Disclosure:**

- [ ] Most important info in SKILL.md body
- [ ] Detailed docs in references/
- [ ] File references are clear and necessary

## Common Anti-Patterns

### ❌ Avoid These Mistakes

**1. Overly Broad Skills**

```yaml
name: development-helper
description: Helps with coding
```

**Fix:** Create focused skills for specific technologies/workflows

**2. Project-Specific Skills**

```yaml
name: acme-deployment
description: Deploy to Acme Corp infrastructure
```

**Fix:** Teach platform skills (Kubernetes, Docker) that work anywhere

**3. Poor Descriptions**

```yaml
description: PDF stuff
```

**Fix:** Be comprehensive with triggers and specifics

**4. Everything in SKILL.md**

- 1000+ line SKILL.md files
**Fix:** Move detailed docs to references/

**5. Hardcoded Values**

```python
API_KEY = "sk-12345"  # Never!
BASE_URL = "https://acme.internal"  # Project-specific
```

**Fix:** Use configuration, environment variables, or parameters

## Skill Composition

Skills work together automatically. Design each to do one thing well.

**Example:**
User asks: "Analyze this PDF invoice and create a summary presentation"

**Skills activated:**

1. `pdf` - Extract data from PDF
2. `data-analysis` - Analyze extracted data  
3. `pptx` - Create presentation with findings

Each contributes specialized capability without explicit coordination.

## Platform Compatibility

Following the Agent Skills specification ensures compatibility across:

- Claude (claude.ai, Claude Code)
- GitHub Copilot (coding agent, CLI, VS Code)
- Cursor
- Windsurf
- Aider
- Any platform implementing the Agent Skills standard

## Supporting Documentation

For detailed information, see the reference files:

- [Agent Skills Specification](references/agent-skills-specification.md) - Complete open standard specification
- [License Guide](references/license-guide.md) - Choosing and applying licenses to skills
- [GitHub Copilot Skills Spec](references/github-copilot-skills-spec.md) - GitHub-specific conventions
- [Example Skills](references/example-skills.md) - Real-world skill examples with analysis
- [Skills Quick Comparison](references/skills-quick-comparison.md) - Field differences across platforms

## Quick Start Template

```yaml
---
name: your-skill-name
description: [What it does]. Use when [scenarios] or when user mentions [keywords].
license: MIT
compatibility: [Requirements if any]
---

# Skill Name

Brief overview of what this skill enables.

## When to Use This Skill

- Scenario 1
- Scenario 2
- When user mentions X, Y, or Z

## Core Workflows

### Primary Use Case

1. Step one with example
2. Step two with example
3. Step three with example

### Secondary Use Case

[Steps and examples]

## Common Patterns

```language
// Reusable code example
```

## Edge Cases

- Limitation 1 and how to handle
- Limitation 2 and workaround

## Examples

**Example 1: [Scenario]**
Input: [What user provides]
Process: [What agent does]
Output: [Expected result]

## References

For detailed information, see:

- [Agent Skills Specification](references/agent-skills-specification.md) - Complete open standard
- [License Guide](references/license-guide.md) - Choosing appropriate license
- [Example Skills](references/example-skills.md) - Real-world examples with analysis
- [GitHub Copilot Skills Spec](references/github-copilot-skills-spec.md) - GitHub-specific conventions
- [Skills Quick Comparison](references/skills-quick-comparison.md) - Platform differences

---

**You're ready to create professional, universal Agent Skills. Follow these guidelines and refer to the supporting documentation for detailed specifications and examples.**
