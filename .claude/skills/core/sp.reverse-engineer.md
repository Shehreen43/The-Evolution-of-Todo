---
name: sp.reverse-engineer
description: Analyze existing code to generate specifications and architecture summaries. Use when: (1) User asks to reverse engineer code, (2) User requests spec extraction from implementation, (3) User wants workflow documentation or architecture analysis, (4) User asks to summarize functionality of a module.
---

# Reverse Engineering Skill

Extract specifications, architecture, and workflows from existing implementations.

## Inputs

Identify target for analysis:
- Directory or file path
- Specific module or component
- Full codebase or subset

## Analysis Workflow

### 1. Explore Structure

Discover project organization:
```
File types and extensions
Directory structure
Entry points and main files
Configuration files
Dependency manifests
```

### 2. Identify Components

For each significant area:
- List files involved
- Identify entry points
- Map dependencies
- Find external integrations

### 3. Analyze Behavior

For each component:
- Read source files
- Identify public interfaces
- Trace data flow
- Document side effects
- Note configuration points

### 4. Extract Specifications

Generate structured output:

```markdown
# Reverse Engineered: <Target>

## Overview
High-level description of functionality

## Components
### Name
- Files: [list]
- Purpose: [description]
- Interfaces: [list]

## Data Flow
[Description of how data moves through system]

## Dependencies
- Internal: [list]
- External: [list]

## Patterns Identified
- Architectural patterns
- Design patterns used
- Anti-patterns present

## Workflows
### Workflow 1
1. Step
2. Step
```

### 5. Document Architecture

Include:
- System boundaries
- Component relationships
- Deployment model if identifiable
- Integration points

### 6. Summarize Findings

Present:
- Key capabilities
- Implicit business logic
- Design decisions evident in code
- Technical constraints
- Recommendations if requested

## Output Destinations

Write to:
- `specs/<feature>/spec.md` if extracting feature spec
- `specs/<feature>/plan.md` if extracting architecture
- `history/analysis/<slug>.md` for general analysis

## Guardrails

### Do
- Trace actual behavior, not assumptions
- Document what exists, not what should exist
- Note inconsistencies or unclear areas
- Map dependencies accurately
- Preserve original terminology

### Do Not
- Invent features not present in code
- Assume intent without evidence
- Include implementation details not present
- Recommend refactoring in analysis
- Speculate about missing functionality

### Defer
- Performance optimization suggestions
- Recommendations for improvement
- Best practice violations
- Security assessments (unless requested)

## Triggers

Use this skill when:
- User says "reverse engineer this code"
- User asks "create spec from this implementation"
- User requests "analyze this project and generate documentation"
- User asks "extract architecture from codebase"
- User says "summarize functionality of this module"
