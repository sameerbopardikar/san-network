---
type: research-report
title: >-
  Are Current Multimodal Video Models Good Enough for Boxing/MMA Technique
  Analysis?
date: '2026-08-04T00:00:00.000Z'
goal: goals/aneek-fighter-development
status: complete
subject: combat-sport video analysis
visibility: private
captured_at: '2026-08-04T22:56:01.147Z'
captured_via: capture-cli
evidence_cutoff: '2026-08-04T00:00:00.000Z'
research_method: >-
  delegated evidence review using official documentation, primary papers, arXiv
  API, and direct URL verification
ingested_via: put_page
ingested_at: '2026-08-04T22:56:12.002Z'
source_kind: put_page
---

# Are current multimodal video models good enough for boxing/MMA technique analysis?

**Evidence cutoff / access date:** 2026-08-04
**Scope:** ordinary sparring video, not instrumented lab motion capture. “Validated” below means demonstrated on a relevant held-out task with ground truth; it does **not** mean that a vendor demo looked plausible.

## Verdict

**Qualified yes for review assistance; no for autonomous coaching or biomechanics.** Current models can usefully **index rounds, propose coarse events, retrieve candidate timestamps, summarize obvious tactical tendencies, and flag a small set of pre-specified visible errors for human review**. This is meaningful if the output is evidence-linked and allowed to abstain. They are **not validated to reliably diagnose fine boxing/MMA mechanics from unconstrained sparring**, and they cannot defensibly infer punch force, impact severity, precise 3-D biomechanics, or skill progression from ordinary monocular video.

The strongest general model family for native video ingestion is Gemini, but its default processing is a poor match to fighting: **1 frame/s**, while punches and defensive reactions unfold over tens to hundreds of milliseconds. Google explicitly warns that fast action can lose detail. Raising FPS and clipping dense windows helps, but does not create missing 3-D geometry, remove occlusion, or turn a general VLM into a combat-validated measurement instrument.

The evidence supports a **hybrid pipeline**: high-frame-rate capture + deterministic clipping/tracking/pose + a domain rubric + a frontier VLM as an evidence-linked candidate generator + human adjudication. It does not support “upload a round and trust the coaching report.”

## What the general models actually ingest

| System (current as of cutoff) | Official input reality | Independent evidence relevant to temporal reliability | Interpretation for sparring |
|---|---|---|---|
| **Gemini 3.6 Flash** (stable; model page updated **July 2026**), **Gemini 3.5 Flash** (May 2026), **Gemini 3.1 Pro Preview** (Feb 2026) | Native video/audio; 1,048,576 input tokens. Google’s API guide says File API video is stored at **1 FPS**, timestamped each second; about **258 visual tokens/frame + 32 audio tokens/s** at default resolution (about 300 tokens/s). Current cloud docs allow `videoMetadata.startOffset`, `endOffset`, and custom `fps`; default remains 1 FPS. Gemini 3 video defaults to **70 tokens/frame**, high is **280**. Approx. max with audio 45 min / without audio 1 h, up to 10 videos. | Current 3.6 was released after the cited independent tests. On **Video-MME-v2** (Apr 2026 preprint), **Gemini-3-Pro** scored **49.4** group-consistent nonlinear score vs **90.7** human experts; Gemini-3-Flash 42.5. Average accuracy for 3-Pro was 66.1%, illustrating how per-question accuracy overstates consistency. On **PushupBench** (Apr 2026 preprint, 5 FPS, max 112 frames), Gemini 3 Flash reached only **42.1% exact counting**, 3 Pro 39.8%. | Best native-video starting point, but not a combat technique validator. Use high-FPS short clips, not whole-round default ingestion. Current 3.6 must be tested rather than assumed superior on this task. |
| **OpenAI GPT-5.6 Sol** (current page; 1.05M context, Feb 16 2026 knowledge cutoff) | Official model page: **text + image input; video not supported**. Video must be converted to frame bursts/contact sheets or handled by an external pipeline. Official vision limitations include precise spatial localization, approximate counting, and possible incorrect descriptions. | **GPT-5** in Video-MME-v2 was evaluated with only 50 frames: nonlinear score **37.0** with subtitle/audio-derived text and 26.4 visual-only. PushupBench exact count **10.9%**. These are not GPT-5.6 results. | Useful as a second-reader on selected frames and structured evidence, not a native-video baseline. Frame selection can dominate results. |
| **Claude Opus 5 / Sonnet 5** (current model IDs; 1M context) | Anthropic vision docs support image inputs; animated images are unsupported and **only the first frame is used**. No native video-analysis endpoint was documented. Frames must be extracted externally. | PushupBench tested older **Claude Opus 4.5 / Sonnet 4.5** at max 100 frames: only **4.9% / 9.5%** exact counting. Not evidence about version 5, but it shows that strong image-language reasoning did not imply temporal counting. | Secondary reviewer only; no evidence that current Claude solves combat temporal perception. |
| **Qwen video-VLs** | Official **Qwen2.5-VL** description reports dynamic-FPS training, absolute time encoding, >1-hour video, and second-level event localization. Open systems permit explicit frame sampling and adaptation. | Video-MME-v2: Qwen2.5-VL-72B-Instruct **22.1** nonlinear at 64 frames. **Qwen3.5-397B-A17B-Think** reached **39.1** with 512 frames, the best open model in that paper, still far below human. | Attractive for privacy/local adaptation and dense-frame experiments, but requires domain validation; more frames and “thinking” are not guarantees of visually grounded reasoning. |

