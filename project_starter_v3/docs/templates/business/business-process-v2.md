# Business Process

Understand the business before understanding the system.

## Business Goal
What is the purpose of this business process?

## Process Overview
Describe high-level business workflows.

Focus on:

- Major business stages
- Process sequence
- Process ownership

Do not describe:

- Detailed execution steps
- Validation logic
- System behavior
- Database actions

Format:
- Start -> Step -> Step -> End

## Process Steps
Step Name:
Owner:
Input:
Action:
Output:
Next Step:

## Decision Points
Decision:
Decision Maker:
Input:
Possible Outcomes:
Next Process:

For decisions with multiple branches or non-trivial logic,
diagram it instead of using the table above:

```
Trigger
↓
Validation
↓
Decision?
├─ Yes → Action A
└─ No  → Action B
```

## Exceptions
Exception:
Cause:
Handling Method:
Responsible Role:

## Pain Points
Current Problem:
Impact:
Current Workaround:

## Future Improvement Ideas
Improvement:
Expected Benefit:
