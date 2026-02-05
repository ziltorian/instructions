# Markdown Formatting Guide for VS Code Instructions

Detailed guide for formatting custom instructions and prompt files.

## General Principles

### Tone and Style

**Directive, Neutral Tone:**
- Write as direct commands and factual statements
- Avoid hypotheticals (could, would, might)
- No emotional language or persuasive rhetoric
- No marketing-style language

**Grammar:**
- Use imperative verbs (Use, Create, Implement)
- Write in present tense (is, creates, returns)
- Prefer active voice
- Keep sentences short (1-2 per bullet point)

**Examples:**

✅ **Good:**
```markdown
- Use tabs for indentation.
- Follow PEP 8 standard.
- Write docstrings for all public functions.
```

❌ **Bad:**
```markdown
- You should probably use tabs for indentation.
- It would be great if you could follow PEP 8.
- We recommend writing docstrings! 🎉
```

## Heading Structure

### Use Case: Custom Instructions

Instructions files require specific heading hierarchy:

```markdown
## Main Section Title           (Required: second-level heading)

### Subsection                  (Third-level for organization)

#### Mandatory Requirements     (Use for critical sections)
```

**Rules:**
- Start with `##` heading (second-level)
- Use `###` for subsections
- Use `####` sparingly for special emphasis
- Never start with `#` (first-level)
- Keep headings descriptive and actionable

### Use Case: Prompt Files

Prompt files are more flexible:

```markdown
## Goal

[Description]

## Requirements

[List of requirements]

## Process

[Step-by-step instructions]
```

## List Formatting

### Bullet Points

**Always use `-` character:**

```markdown
- Item one
- Item two
- Item three
```

**Never use:**
- `*` asterisks
- `+` plus signs
- `•` Unicode bullets

### List Content

**One idea per bullet:**

✅ **Good:**
```markdown
- Use type hints for function parameters.
- Write docstrings for all public functions.
- Follow PEP 8 style guide.
```

❌ **Bad:**
```markdown
- Use type hints for function parameters and write docstrings 
  for all public functions while following PEP 8.
```

**Length guidelines:**
- 1-2 sentences per bullet point
- Maximum 3 sentences for complex points
- Split longer content into sub-bullets

**Sub-bullets:**
```markdown
- Main point
  - Supporting detail
  - Additional detail
- Another main point
```

## Code Formatting

### Inline Code

Use single backticks for:
- Function names: `calculate_total()`
- Variable names: `user_id`
- Class names: `UserManager`
- File names: `config.py`
- Module names: `database.models`

**Examples:**

```markdown
- Use `snake_case` for variables.
- Call `initialize()` before use.
- Import from `core.utils` module.
```

### Code Blocks

**Always specify language:**

````markdown
```python
def example():
    return "code"
```

```typescript
const example = (): string => {
  return "code";
};
```
````

**When to use:**
- Complete, runnable examples
- Template code
- Configuration examples
- Multi-line snippets

**Keep minimal:**
- Show only relevant code
- Use comments to explain
- Omit boilerplate when possible

## Emphasis and Highlighting

### Bold Text

Use **bold** for:
- Keywords and important terms
- Required actions
- Critical warnings

**Examples:**

```markdown
- **Update this file**: when module changes.
- **MUST DO**: validate all inputs.
- Use **absolute imports** for clarity.
```

**Don't overuse:**
- Not every noun needs emphasis
- Avoid bolding entire sentences
- Use sparingly for maximum impact

### Italic Text

Generally avoid italics in instructions. Use bold instead.

### Prohibited Formatting

❌ **Never use:**
- Emojis (😀 🎉 ✨)
- Decorative symbols (━━━ ┃ ╋)
- Color codes
- HTML tags (except code blocks)
- Underlines
- Strike-through

## Section Organization

### Mandatory Requirements Section

**Always include for module instructions:**

```markdown
### Mandatory Requirements
- **Update this file**: when module structure changes, update these instructions.
```

This reminds AI to keep instructions current.

### Standard Sections

**For coding standards:**

```markdown
## Code Style
[Formatting rules]

## Naming Conventions
[Naming patterns]

## Documentation
[Documentation requirements]

## Error Handling
[Error handling patterns]

## Testing
[Testing requirements]

## MUST DO
[Required actions]

## MUST NOT DO
[Prohibited actions]
```

### MUST DO / MUST NOT DO

These sections should be clear and actionable:

✅ **Good:**
```markdown
## MUST DO
- Validate all user inputs before processing.
- Log errors with contextual information.
- Close database connections in finally blocks.

## MUST NOT DO
- Execute raw SQL from user input.
- Catch exceptions without logging.
- Store credentials in code.
```

❌ **Bad:**
```markdown
## MUST DO
- Try to validate inputs when possible.
- Maybe log some errors.

## MUST NOT DO
- Don't do bad things.
```

## Character Limits

### Instructions Files

- **Maximum**: 12,000 characters per file
- **Recommended**: 6,000-8,000 characters
- **Strategy**: Split large files into multiple topic-specific files

### Content Distribution

**In main file (under 12,000 chars):**
- Core standards
- Critical requirements
- Common patterns

**In separate files:**
- Detailed examples
- Edge case handling
- Advanced topics
- Historical context

## Tables

Use tables for comparisons and structured data:

```markdown
| Feature | Requirement | Example |
|---------|-------------|---------|
| Indentation | 4 spaces | `    code` |
| Line length | 100 chars | [example] |
| Quotes | Double | `"string"` |
```

