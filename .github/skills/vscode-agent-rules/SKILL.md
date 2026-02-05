---
name: vscode-agent-rules
description: Create VS Code custom instructions files (.instructions.md) and prompt files (.prompt.md) for GitHub Copilot. Use when creating agent rules, coding standards, module-specific instructions, or reusable prompts for VS Code projects. Includes YAML frontmatter format, markdown formatting standards, and file organization patterns.
license: MIT
---

# VS Code Agent Rules Creator

Create professional custom instructions and prompt files for GitHub Copilot in VS Code following official specifications and best practices.

## Overview

This skill teaches how to create two types of VS Code customization files:

1. **Custom Instructions** (`.instructions.md`) - Define coding standards, guidelines, and module-specific rules
2. **Prompt Files** (`.prompt.md`) - Create reusable prompts for common development tasks

Both file types use YAML frontmatter and Markdown, but serve different purposes and have distinct formats.

## Custom Instructions Files

### What They Are

Custom instructions define common guidelines that automatically influence AI responses. They can apply to all files or specific file types using glob patterns.

### File Locations

**Workspace instructions** (project-specific):

- Primary: `.github/instructions/{name}.instructions.md`
- Legacy: `.github/copilot-instructions.md` (single file, auto-applies to all)

**User instructions** (cross-workspace):

- Stored in VS Code user profile
- Available across all workspaces

### YAML Frontmatter Format

```yaml
---
name: "Module_Name_Instructions"        # Required: display name, underscore-separated
description: "Brief description"         # Required: what these instructions do
applyTo: "**/*.py"                      # Optional: glob pattern for auto-apply
---
```

**Field specifications:**

- `name` - Display name shown in UI (use underscores between words)
- `description` - Brief explanation of the instructions' purpose
- `applyTo` - Glob pattern defining which files trigger auto-application
  - Use `**` for all files
  - Examples: `**/*.py`, `modules/api/**`, `**/*.{ts,tsx}`
  - If omitted, instructions are not applied automatically

### Body Content Structure

Use directive, neutral tone with imperative verbs. Keep under 12,000 characters.

**Required structure:**

```markdown
## Main Section Title

### Subsection

#### Mandatory Requirements
- **Update this file**: when module changes, update these instructions.

### Code Style
- Use tabs for indentation.
- Follow PEP 8 standard.
- Use type hints for all function parameters.

### Error Handling
- Use custom exceptions from `modules.exceptions`.
- Always include contextual error messages.

### MUST DO
- Requirement 1
- Requirement 2

### MUST NOT DO
- Prohibition 1
- Prohibition 2
```

**Formatting rules:**

- Main heading: `##` (second level)
- Subsections: `###` (third level)
- Lists: `-` bullet character only
- Code elements: single backticks `className`, `function_name`
- Emphasis: **bold** for keywords only
- Examples: code blocks only, minimal
- No emojis, decorative symbols, or emotional language
- One idea per bullet point (1-2 sentences max)

### Common Patterns

**General coding standards:**

```markdown
---
applyTo: "**/*.py"
name: "Python_Code_Standards"
description: "Python coding standards for the project"
---

## Python Code Standards

### Code Style
- Use tabs for indentation.
- Follow PEP 8 guidelines.
- Use type hints for function parameters and returns.

### Documentation
- Write docstrings for all public functions.
- Include parameter descriptions and return types.

### Testing
- Write unit tests for new functions.
- Maintain 80% code coverage minimum.
```

**Module-specific instructions:**

```markdown
---
applyTo: "modules/api/**"
name: "API_Module_Instructions"
description: "Instructions for API module development"
---

## API Module

### Mandatory Requirements
- **Update this file**: when API structure changes, update these instructions.

### Module Description
Handles REST API endpoints and request processing.

### Module Tasks
- Process incoming HTTP requests
- Validate request data
- Return formatted JSON responses

### Architecture
- `endpoints.py`: Route definitions
- `handlers.py`: Request processing logic
- `validators.py`: Input validation

### MUST DO
- Validate all incoming data before processing.
- Use `@app.route` decorators for endpoints.
- Return proper HTTP status codes.

### MUST NOT DO
- Process unvalidated user input.
- Expose internal error details in responses.
```

**Documentation writing guidelines:**