**Primary official ingestion sources**

- Google Gemini video guide (last updated 2026-07-30): https://ai.google.dev/gemini-api/docs/video-understanding
- Google current video customization / tokenization: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/video-understanding
- Google `VideoMetadata` schema (`startOffset`, `endOffset`, `fps`): https://ai.google.dev/api/generate-content#VideoMetadata
- Gemini 3.6 Flash model page: https://ai.google.dev/gemini-api/docs/models/gemini-3.6-flash
- Gemini 3.1 Pro Preview: https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview
- GPT-5.6 Sol model page: https://developers.openai.com/api/docs/models/gpt-5.6-sol
- OpenAI vision limitations: https://developers.openai.com/api/docs/guides/images-vision
- Anthropic vision (first-frame-only animation behavior): https://platform.claude.com/docs/en/build-with-claude/vision
- Anthropic current models: https://platform.claude.com/docs/en/about-claude/models/overview
- Qwen2.5-VL official release: https://qwenlm.github.io/blog/qwen2.5-vl/

## Evidence by requested capability

| Capability | Evidence-weighted status | What is defensible now |
|---|---|---|
| **Coarse event recognition** (exchange begins, jab-like punch, kick attempt, clinch, takedown attempt, knockdown) | **Validated in adjacent tasks; plausible-to-good in clean sparring; not boxing-validated for frontier VLMs.** Generic video benchmarks establish action/event recognition, but fine combat labels and occlusion are harder. BoxingVI (Nov 2025 preprint) supplies 6,915 manually segmented clips from only 20 YouTube sessions / 18 athletes and six punch classes; it is a dataset paper, not proof of robust deployment. | Generate candidate events with timestamps, then verify. A domain detector trained on local labels should beat free-form prompting once enough data exists. |
| **Tactical pattern analysis** (straight-line retreats, repeated reactions, entry-after-feint, predictable exits) | **Plausible, not validated.** It composes event detection, identity tracking, geometry, and temporal aggregation—the very hierarchy where Video-MME-v2 shows cascading errors. Audio/subtitles materially inflated some benchmark results, which sparring often lacks. | Restrict to a predeclared taxonomy; require timestamped examples and counterexamples; report counts/rates with uncertainty; coach confirms. Do not accept narrative-only “tendencies.” |
| **Form-error candidate detection** (crossing feet, guard not returning, visible balance loss, head static after body shot) | **Plausible only for visible, operationalized errors in short dense clips.** Sports Action Quality Assessment (AQA) works when trained on sport-specific, procedure-annotated data. FineDiving has 3,000 clips with official scores and step boundaries; it does not demonstrate cross-sport transfer to boxing. | Binary candidate flags with exact evidence frames, visibility/confidence, and an abstention state. A human decides whether it is actually an error in context. |
| **Quantitative biomechanics** (joint angles, velocities, COM, 3-D rotation) | **No-go from a general VLM; limited with specialized CV.** AthletePose3D (Mar 2025) found conventional monocular 3-D models poor on high-acceleration sport; sport fine-tuning reduced MPJPE from **234 mm to 98 mm**, while velocity estimates remained limited. AthleticsPose (Jul 2025) likewise found camera-view/scale sensitivity and failure on higher-speed knee-drive velocity. | 2-D/relative kinematics may be useful under fixed cameras after local validation. Credible 3-D requires calibrated multi-view capture and sport/domain adaptation. Do not report centimeter/degree precision without a reference system. |
| **Force/contact estimation** | **Contact occurrence: plausible candidate detection. Force magnitude / damage: no-go.** Video does not uniquely determine glove acceleration, effective mass, tissue compliance, bracing, or hidden contact geometry. Video-to-force papers estimate **ground-reaction force** only after training on synchronized force plates and narrow movements—not fist impact. | Detect “possible contact” and manually score contact class. Never output Newtons, “power,” damage, concussion risk, or impact severity from ordinary video. Use instrumented bags/gloves or force sensors for force questions. |
| **Skill-state progression** | **Not validated as autonomous scoring.** Longitudinal tracking is plausible only after reliable component measurements exist. AQA correlations on fixed judged sports do not establish sensitivity to boxing learning or resistance/fatigue transfer. | Maintain a human-governed state: introduced → clean isolated drill → reaction drill → constrained sparring → retained under fatigue/contact. Video supplies evidence clips; it does not promote states by itself. |

## Why specialized CV is still necessary

- **Precise event spotting can work when the task is supervised and narrow.** T-DEED (2024) reached **73.23 mAP at ±1 frame** and 88.88 at ±2 frames on four FineDiving event classes (25–30 FPS). This validates the architecture/task pattern, not transfer to punches or sparring.
- **Combat pose needs multi-view and physics constraints.** “Multi-person Physics-based Pose Estimation for Combat Sports” (Apr 2025 preprint) uses calibrated sparse multi-camera footage, epipolar constraints, triangulation, identity tracking, kinematic smoothing, and physics optimization on elite boxing. The paper explicitly says monocular methods lack precision/robustness under rapid motion and occlusion. Its physics layer enforces plausibility/collision avoidance; that is not measured punch force.
- **Sports-specific training data matters.** AthletePose3D’s large error reduction after sports fine-tuning and BoxingVI’s small, narrow corpus both imply that general-purpose pose/action models should not be trusted out of domain.

**Primary research URLs**

- Video-MME-v2 (preprint, 2026-04-06): https://arxiv.org/abs/2604.05015
- PushupBench (preprint, 2026-04-25): https://arxiv.org/abs/2604.23407
- TempCompass (2024; temporally conflicting videos): https://arxiv.org/abs/2403.00476
- TimeLens / refined temporal-grounding benchmarks (preprint, 2025-12-16): https://arxiv.org/abs/2512.14698
- OmniVCHall compositional video hallucination benchmark (preprint, 2026-01-31): https://arxiv.org/abs/2602.00559
- FineDiving (CVPR 2022): https://arxiv.org/abs/2204.03646 and https://github.com/xujinglin/FineDiving
- T-DEED precise sports event spotting (2024): https://arxiv.org/abs/2404.05392
- AthletePose3D (preprint, 2025-03-10): https://arxiv.org/abs/2503.07499
- AthleticsPose (preprint, 2025-07-17): https://arxiv.org/abs/2507.12905
- Combat-sports multi-person 3-D pose (preprint, 2025-04-11): https://arxiv.org/abs/2504.08175
- BoxingVI dataset (preprint, 2025-11-20): https://arxiv.org/abs/2511.16524
- Video-to-ground-reaction-force with synchronized force plates (ACM MM 2022): https://arxiv.org/abs/2207.05845

## Benchmark caveats that materially affect the verdict

1. **Most video-VLM benchmarks are multiple-choice QA, not coaching.** Correctly choosing an option does not validate precise localization, causal mechanics, or useful correction.
2. **Per-question accuracy can hide inconsistency.** Video-MME-v2’s best model had 66.1% average accuracy but only 49.4 on its grouped nonlinear consistency score.
3. **Inputs differ across models.** Video-MME-v2 used native/recommended 1 FPS for some commercial systems, 50 frames for GPT-5, 64 or 512 frames for open models, and sometimes subtitles/raw audio. This is not a controlled architecture comparison.
4. **Model versions move faster than independent evaluation.** Gemini 3.6, GPT-5.6, and Claude 5 are newer than several cited tests. Absence of a benchmark result is uncertainty, not evidence of failure—or success.
5. **Sports AQA is highly domain-bound.** Diving/figure-skating clips have known procedures, broadcast views, official scores, and repeated backgrounds. Sparring has two interacting bodies, occlusion, variable tactics, no single canonical “correct” action, and context-dependent coaching judgments.
6. **Pose metrics do not automatically validate derived biomechanics.** Low joint-position error can coexist with biased velocity, unstable depth, and camera-dependent angles.
7. **Hallucination is not solved by prompting.** OmniVCHall evaluated 39 models and found accuracy drops of roughly 5.7–9.3 points on compositional versus single-factor questions; Video-MME-v2 found “thinking” could worsen visual-only performance.

## Minimum experimentally defensible Aneek/Sameer pipeline

