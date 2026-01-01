---
name: sp.constitution
description: Non-negotiable rules governing skill design, structure, and lifecycle. Use when creating, validating, or iterating on any skill in the system.
license: Core Governance
---

# Skill Constitution

## 1. Project Scope

This constitution defines the non-negotiable rules governing all skills within the system. Every skill, regardless of scope, author, or purpose, MUST comply with these rules.

**Scope includes:**
- Skill directory structure and file organization
- SKILL.md format, content limits, and writing standards
- YAML frontmatter constraints and allowed fields
- Progressive disclosure patterns
- Bundled resource management (scripts/, references/, assets/)
- Skill lifecycle workflow
- Validation and packaging requirements

**This constitution does not cover:**
- Skill distribution mechanisms
- User-facing documentation
- Marketing or promotional content

## 2. Core Principles

### 2.1 Context Economy

The context window is a shared, finite resource. Skills share this space with system prompts, conversation history, other skills metadata, and user requests.

Claude is already highly capable. Only add context that Claude cannot derive from its training or the current conversation.

Challenge every piece of information: Does Claude truly need this explanation? Does this paragraph justify its token cost?

### 2.2 Conciseness Over Verbosity

Prefer concise, dense content over verbose explanations. Write for efficiency, not readability for humans.

Delete information that Claude can infer or derive. Remove redundancy. Eliminate "just in case" content.

### 2.3 Progressive Disclosure

Skills use a three-level loading system:

1. **Metadata** (name + description): Always loaded, ~100 tokens
2. **SKILL.md body**: Loaded when skill triggers, under 500 lines
3. **Bundled resources**: Loaded as needed by Claude, unlimited

Keep SKILL.md lean. Move detailed content to references/ files. Claude loads references only when it determines they are needed.

### 2.4 Reusability and Determinism

Identify operations that are repeatedly rewritten and extract them into scripts/ for deterministic execution.

Identify information that is repeatedly referenced and document it once in references/.

Identify templates or boilerplate that are repeatedly used and store them in assets/.

Each resource type serves a distinct purpose. Do not conflate them.

### 2.5 Clear Separation

Separate concerns across file types:

- **SKILL.md**: Workflow guidance, trigger conditions, selection criteria
- **scripts/**: Executable code for deterministic operations
- **references/**: Documentation for Claude to reference while working
- **assets/**: Files for output, not for context loading

## 3. Skill Design Rules

### 3.1 Required Directory Structure

Every skill MUST follow this structure:

```
skill-name/
├── SKILL.md (required)
├── scripts/ (optional)
├── references/ (optional)
└── assets/ (optional)
```

### 3.2 SKILL.md Requirements

SKILL.md consists of two parts:

**Frontmatter (required):**
```yaml
---
name: skill-name
description: Description of what the skill does and when to use it
---
```

**Body (required):**
Markdown content providing workflow guidance and resource references.

### 3.3 YAML Frontmatter Constraints

**Allowed fields:**
- `name`: Required, hyphen-case, lowercase, max 64 characters
- `description`: Required, max 1024 characters, includes when-to-use triggers
- `license`: Optional
- `allowed-tools`: Optional, list of permitted tools
- `metadata`: Optional, for internal use

**Field rules:**

`name` MUST match the directory name exactly. MUST contain only lowercase letters, digits, and hyphens. MUST NOT start or end with a hyphen. MUST NOT contain consecutive hyphens.

`description` MUST include both what the skill does AND specific contexts/scenarios for when to use it. This is the primary triggering mechanism. All "when to use" information belongs here, not in the body.

### 3.4 Writing Style Rules

- Use imperative/infinitive form for instructions
- Use declarative, authoritative language
- Write for another Claude instance, not for humans
- Omit conversational filler, marketing language, and motivational statements
- Omit examples unless structurally required for demonstrating a pattern
- Omit "just in case" content

### 3.5 SKILL.md Content Limits

- Body MUST NOT exceed 500 lines
- Body SHOULD be under 5,000 words
- When approaching limits, split content into references/ files
- Link to references files from SKILL.md with clear usage guidance

### 3.6 scripts/ Rules

**Purpose:** Executable code (Python/Bash/etc.) for deterministic or error-prone operations.

**When to include:**
- Code that is repeatedly rewritten
- Operations requiring deterministic reliability
- Complex logic that benefits from testing

**Rules:**
- Scripts MUST be executable
- Scripts SHOULD be tested before packaging
- Scripts MAY be executed without loading into context
- Claude MAY read scripts for environment-specific adjustments

### 3.7 references/ Rules

**Purpose:** Documentation and reference material for Claude to load as needed.

**When to include:**
- Detailed API documentation
- Database schemas
- Company policies
- Complex workflow guides
- Information too lengthy for SKILL.md

**Rules:**
- Reference files MUST be linked from SKILL.md
- Reference files SHOULD include navigation guidance at the top for files over 100 lines
- Avoid deeply nested references; keep references one level deep from SKILL.md
- Information SHOULD live in either SKILL.md or references/, not both

### 3.8 assets/ Rules

**Purpose:** Files not loaded into context but used in output.

**When to include:**
- Templates (PPT, DOCX, HTML/React boilerplate)
- Brand assets (logos, icons, fonts)
- Sample data for testing

**Rules:**
- Assets are NOT loaded into context
- Assets are copied or referenced in output
- Assets MAY be any file type

## 4. Prohibited Practices

### 4.1 Forbidden Files

Skills MUST NOT contain:
- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- USER_GUIDE.md
- GETTING_STARTED.md
- Any similarly named documentation files

### 4.2 Forbidden Content

- Duplication of information across SKILL.md and references/
- Verbose explanations where conciseness suffices
- "Just in case" content not immediately needed
- User-facing documentation mixed with skill instructions
- Auxiliary context about the skill creation process
- Setup and testing procedures
- Marketing or promotional language
- Conversational filler

### 4.3 Forbidden Patterns

- Overloading SKILL.md with reference material
- Unjustified bundled resources (include only what is needed)
- Deeply nested reference hierarchies
- Missing navigation in long reference files
- Confusing resource types (scripts as documentation, references as executables)

## 5. Authoritative Skill Lifecycle

### 5.1 Understanding

Before creating a skill, understand concrete usage examples. Identify:
- What functionality the skill supports
- What users would say to trigger the skill
- What workflows the skill enables

Conclude with clear understanding of scope and triggers.

### 5.2 Planning

Analyze each concrete example to identify reusable components:
- scripts/: Operations repeatedly rewritten
- references/: Information repeatedly referenced
- assets/: Templates repeatedly used

Create a list of resources to include.

### 5.3 Initialization

Create skill directory structure using init_skill.py or equivalent template:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

This creates:
- SKILL.md with frontmatter and TODO placeholders
- scripts/ with example files
- references/ with example files
- assets/ with example files

### 5.4 Editing

Implement reusable resources first:
- Create and test scripts
- Write reference documentation
- Add or update assets

Delete example files not needed.

Update SKILL.md:
- Complete frontmatter (name, description with triggers)
- Write body with workflow guidance
- Link to references files with usage guidance

### 5.5 Validation

Run validation before packaging:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

This automatically validates:
- YAML frontmatter format and required fields
- Skill naming conventions
- Description completeness
- File organization

Fix validation errors before proceeding.

### 5.6 Packaging

Package validated skills into distributable .skill files:

```bash
scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

This creates a .skill file (zip format) containing all skill files.

### 5.7 Iteration

After real usage:
- Notice struggles or inefficiencies
- Identify updates needed to SKILL.md or resources
- Implement changes
- Re-validate and re-package
- Test again

## 6. Compliance and Enforcement

### 6.1 When Deviation Is Allowed

Deviation from these rules is allowed only when:
- A specific use case clearly requires it
- The deviation does not violate the core principles
- The deviation is documented where relevant

Deviation is NOT allowed for:
- Required directory structure
- YAML frontmatter format and allowed fields
- Prohibited files
- SKILL.md content limits

### 6.2 Self-Correction Requirement

Before packaging, creators MUST:
- Review SKILL.md for conciseness
- Verify no prohibited files exist
- Confirm progressive disclosure is properly implemented
- Ensure all validation checks pass

### 6.3 Skill Rejection Criteria

A skill is REJECTED if:
- SKILL.md does not exist
- Frontmatter is missing name or description
- Name does not match directory or naming conventions
- Description is empty or lacks when-to-use triggers
- Prohibited files are present
- Validation script reports errors

### 6.4 Enforcement

Packaging scripts enforce these rules. Skills that fail validation do not package.

Creators MUST self-correct before packaging. The system does not accept justifications for violations.
