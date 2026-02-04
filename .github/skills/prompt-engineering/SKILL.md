---
name: prompt-engineering
description: Guide for creating effective prompts for AI coding assistants (Claude, GitHub Copilot, Cursor, Windsurf, Aider). Use when crafting prompts, writing instructions for agents, creating system prompts, optimizing agent behavior, or when user mentions prompts, instructions, system messages, agent configuration, or improving AI responses.
license: MIT
metadata:
  version: "1.0"
  category: ai-assistant-configuration
  author: ziltorian
---

# Prompt Engineering Guide

Comprehensive guide for creating effective prompts that elicit accurate, relevant, and high-quality responses from AI coding assistants across multiple platforms.

## Overview

This skill teaches you to craft professional prompts for AI agents including Claude, GPT-4, GitHub Copilot, and other coding assistants. Master fundamental principles, advanced techniques, platform-specific optimizations, and proven templates.

## When to Use This Skill

- Creating or updating system prompts for AI agents
- Improving existing prompts that produce inconsistent results
- Designing instruction files (.instructions.md, SKILL.md)
- Optimizing agent behavior for specific tasks
- Debugging problematic prompts
- Migrating prompts between platforms
- Creating reusable prompt templates

## Core Principles

### 1. Clarity and Specificity

Always formulate instructions clearly and unambiguously:

**Poor:**

```
Сделай что-нибудь с этим текстом
```

**Good:**

```
Проанализируй этот текст и извлеки все упоминания дат, имен и организаций. 
Представь результат в формате JSON с полями: dates[], names[], organizations[]
```

**Key rules:**

- Use concrete examples instead of abstract descriptions
- Define exact success criteria
- Avoid ambiguity in formulations
- Specify expected output format precisely

### 2. Recommended Prompt Structure

```xml
<role>
Define AI role and primary task
</role>

<context>
Provide necessary background information
</context>

<instructions>
Step-by-step task execution guidelines
1. First step
2. Second step
3. Final step
</instructions>

<output_format>
Precise description of desired result format
</output_format>

<examples>
<example id="1">
<input>Sample input</input>
<output>Expected output</output>
</example>
</examples>

<constraints>
What NOT to do, task boundaries
- Don't include X
- Avoid Y
- Never Z
</constraints>
```

### 3. Effective Delimiters

Choose delimiters based on context complexity:

**Markdown** (recommended for simple prompts):

```markdown
# Main Instructions
## Section 1
- Point A
- Point B

## Section 2
Code example: `inline` or ```blocks```
```

**XML** (best for complex structures):

```xml
<instructions>
  <task>Main task</task>
  <constraints>
    <constraint>Constraint 1</constraint>
    <constraint>Constraint 2</constraint>
  </constraints>
</instructions>
```

**JSON** (for structured data):

```json
{
  "task": "description",
  "parameters": {
    "timeout": 30,
    "retries": 3
  }
}
```

## Core Techniques

### Chain of Thought (CoT)

Encourage step-by-step reasoning:

```
Solve this task step by step:
1. First analyze input data
2. Identify key patterns
3. Formulate hypothesis
4. Test hypothesis with examples
5. Provide final answer with justification
```

**When to use:**

- Complex problem-solving tasks
- Multi-step analysis
- Code debugging
- Architecture decisions

### Few-Shot Learning

Provide 2-5 examples of desired behavior:

```xml
<examples>
<example id="1">
Input: "Куплю iPhone 13"
Output: {"intent": "purchase", "product": "iPhone 13", "sentiment": "neutral"}
</example>

<example id="2">
Input: "Этот телефон ужасен!"
Output: {"intent": "complaint", "product": "unknown", "sentiment": "negative"}
</example>
</examples>

Now process: "Ищу хороший смартфон до 500$"
```

**When to use:**

- Task requires specific output format
- Model needs to learn pattern from examples
- Classification or extraction tasks
- Consistency is critical

### Self-Consistency

For critical tasks, request multiple approaches:

```
Solve this problem using three different methods.
Then compare results and choose the most justified answer.
Explain why you selected this solution.
```

**When to use:**

- High-stakes decisions
- Complex calculations
- Architecture validation
- Security-critical code

## Platform-Specific Optimizations

### Claude (Anthropic)

**Strengths:**