### Capture

1. Record **two fixed, synchronized views** at **1080p/60 FPS** (prefer 120 FPS if bright enough), one broad side/diagonal and one approximately orthogonal. Keep full bodies and floor visible; no digital zoom or moving camera.
2. Use a clap/flash for synchronization, a visible 1 m scale or measured floor markers, locked exposure/focus, and bright lighting to reduce motion blur. Preserve original files and timestamps.
3. Record drill label, round constraints, contact ceiling, fatigue state, and which fighter is Aneek. These are necessary context, not optional metadata.

### Processing

1. **Do not send only the whole round at Gemini’s default 1 FPS.** Run coarse segmentation/event proposals over the round, then create 2–4 s windows around each candidate from the original 60 FPS footage.
2. For each window, retain: both views, 8–10 FPS VLM sample, original-FPS burst, tracked fighter IDs, 2-D pose/keypoint confidence, optical flow, and visibility/occlusion flags. Dense original frames remain available for human review.
3. Ask Gemini 3.6 Flash and one independent frame-based model (GPT-5.6 or Claude 5) to fill a **fixed JSON rubric**, not write a free-form coaching essay: event type; start/end; fighter; visible evidence; candidate error; counterevidence; visibility; confidence; abstain reason.
4. Calculate counts and tactical chains deterministically from accepted events. Let the VLM explain **accepted structured evidence**, not invent the event ledger.
5. Coach adjudicates every correction. Only adjudicated observations may update Aneek’s state-of-fighter; preserve model proposal versus coach observation as separate evidence classes.

### Pilot design

Create a frozen gold set before looking at model outputs:

- **60 short clips** sampled across cooperative drills, constrained sparring, and freer technical sparring; at least **300 candidate actions**.
- Predeclare 6–8 observable labels, e.g. jab/cross/hook, slip/guard, straight retreat, angle exit, stance cross, visible balance loss, possible contact, clinch/takedown attempt. Avoid internal states (“hesitant”) and force claims.
- Sameer plus one independent qualified combat-sports reviewer annotate event boundaries, fighter identity, visibility, and candidate errors. Resolve disagreements after measuring them. If inter-rater **Cohen’s κ < 0.70** on an error label, that label is not stable enough to evaluate a model.
- Blind the reviewers to model identity; evaluate current Gemini 3.6, a 1-FPS ablation, a high-FPS clipped condition, and one frame-based competitor. Include 20% negative/near-miss clips and repeat 10% of prompts to test consistency.

### Go / no-go thresholds

**Go for candidate-assist only** if all applicable gates pass on held-out clips:

- Coarse event detection: **precision ≥ 0.90, recall ≥ 0.80**, boundary within **±0.25 s**.
- Fighter identity: **≥ 0.98** correct with **<1% identity swaps**.
- Form-error candidate flags: **precision ≥ 0.80**, recall ≥ 0.60, evaluated only where both human raters mark the feature visible.
- Tactical claims: **≥ 0.85 timestamp-evidence precision** and **≥ 0.75 expert agreement** on predeclared pattern labels.
- Unsupported/hallucinated factual claims: **≤ 5%** claim-level; when evidence is occluded/insufficient, correct abstention **≥ 0.90**.
- Repeatability: identical-input label agreement **κ ≥ 0.80**.
- High-FPS clipped processing must materially outperform the 1-FPS condition (predeclare **≥5 percentage-point F1 gain**) to justify cost/complexity.

**No-go / redesign** if any safety-critical gate fails, if gains disappear on a different session/camera placement, or if performance depends on coach hints embedded in prompts. Even if the pilot passes, remain **no-go** for autonomous correction, numeric biomechanics, punch/contact force, injury/concussion inference, or automatic promotion of skill state.

### Progression pilot (later, separate)

Only after event/error reliability passes: run the same constrained drill battery on three dates. A progression metric should be accepted only if it has **ICC ≥ 0.80** test–retest reliability on unchanged clips, **Spearman ρ ≥ 0.70** with blinded human ratings, and detects predeclared improvement without a rising false-positive rate on unchanged controls. Until then, video is evidence for human state updates, not a skill score.

## Bottom line for Aneek/Sameer

Start the pilot: the technology is good enough to test as a **review accelerator** and evidence organizer. Do not buy the premise that a frontier VLM is already a reliable boxing/MMA technique analyst. The defensible product is “find and structure moments a coach should inspect,” not “replace the coach,” and the most valuable engineering work is likely capture quality, a local combat rubric, dense temporal windows, and a small adjudicated Aneek/Sameer dataset—not a longer prompt.
