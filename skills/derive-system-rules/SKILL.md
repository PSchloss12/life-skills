# Derive System Rules Skill

## Description
This skill helps the agent learn from both mistakes and successes by creating a system of learned rules. When the agent makes a mistake or discovers a valuable success (work-saving shortcut), this skill is used to record the lesson. The first time a lesson occurs, a draft rule is created. The second time the same lesson occurs, the draft rule is promoted to an active rule. The rules are stored in the project's `agent-learned-rules` directory, with separate files for mistakes and successes.

## Location
/home/pjs/Documents/agent-skills/skills/derive-system-rules/SKILL.md

## Instructions
When using this skill, follow these steps:

1. **Read Existing Rules**: 
   - Check if the directory `agent-learned-rules` exists in the current project. If not, create it.
   - Read the file `agent-learned-rules/rules-mistakes.md` (if it exists) to remember the current active mistake rules.
   - Read the file `agent-learned-rules/rules-successes.md` (if it exists) to remember the current active success rules.

2. **Describe the Lesson**:
   - Clearly describe the lesson that was just learned (either a mistake or a success). Include context if necessary.
   - Also, describe what the correct behavior should be or what rule would prevent the mistake or ensure the success.
   - For successes, note that the bar is higher: only record a success if it represents a real work-saving shortcut, not just a note of how we succeeded in the past.

3. **Determine Cause and Type**:
   - Ask: Was this lesson due to an invoked skill or an erroneous prompt?
     - If yes, then note that the skill or prompt needs improvement (this skill does not modify skills or prompts).
     - If no, proceed to step 4.
   - Also specify whether this lesson is a **mistake** or a **success** (work-saving shortcut).

4. **Check for Draft Rule**:
   - If the lesson is a mistake, look in `agent-learned-rules/draft-mistakes.md` for a rule that matches the lesson description.
   - If the lesson is a success, look in `agent-learned-rules/draft-successes.md` for a rule that matches the lesson description.
     - If a matching draft rule is found:
         a. Append the draft rule to the appropriate active rules file (`rules-mistakes.md` or `rules-successes.md`).
         b. Remove the draft rule from the draft file.
     - If no matching draft rule is found:
         a. Append the new rule (describing the lesson and the correction) to the appropriate draft file (`draft-mistakes.md` or `draft-successes.md`).

5. **Reminder**:
   - After updating the rules, remind the agent to read the published rules (`agent-learned-rules/rules-mistakes.md` and `agent-learned-rules/rules-successes.md`) at the start of future tasks.

## Notes
- The skill assumes that the agent will provide the lesson description and correction when invoking the skill.
- The skill does not automatically detect lessons; it is invoked after a lesson has been recognized.
- The comparison for matching draft rules is based on the text description. The agent should strive for consistent descriptions of the same lesson.
- For successes, only record if it is a genuine work-saving shortcut that would save significant time or effort in similar future situations.

## Example (Mistake)
Suppose the agent mistakenly used the flag `--force` when it should have used `--verbose` in a CLI command.
- First mistake: 
    - Description: "Used --force instead of --verbose in the cli command, causing unintended deletion."
    - Correction: "Always use --verbose to check what will be done before using --force, or avoid --force unless absolutely necessary."
    - Since no draft exists, create a draft in `draft-mistakes.md`.
- Second time the same mistake is made:
    - The agent describes the same mistake.
    - The skill finds the draft and promotes it to `rules-mistakes.md`.

## Example (Success)
Suppose the agent spends time researching the best way to configure a Raspberry Pi for a specific task and discovers that using `overlayfs` with a particular set of options yields the best performance, saving hours of troubleshooting.
- First successful discovery (work-saving shortcut):
    - Description: "Found that using overlayfs with `lowerdir=/opt/base,upperdir=/mnt/rw,workdir=/mnt/work` gives optimal performance for our workload, avoiding hours of trial-and-error."
    - Correction/Rules: "Always use this overlayfs configuration when setting up the Pi for this task."
    - Since no draft exists, create a draft in `draft-successes.md`.
- Second time the same configuration is used successfully (and noted as a work-saving shortcut):
    - The agent notes the same successful outcome.
    - The skill promotes the draft to `agent-learned-rules/rules-successes.md`.

## Important
- The rules directory (`agent-learned-rules`) should be in the root of the current project.
- This skill does not modify the agent's skills or prompts; it only creates rules for the agent to follow.
- Successes are only recorded when they represent a real work-saving shortcut, not just a note of past success.