- Precise instruction following
- Excellent XML tag support
- Prefilling capability
- Extended thinking (Opus 4.5)

**Best practices:**

```xml
<instructions>
Be maximally explicit. Claude follows instructions literally.

❌ Don't say: "Don't use markdown"
✅ Say: "Your response must consist of smoothly flowing prose paragraphs without markdown formatting"
</instructions>

<thinking_guidance>
After receiving tool results, carefully analyze their quality and determine optimal next steps before proceeding. Use your thinking for planning and iterations based on new information.
</thinking_guidance>
```

**Prefilling example:**

```python
messages = [
    {"role": "user", "content": "Write JSON with user data"},
    {"role": "assistant", "content": "{"}  # Forces JSON output
]
```

### GPT-4.1 (OpenAI)

**Strengths:**

- Agentic workflows
- Tool calling
- Long context (1M tokens)

**Best practices:**

```xml
<persistence_reminder>
You are an agent. Continue working until user request is fully resolved before ending your turn. Only terminate when certain the task is complete.
</persistence_reminder>

<tool_calling_reminder>
If uncertain about file contents or codebase structure, use your tools to read files and gather information. DO NOT GUESS or make up answers.
</tool_calling_reminder>

<planning_reminder>
You MUST plan in detail before each function call and reason thoroughly about results of previous calls. DO NOT execute entire process only through function calls—this may degrade problem-solving ability.
</planning_reminder>
```

**Long context handling:**

- Place instructions at START and END of context
- Use structured format for documents: `ID: 1 | TITLE: Doc | CONTENT: text...`
- Avoid JSON for large document collections

### GitHub Copilot / Cursor / Windsurf

**Key considerations:**

- Instructions often provided via `.instructions.md` files
- Keep instructions concise (under 500 lines)
- Focus on project-specific conventions
- Use clear section headers

**Example structure:**

```markdown
# Project Context
Brief description of project purpose and architecture

# Code Style Guidelines
- Use TypeScript strict mode
- Prefer functional components
- Follow Repository pattern

# Testing Requirements
- Write unit tests for all services
- Use Jest for testing
- Minimum 80% coverage
```

## Common Patterns

### 1. System Prompt for Coding Agent

```xml
<role>
You are an expert software engineer specializing in [languages/frameworks].
</role>

<capabilities>
- Write production-quality code following best practices
- Debug complex issues systematically
- Optimize for performance and maintainability
- Provide clear explanations for decisions
</capabilities>

<workflow>
For each task:
1. Analyze requirements thoroughly
2. Plan implementation approach
3. Write clean, tested code
4. Verify solution meets requirements
</workflow>

<code_standards>
- Follow [language] idioms and conventions
- Include error handling
- Add meaningful comments for complex logic
- Write self-documenting code with clear names
</code_standards>

<constraints>
- Never introduce security vulnerabilities
- Always validate inputs
- Handle edge cases explicitly
- Maintain backward compatibility
</constraints>
```

### 2. Code Review Prompt

```xml
<task>
Review the provided code for quality, bugs, and improvements.
</task>

<review_criteria>
1. Correctness
   - Logic errors
   - Edge cases
   - Error handling

2. Code Quality
   - Readability
   - Maintainability
   - DRY principle
   - SOLID principles

3. Performance
   - Time complexity
   - Space complexity
   - Optimization opportunities

4. Security
   - Input validation
   - SQL injection risks
   - XSS vulnerabilities
   - Authentication/authorization
</review_criteria>

<output_format>
# Summary
Overall code quality rating and key findings

# Critical Issues
High-priority problems requiring immediate attention

# Improvements
Suggestions for better code quality

# Positive Aspects
What's done well

# Recommendations
Specific action items
</output_format>
```

### 3. Data Analysis Prompt

```xml
<task>
Analyze provided data and deliver comprehensive report.
</task>

<analysis_framework>
1. Descriptive Statistics
   - Key metrics (mean, median, mode)
   - Data distribution
   - Outliers and anomalies

2. Patterns and Trends
   - Temporal trends
   - Correlations
   - Seasonality

3. Segmentation
   - Group by key characteristics
   - Comparative analysis

4. Insights and Recommendations
   - Key findings
   - Actionable recommendations
</analysis_framework>

<output_format>
# Executive Summary
2-3 sentences with main findings

# Key Metrics
Table with primary indicators

# Detailed Analysis
Paragraphs for each framework area

# Visualizations
Description of recommended charts

# Conclusions
Actionable recommendations
</output_format>
```

## Troubleshooting Guide

### Problem: Inconsistent Outputs

**Diagnosis:**

- Results vary significantly between runs
- Model occasionally ignores instructions

**Solutions:**

1. Add 2-5 concrete examples
2. Make constraints more explicit
3. Use XML tags for structure
4. Increase temperature parameter (if too low)
5. Add self-consistency check

### Problem: Instruction Ignored

**Diagnosis:**

- Model consistently ignores specific instruction
- Output format doesn't match requirements

**Solutions:**

1. Move critical instructions to END of prompt
2. Rephrase positively ("Do X" vs "Don't do Y")
3. Add example demonstrating requirement
4. Use XML tags to highlight instruction
5. Check for contradictions with other instructions

### Problem: Hallucinations

**Diagnosis:**

- Model invents information not in context
- Citations reference non-existent sources

**Solutions:**

```xml
<constraints>
- Only use information explicitly provided in context
- If information is unavailable, state "Information not found"
- Never invent data, citations, or sources
- Always quote exact text when referencing context
</constraints>
```

### Problem: Output Too Verbose

**Diagnosis:**

- Responses exceed needed length
- Unnecessary explanations included

**Solutions:**

```xml
<output_requirements>
- Maximum response length: [X] words/tokens
- Be concise and direct
- Omit obvious explanations
- Focus on essential information only
</output_requirements>
```

### Problem: Wrong Format

**Diagnosis:**

- Output doesn't match specified format
- JSON is malformed or incomplete

**Solutions:**

1. Show exact format example
2. Use prefilling (Claude)
3. Add format validation instruction
4. Start assistant response with opening delimiter

## Optimization Checklist

### Before Deployment

- [ ] Clear task definition with success criteria
- [ ] Appropriate delimiter choice (Markdown/XML/JSON)
- [ ] Consistent terminology throughout
- [ ] No contradicting instructions
- [ ] 2-5 examples for complex tasks
- [ ] Edge cases covered
- [ ] Tested on typical inputs
- [ ] Tested on boundary cases
- [ ] Prompt length optimized
- [ ] Platform-specific optimizations applied

### Prompt Length Guidelines

**Simple tasks** (classification, extraction):

- System prompt: 100-300 tokens
- User prompt: 50-200 tokens
- Examples: 0-2

**Medium complexity** (analysis, generation):

- System prompt: 300-800 tokens
- User prompt: 100-500 tokens
- Examples: 2-5

**Complex tasks** (agents, multi-step):

- System prompt: 800-2000 tokens
- User prompt: variable
- Examples: 3-10

## Quick Reference

### Prompt Creation Workflow

1. **Define** goal, audience, success criteria
2. **Structure** role, instructions, format, constraints
3. **Enhance** with examples, delimiters, context
4. **Test** on typical and edge cases
5. **Optimize** based on results

### Common Mistakes to Avoid

❌ **Ambiguous instructions** → Be specific and concrete  
❌ **Contradicting rules** → Review for conflicts  
❌ **Missing examples** → Add 2-5 for complex tasks  
❌ **No output format** → Specify exact format  
❌ **Negative instructions** → Rephrase positively  
❌ **Insufficient context** → Provide necessary background  
❌ **Overly verbose** → Optimize length  
❌ **Platform-agnostic** → Apply platform-specific techniques  

## Examples Repository

Complete prompt templates and examples available in:

- **[references/prompt_templates.md](references/prompt_templates.md)** - Production-ready templates for common tasks
- **[references/practical_guidelines.md](references/practical_guidelines.md)** - Checklists and troubleshooting guides
- **[references/advanced_prompting_techniques.md](references/advanced_prompting_techniques.md)** - Platform-specific optimizations
- **[references/prompt_engineering_fundamentals.md](references/prompt_engineering_fundamentals.md)** - Core principles and theory

## Further Reading

- Agent Skills Specification: <https://agentskills.io/specification>
- Anthropic Prompt Engineering: <https://docs.anthropic.com/claude/docs/prompt-engineering>
- OpenAI Best Practices: <https://platform.openai.com/docs/guides/prompt-engineering>
- GitHub Copilot Documentation: <https://docs.github.com/en/copilot>
