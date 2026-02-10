---
name: add-table-of-contents
description: "Generate and add table of contents to markdown document"
argument-hint: "path to markdown file"
agent: "agent"
---

Generate table of contents for a markdown document and insert it at the appropriate location.

## Input

Document path: `${input:documentPath}`

## Process

### Step 1: Read Document

Read the entire document to extract:
- All `##` and `###` level headings
- Existing TOC section (if present)
- Best insertion point (after frontmatter/title)

### Step 2: Generate TOC

Create table of contents with:
- Links to all major sections: `[Display Text](#anchor-link)`
- Hierarchical structure with indentation for subsections
- TOC header (e.g., "Contents" or "Содержание")

**Anchor generation:**
1. Convert heading text to lowercase
2. Replace spaces with hyphens
3. Remove special characters (keep: letters, numbers, hyphens, underscores)
4. Preserve numbers in their positions
5. Handle non-ASCII characters properly

### Step 3: Insert or Update

- If no TOC exists: insert after frontmatter or document title
- If TOC exists: replace with updated version
- End TOC with horizontal rule `---`

## Format Rules

### What to Include

**Include:**
- `##` level headings (main sections)
- `###` level headings (subsections)

**Exclude:**
- `#` level heading (document title)
- `####` and below (too detailed)
- Headings inside code blocks
- Commented-out headings

### Hierarchy Format

**Top-level sections (##):**
```markdown
- [Section Name](#anchor)
```

**Subsections (###):**
```markdown
  - [Subsection Name](#anchor)
```

## Anchor Examples

| Heading | Anchor |
|---------|--------|
| `## System Overview` | `#system-overview` |
| `## 1. Introduction` | `#1-introduction` |
| `### 2.1 Components` | `#21-components` |
| `## API & Storage` | `#api--storage` |

## Template

```markdown
## Contents

- [Section 1](#section-1)
- [Section 2](#section-2)
  - [Subsection 2.1](#subsection-21)
  - [Subsection 2.2](#subsection-22)
- [Section 3](#section-3)

---
```

## Special Cases

### Code Blocks

Ignore heading markers inside code blocks. Track state with triple backticks.

### Duplicate Headings

If multiple headings have identical text, markdown engines auto-append numbers:
- First: `#anchor`
- Second: `#anchor-1`
- Third: `#anchor-2`

### Special Characters

- Quotes, colons, asterisks → remove
- Ampersands `&` → convert to `--`
- Parentheses → keep in display, remove from anchor

## Verification

After generating TOC:

- [ ] All `##` and `###` headings included (except title)
- [ ] Subsections indented with 2 spaces
- [ ] Anchor links are lowercase
- [ ] Spaces replaced with hyphens
- [ ] Numbers preserved in anchors
- [ ] TOC ends with `---`
- [ ] Links navigate correctly in preview

## Output Format

```
✅ TOC added to ${input:documentPath}

Structure:
- X sections (## level)
- Y subsections (### level)

Location: [After title / After frontmatter / Replaced existing]
```