**Formatting:**
- Use pipes `|` for columns
- Align with hyphens in header row
- Keep content concise
- Use for comparisons, not documentation

## Links and References

### Internal Links

Reference other files using relative paths:

```markdown
See [API documentation](../docs/api-reference.md) for details.
Follow [code standards](./Python_Standards.instructions.md).
```

### External Links

Include full URLs with descriptive text:

```markdown
Follow [PEP 8](https://peps.python.org/pep-0008/) guidelines.
See [FastAPI docs](https://fastapi.tiangolo.com/) for examples.
```

## Special Markers

### File Update Reminder

Always include in module instructions:

```markdown
### Mandatory Requirements
- **Update this file**: when module structure changes, update these instructions.
```

### Tool References (Prompt Files)

Reference tools using special syntax:

```markdown
Use #tool:githubRepo to search templates.
Query codebase with #tool:search/codebase.
```

## Examples Section

### Structure for Examples

```markdown
## Examples

### Example 1: [Scenario Name]

[Description of what example demonstrates]

```language
[Code example]
```

[Explanation of example]

### Example 2: [Another Scenario]

[Description]

```language
[Code]
```

[Explanation]
```

### Example Quality

**Good examples:**
- Self-contained and runnable
- Use realistic variable names
- Include comments for clarity
- Show both correct and incorrect usage

**Example format:**

````markdown
### Good Example

```python
def calculate_total(items: list[Item]) -> Decimal:
    """Calculate order total with tax."""
    subtotal = sum(item.price * item.quantity for item in items)
    tax = subtotal * Decimal('0.08')
    return subtotal + tax
```

### Bad Example

```python
def calc(x):  # ❌ Unclear name, no types, no docstring
    return sum([i.p * i.q for i in x]) * 1.08
```
````

## Front Matter (YAML)

### Instructions Files

```yaml
---
name: "Module_Name_Instructions"        # Underscores for display
description: "Brief description"         # What it does
applyTo: "**/*.py"                      # Optional glob pattern
---
```

**Rules:**
- Use underscores in `name` field
- Keep description under 200 characters
- Quote strings with special characters
- Use spaces for indentation (not tabs)

### Prompt Files

```yaml
---
name: create-component                   # Hyphens for command
description: "Generate React component"  # Brief description
argument-hint: "component name"          # Optional hint
agent: "agent"                          # Optional agent
model: "GPT-4o"                        # Optional model
tools: ["githubRepo", "search"]         # Optional tools
---
```

**Rules:**
- Use hyphens in `name` field (for `/command`)
- List tools as array
- Quote all string values
- Validate YAML syntax

## Common Mistakes

### ❌ Mistake 1: Overly Verbose

**Bad:**
```markdown
It is highly recommended that developers should consider using 
type hints whenever possible, as this helps improve code clarity 
and makes it easier for other team members to understand the code.
```

**Good:**
```markdown
Use type hints for all function parameters and return values.
```

### ❌ Mistake 2: Emotional Language

**Bad:**
```markdown
🎉 You should really try to write amazing tests! It's super 
important and will make you feel great about your code! ✨
```

**Good:**
```markdown
Write unit tests for all new functions. Maintain 80% code coverage.
```

### ❌ Mistake 3: Ambiguous Requirements

**Bad:**
```markdown
Try to validate inputs when you can.
Maybe add some error handling.
```

**Good:**
```markdown
- Validate all user inputs before processing.
- Catch and log all exceptions with context.
```

### ❌ Mistake 4: Mixed Formatting

**Bad:**
```markdown
* Use this
+ Or this
- Or even this
```

**Good:**
```markdown
- Use consistent bullet format
- Always use hyphens
- Never mix bullet styles
```

### ❌ Mistake 5: Improper Heading Levels

**Bad:**
```markdown
# Main Title (Too high for instructions)

##### Tiny Section (Too low, skip levels)
```

**Good:**
```markdown
## Main Section

### Subsection

#### Special Emphasis
```

## Verification Checklist

Before finalizing instructions or prompts:

**Content:**
- [ ] Under character limit (12,000 for instructions)
- [ ] Directive, neutral tone throughout
- [ ] No emojis or decorative symbols
- [ ] One idea per bullet point

**Structure:**
- [ ] Proper heading hierarchy (##, ###, ####)
- [ ] Consistent bullet style (-)
- [ ] Required sections included
- [ ] YAML frontmatter valid

**Formatting:**
- [ ] Inline code uses backticks
- [ ] Code blocks specify language
- [ ] Bold used sparingly for emphasis
- [ ] Tables formatted properly

**Quality:**
- [ ] Examples are clear and complete
- [ ] Requirements are specific and verifiable
- [ ] No ambiguous language
- [ ] Links use relative paths

## Templates

### Minimal Instructions Template

```markdown
---
applyTo: "**/*.py"
name: "Python_Standards"
description: "Python coding standards"
---

## Python Standards

### Mandatory Requirements
- **Update this file**: when standards change.

### Code Style
- [Requirements]

### MUST DO
- [Required actions]

### MUST NOT DO
- [Prohibited actions]
```

### Minimal Prompt Template

```markdown
---
name: task-name
description: "Brief description"
agent: "agent"
---

Accomplish [specific goal].

## Requirements

- [Requirement 1]
- [Requirement 2]

## Process

1. [Step 1]
2. [Step 2]
3. [Step 3]
```
