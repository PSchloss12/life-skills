---
name: build-manual
description: Turns a buildable object or multi-step task into a complete, LEGO-style visual instruction manual one action per step, the new part highlighted, a finished-result promise up front. Analyzes the task, researches steps and parts that aren't already known, plans the build sequence, then sources real photos from the web or generates step imagery when an image model is available. Use when the user asks for a visual guide, step-by-step manual, instruction booklet, assembly or install guide with pictures, or a how-to manual for any process.
---

# Build-Manual Creator

Turn any buildable object or multi-step task into a complete, easy-to-follow instruction manual in the LEGO tradition: wordless where possible, one clear action per step, the new part always highlighted, and a finished-result promise up front. This skill is the orchestrator — it does the thinking (analysis, research, sequencing, layout) and then, for each panel, finds or creates the best image: an accurate photo sourced from the web, an image produced with whatever image-generation tools are available, or a sourced photo with an overlay arrow. No specific image skill or subagent is required.

## Image sourcing policy (read this first)

Real photos beat vector art, always. Per step, in priority order:

1. **A perfect photo exists** — an accurate image of the exact part, location, or action, found online. Use it.
2. **Image generation is available** — use downloaded real photos as visual reference to generate the step's unique image (the action, the connection, the exact model combination).
3. **No generation available** — find existing photos of the parts involved and overlay an arrow pointing to where each goes. Never draw artwork from scratch by hand.

Detect image generation by checking the environment for known provider keys (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `REPLICATE_API_TOKEN`, `STABILITY_API_KEY`, `FAL_KEY`). If a generation attempt fails at runtime, fall back to rule 3.

**Abort rule:** if a step depends on recognizing a part, location, or connection — and no photo can be found and none can be generated — abort the run and tell the user exactly which parts or processes had no imagery. Never ship a manual with blind steps. (Purely textual steps like "wait 30 seconds" don't need images.)

## Why planning comes first

A good manual is two different jobs. Deciding what the steps are and in what order is reasoning; producing each step's image consistently is rendering. Settle the whole sequence, parts inventory, and visual style up front so every panel — however it is sourced — reads as one coherent manual.

## The LEGO principles you must honor

Read [references/lego-principles.md](references/lego-principles.md) for the full treatment. The essentials, adapted for real-photo panels:

1. **One clear action per step.** A reader should never wonder "what changed?" Small, incremental steps beat a few dense ones. When in doubt, split a step.
2. **Highlight what's new.** On generated images: full saturation for new parts, muted for the existing build. On real photos: a bold overlay marker (arrow, circle) on the part or spot that changes this step. This is the single most important LEGO technique.
3. **Constant viewpoint.** Keep one angle as long as sources allow — prefer photos matching the manual's dominant angle. Show an explicit flip/rotate callout when orientation genuinely changes.
4. **Show, don't tell.** Pictures, arrows, and symbols carry the meaning. Text only for step numbers, quantities, dimensions, and short captions where a photo can't disambiguate.
5. **Finished result first.** Panel 0 shows the completed outcome — the goal the reader works toward.
6. **Sequence for early success.** Order steps so a big, satisfying chunk comes together early; build outward from a stable base; never attach to a part that isn't there yet.
7. **Parts call-out per step.** Each panel shows a parts tag: which parts and how many (×N), like LEGO's per-step parts box.
8. **Sub-assemblies as callouts.** A piece needing its own 2–3 steps gets a boxed callout section, then drops into the main sequence as one finished unit.
9. **No hands or human figures.** Prefer hand-free photos when selecting; convey action with arrows and overlay markers, never clutter.
10. **Error prevention.** Where a mistake is likely (part fits two ways, wrong slot, reversed connector), add a correct/✗-wrong pair or a ⚠ callout rather than trusting the reader to infer it.

## Workflow

### 1. Analyze the task
Establish before anything is drawn:
- What is being built/done — the end object or outcome.
- The specific products/models involved (e.g., "Viofo hardwire kit" + "Kia K4 2025"); research unknowns before proceeding.
- Ask the user which output format they want: **image** (single composite PNG), **PDF**, or **HTML**.
- State assumptions and required tools in the manual's intro.

### 2. Research
- List what you don't already know: steps, part names and counts, safety-critical specs.
- Research via web search: official manuals and manufacturer documentation first, then videos, then reputable guides.
- Corroborate safety-critical facts (fuse ratings, torque specs, wiring polarity) against manufacturer/vehicle documentation specifically; flag anything secondhand as "verify".
- On conflicting instructions: the official source wins; label any conflict you cannot resolve inline. Stop when the step list is coherent and no conflicts remain.

### 3. Plan the manual
- Full ordered step list, one action per step.
- Parts inventory with counts — feeds the front-of-manual inventory and every per-step parts tag.
- For each step, decide the image strategy: perfect photo / generate / part-photo + arrow.
- Promote sub-assemblies to callout sections.

### 4. Gather & make images
- Create the run folder `build-manual/<slug>/` (kebab-case task name) under the current working directory; save every fetched image to `build-manual/<slug>/assets/`.
- Download images; credit the source domain in a small caption. Quality gate: shows the right part/model, ≥400px, no heavy watermark.
- **Validate every download**: confirm each file is actually an image (magic bytes/`file` type), not an HTML error page served as `.png`/`.jpg`. Delete and re-source failures before proceeding — an unvalidated download is a blind step.
- Generate missing or action imagery using the downloaded photos as reference.
- Apply overlays (arrows, circles, ✗) as positioned SVG/HTML elements, or with Pillow when compositing to a single image.
- **No number overlays on images** — step numbers belong on the panel or caption beside the photo, never burned onto the image itself.
- **Off-model photos**: when a sourced photo doesn't show the exact model being worked on (e.g., a generic fuse box instead of the 2025 Kia K4's), add a small note in the corner that it may differ from the parts being used.

### 5. Produce the manual
Assembly order — the LEGO booklet:
1. Cover / finished-result panel — the promise.
2. Parts inventory — every part with its quantity.
3. Numbered step panels — the number sits on the panel/caption, not on the image; one action each, new part highlighted, parts tag, arrows for motion, ⚠/✗ where needed.
4. Optional repeated finished thumbnail for orientation.

Format specifics — the deliverable always lives in the run folder, never the cwd:
- **HTML**: write to `build-manual/<slug>/manual.html` (follow the `html` skill for conventions), using relative `assets/` paths.
- **PDF**: follow the `pdf` skill.
- **Image**: composite all panels vertically into one tall PNG (Pillow/matplotlib).

### 6. Verify & deliver
- QA pass: every step is exactly one action plus an image (or an explicit note for non-visual steps); per-step parts tags present; source credits present; no unresolved research conflicts; the sound-off test — could someone follow this from the pictures alone?
- **Link check**: every `src` in the final HTML resolves to an existing, validated image file in `assets/`. A manual that reports success while referencing missing or fake images is a failed run.
- Deliver: report the file path, step count, and image coverage (e.g., "14 photos sourced, 2 generated").
