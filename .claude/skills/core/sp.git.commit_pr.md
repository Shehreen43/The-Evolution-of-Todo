---
name: sp.git.commit_pr
description: Automate Git commit and pull request workflow. Use when: (1) User asks to create a pull request, (2) User asks to commit local changes and open a PR, (3) Workflow requires automated commit message generation and PR submission.
---

# Git Commit and PR Skill

Automate creating, reviewing, and submitting Git pull requests.

## Preconditions

Verify:
- Working directory is git repository
- User has permission to commit and create PR
- Branch is clean or changes are staged

## Workflow

### 1. Review Changes

Run:
```bash
git status
git diff --staged
git log --oneline -5
```

Identify:
- Files modified
- Changes staged
- Recent commit history

### 2. Generate Commit Message

Generate commit message following repository standards:
- Use conventional commit format if configured
- Include ticket/reference numbers
- Keep summary under 50 characters
- Add body if needed for context

Present message to user for approval before committing.

### 3. Create Commit

Run:
```bash
git commit -m "<message>"
```

If commit fails, report error and halt.

### 4. Push Branch

Run:
```bash
git push origin <branch-name>
```

### 5. Create Pull Request

If PR does not exist:
- Fetch target branch
- Check for merge conflicts
- Create PR with:
  - Title from commit message
  - Description from commit body or change summary
  - Link to related issues/tickets

### 6. Report Result

Report:
- Commit hash
- PR URL
- Any conflicts or issues requiring attention

## Guardrails

### Do
- Verify repository and branch before starting
- Present commit message for user approval
- Check for conflicts before creating PR
- Report all errors clearly
- Follow repository commit message conventions

### Do Not
- Force push without user approval
- Create PR with unresolved conflicts
- Skip conflict detection
- Commit without presenting message first

### Escalate
- Merge conflicts require resolution
- Permission denied errors
- Branch protection rules block push
- PR template missing required fields

## Outputs

- Committed changes
- Created pull request with URL
- Status report with any issues

## Triggers

Use this skill when:
- User says "create a pull request"
- User says "commit my changes and open a PR"
- User asks to "submit this for review"
- Workflow reaches commit phase