```markdown
---
applyTo: "docs/**/*.md"
name: "Documentation_Writing_Guidelines"
description: "Standards for project documentation"
---

## Documentation Writing Guidelines

### Grammar and Style
- Use present tense verbs.
- Write in second person (you).
- Use active voice.
- Write factual statements and direct commands.

### Structure
- Use headings to organize content.
- Use bullet points for lists.
- Include code examples where applicable.

### Markdown Conventions
- Use code blocks for code snippets.
- Include links to related resources.
- Use tables for structured data.
```

## Prompt Files

### What They Are

Prompt files define reusable prompts for common development tasks. Unlike instructions that auto-apply, prompts are triggered on-demand by typing `/prompt-name` in chat.

### File Locations

**Workspace prompts** (project-specific):

- `.github/prompts/{name}.prompt.md`

**User prompts** (cross-workspace):

- Stored in VS Code user profile
- Available across all workspaces

### YAML Frontmatter Format

```yaml
---
name: create-react-form                 # Required: prompt name (lowercase-hyphen)
description: "Generate React form"      # Required: what the prompt does
argument-hint: "form name and fields"   # Optional: hint text for chat input
agent: "agent"                          # Optional: ask|edit|agent|custom-agent
model: "GPT-4o"                        # Optional: specific model
tools: ["githubRepo", "search/codebase"] # Optional: available tools
---
```

**Field specifications:**

- `name` - Prompt name used after `/` in chat (lowercase with hyphens)
- `description` - Short description shown in prompt list
- `argument-hint` - Optional hint text shown in chat input field
- `agent` - Which agent runs the prompt: `ask`, `edit`, `agent`, or custom agent name
- `model` - Language model to use (if not specified, uses current selection)
- `tools` - List of available tools for this prompt

### Body Content Structure

Write clear instructions for the AI to follow when the prompt is triggered.

**Structure:**

```markdown
## Goal

[What this prompt accomplishes]

## Requirements

[Specific guidelines and rules]

## Process

1. [Step one]
2. [Step two]
3. [Step three]

## Examples

[Concrete examples of expected behavior]
```

**Variables you can use:**

- `${workspaceFolder}` - Workspace root path
- `${file}` - Current file path
- `${selection}` - Selected text
- `${input:variableName}` - User input from chat
- `${input:variableName:placeholder}` - Input with placeholder text

**Referencing files:**

- Use Markdown links with relative paths: `[design system](../docs/design-system.md)`
- Reference tools: `#tool:githubRepo`, `#tool:search/codebase`

### Common Patterns

**Code generation prompt:**

```markdown
---
name: create-react-form
description: "Generate new React form component"
agent: "agent"
model: "GPT-4o"
tools: ["githubRepo", "search/codebase"]
---

Generate a new React form component based on project templates.

Ask for form name and fields if not provided.

## Requirements

- Use design system components from [Form.md](../docs/design-system/Form.md)
- Use `react-hook-form` for state management
- Define TypeScript types for form data
- Use uncontrolled components with `register`
- Use `yup` for validation with TypeScript types

## Process

1. Ask user for form name and required fields
2. Check existing forms in `#tool:githubRepo` for patterns
3. Generate component with proper types
4. Include validation schema
5. Add to appropriate directory
```

**Code review prompt:**

```markdown
---
name: security-review
description: "Perform REST API security review"
agent: "ask"
model: "Claude Sonnet 4"
---

Perform REST API security review and provide TODO list.

## Check Points

- All endpoints protected by authentication/authorization
- User inputs validated and sanitized
- Rate limiting implemented
- Security event logging enabled

## Output Format

Return TODO list in Markdown, grouped by:
- Priority (High/Medium/Low)
- Issue type (Authentication/Validation/Logging)

Include specific file paths and line numbers for each issue.
```

**Scaffolding prompt:**

```markdown
---
name: create-test-suite
description: "Generate test suite for module"
argument-hint: "module path"
agent: "agent"
tools: ["search/codebase"]
---

Create comprehensive test suite for ${input:modulePath}.

## Process

1. Analyze module structure using `#tool:search/codebase`
2. Identify public functions and classes
3. Generate unit tests with:
   - Setup and teardown
   - Happy path tests
   - Edge case tests
   - Error condition tests
4. Create test file in `tests/` directory
5. Use project's testing framework (pytest/jest)

## Requirements

