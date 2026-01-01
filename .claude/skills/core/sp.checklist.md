---
name: sp.checklist
description: Validate skill compliance with skill-creator rules. Use when reviewing, finalizing, or packaging skills to ensure structure, content, and governance meet standards.
---

# Skill Checklist

Verify skill compliance using this checklist.

## 1. Folder Structure Check

Verify:
- Skill folder exists at correct path
- SKILL.md file exists
- scripts/ directory contains executables (if present)
- references/ directory contains docs (if present)
- assets/ directory contains output files (if present)
- No extraneous top-level files

## 2. SKILL.md Frontmatter Check

Verify:
- File starts with `---`
- `name` field exists and matches folder name
- `name` uses hyphen-case, lowercase, max 64 chars
- `description` field exists, max 1024 chars
- `description` includes triggers and when-to-use
- Frontmatter ends with `---`
- No additional fields in frontmatter

## 3. SKILL.md Body Check

Verify:
- Body uses imperative/infinitive form
- Content is procedural and directive
- No conversational or marketing tone
- No "When to use this skill" sections
- No examples unless structurally required
- Body under 500 lines

## 4. Bundled Resources Check

Verify:
- scripts/ contains only executable code
- references/ contains only documentation
- assets/ contains only output files
- Resources are used, not decorative
- No duplication between SKILL.md and references

## 5. Progressive Disclosure Check

Verify:
- SKILL.md contains only core workflow
- Detailed content is in references/
- References are linked from SKILL.md
- References are one level deep maximum
- Long references have navigation headers

## 6. Forbidden Files Check

Verify NO files named:
- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- USER_GUIDE.md
- GETTING_STARTED.md
- Any similar documentation files

## 7. Degree of Freedom Check

Verify:
- Low freedom for fragile, error-prone operations
- Medium freedom for configurable patterns
- High freedom for context-dependent decisions
- Freedom level matches task fragility

## 8. Context Efficiency Check

Verify:
- No verbose explanations
- No redundant information
- No "just in case" content
- Each section justifies token cost
- Claude's existing knowledge is not repeated

## 9. Validation Script Check

Run:
```bash
scripts/quick_validate.py <skill-path>
```

Fix any errors before packaging.

## 10. Packaging Check

Run:
```bash
scripts/package_skill.py <skill-path>
```

Verify:
- Validation passes
- .skill file is created
- No missing files

## Output

Generate compliance report:
```markdown
# Skill Compliance: <skill-name>

## Check 1: Folder Structure
[PASS | FAIL]

## Check 2: Frontmatter
[PASS | FAIL]

...

## Summary
- Total checks
- Passed
- Failed
- Result: [COMPLIANT | NON-COMPLIANT]
```

## Triggers

Use this skill when:
- Reviewing skills before packaging
- Validating skills created by other agents
- Ensuring skill quality meets standards
- Pre-commit or pre-merge review
- Troubleshooting skill issues
