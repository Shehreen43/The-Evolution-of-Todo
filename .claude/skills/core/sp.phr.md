---
name: sp.phr
description: Apply Problem-Hypothesis-Resolution reasoning. Use when analyzing issues, debugging, making decisions, or solving problems systematically.
---

# PHR Reasoning Skill

Apply structured Problem-Hypothesis-Resolution reasoning.

## PHR Structure

### Problem Statement
Define the problem precisely:
- What is happening?
- Where is it happening?
- When does it occur?
- Who is affected?
- What is the expected behavior?

Write problem statements that are observable and bounded.

### Hypothesis Formation
Form testable hypotheses:
- Single cause per hypothesis
- Can be proven or disproven
- Based on available evidence
- Prioritized by likelihood

Avoid compound hypotheses. Test one variable at a time.

### Resolution Selection
Select and execute resolution:
- Test highest-probability hypothesis first
- Validate hypothesis before implementing fix
- Measure outcome against expected behavior
- Iterate if resolution fails

## PHR Workflow

### 1. Frame Problem

Gather evidence:
- Observe symptoms
- Collect error messages
- Identify affected components
- Determine scope of impact

Write problem statement without assuming cause.

### 2. Generate Hypotheses

For each possible cause:
- State the hypothesis clearly
- Identify how to test it
- Estimate probability based on evidence

Prioritize hypotheses by:
- Likelihood of cause
- Ease of testing
- Impact if true

### 3. Test Hypothesis

Execute test:
- Isolate the variable
- Run controlled check
- Observe result
- Confirm or reject hypothesis

### 4. Implement Resolution

If hypothesis is confirmed:
- Implement fix
- Verify fix resolves problem
- Check for side effects
- Document solution

If hypothesis is rejected:
- Move to next hypothesis
- Repeat until resolution found

### 5. Document Outcome

Record:
- Original problem statement
- Root cause identified
- Resolution applied
- Verification result

## Guardrails

### Do
- State problems precisely without assuming causes
- Test one hypothesis at a time
- Validate hypotheses before fixing
- Document root causes
- Verify resolutions completely

### Do Not
- Skip problem framing
- Test multiple hypotheses simultaneously
- Assume cause without evidence
- Implement untested fixes
- Close issues without verification

### Defer
- Long-term improvements
- Refactoring unrelated to problem
- Feature requests
- Documentation updates

## Triggers

Use this skill when:
- User reports an issue or bug
- User asks "why is this happening?"
- Debugging or troubleshooting
- Making decisions with uncertainty
- Investigating failures or errors