- Follow existing test patterns in repository
- Mock external dependencies
- Aim for >80% code coverage
- Include docstrings for test functions
```

## Key Differences

| Aspect | Custom Instructions | Prompt Files |
|--------|-------------------|--------------|
| **Extension** | `.instructions.md` | `.prompt.md` |
| **Purpose** | Auto-apply guidelines | On-demand tasks |
| **Trigger** | Automatic via `applyTo` | Manual via `/name` |
| **Name format** | Underscores: `Module_Name` | Hyphens: `module-name` |
| **Location** | `.github/instructions/` | `.github/prompts/` |
| **Content** | Standards and rules | Task instructions |
| **Variables** | Not supported | Supported (`${var}`) |

## Best Practices

### For Custom Instructions

**DO:**

- Keep under 12,000 characters
- Use directive, neutral tone
- One idea per bullet point
- Include **Update this file** task for module instructions
- Use specific, verifiable requirements
- Reference external files for details

**DON'T:**

- Use emojis or decorative symbols
- Write long narrative explanations
- Duplicate information across files
- Include emotional or marketing language
- Make requirements ambiguous

### For Prompt Files

**DO:**

- Write clear, specific instructions
- Include concrete examples
- Use variables for flexibility
- Reference related files with links
- Test prompts before sharing
- Keep prompts focused on single task

**DON'T:**

- Duplicate instructions already in files
- Make prompts too generic
- Forget to specify required tools
- Overcomplicate simple tasks

## File Organization

**Recommended structure:**

```
project-root/
├── .github/
│   ├── instructions/
│   │   ├── Python_Code_Standards.instructions.md
│   │   ├── API_Module.instructions.md
│   │   └── Frontend_Standards.instructions.md
│   ├── prompts/
│   │   ├── create-component.prompt.md
│   │   ├── security-review.prompt.md
│   │   └── generate-tests.prompt.md
│   └── copilot-instructions.md  # Optional: single file for all
```

## Creating Files

### Using VS Code UI

**For instructions:**

1. Open Chat view
2. Select **Configure Chat** (gear icon) > **Chat Instructions**
3. Select **New instruction file**
4. Choose **Workspace** or **User profile**
5. Enter filename and create

**For prompts:**

1. Open Chat view
2. Select **Configure Chat** > **Prompt Files**
3. Select **New prompt file**
4. Choose location and create
5. Edit YAML frontmatter and body

### Using Command Palette

- `Chat: New Instructions File`
- `Chat: New Prompt File`
- `Chat: Configure Instructions`
- `Chat: Configure Prompt Files`

## Using the Files

### Custom Instructions

**Auto-apply** - Triggered automatically when `applyTo` pattern matches:

```yaml
applyTo: "**/*.py"  # Applies to all Python files
```

**Manual** - Add via Chat view **Add Context** > **Instructions**

**Verify** - Check "References" section in chat response

### Prompt Files

**In Chat** - Type `/` followed by prompt name:

```
/create-react-form formName=LoginForm
```

**From Command Palette:**

- `Chat: Run Prompt` - Select from list

**From Editor:**

- Open `.prompt.md` file
- Click play button in title area
- Choose current or new chat session

## Troubleshooting

### Instructions not applying

1. Verify file location in `.github/instructions/`
2. Check `applyTo` glob pattern matches target files
3. Ensure `github.copilot.chat.codeGeneration.useInstructionFiles` setting enabled
4. Check chat logs via **Chat Debug view**

### Prompt not triggering

1. Verify file location in `.github/prompts/`
2. Check `name` field matches what you type after `/`
3. Ensure chat.promptFilesRecommendations setting if using recommendations
4. Test by opening file and clicking play button

### Common issues

**Character limit exceeded:**

- Instructions must be under 12,000 characters
- Split into multiple files if needed
- Move detailed content to referenced files

**YAML parsing errors:**

- Ensure proper indentation (spaces, not tabs)
- Quote strings with special characters
- Check frontmatter delimiters (`---`)

**Glob patterns not matching:**

- Test patterns: `**/*.py` (all Python), `src/**` (src folder)
- Use `.github/**` for GitHub folder
- Combine with `{ts,tsx}` for multiple extensions

## Examples and Templates

For complete working examples, see:

- [references/instruction-examples.md](references/instruction-examples.md) - Full instruction file templates
- [references/prompt-examples.md](references/prompt-examples.md) - Complete prompt file examples
- [references/formatting-guide.md](references/formatting-guide.md) - Detailed markdown formatting rules

## References

- Official VS Code docs: [Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- Official VS Code docs: [Prompt Files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- Community examples: [GitHub Awesome Copilot](https://github.com/github/awesome-copilot)
