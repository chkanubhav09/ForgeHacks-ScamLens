# ScamLens: Pause. Check. Protect.

## Tagline
A browser-local ML second opinion for suspicious messages, with transparent warning evidence and no message uploads.

## Track and prompt
AI + Cybersecurity: 'Build an AI-powered solution that helps people recognize, prevent, verify, or respond to scams, impersonation, and fraud enabled by AI or modern technologies.'

## Problem and users
Unexpected messages can combine urgency, authority, KYC demands, rewards and requests for payment or OTPs. A familiar name or professional wording is not proof of identity. Students, families and everyday mobile users need a way to pause and examine a message without sharing it with another service. ScamLens is an educational triage tool, not a fraud verdict.

## What it does
Paste a message or use a clearly marked synthetic example. ScamLens combines a real locally trained text classifier, separate human-readable warning rules and text-only URL host checks. It shows whether the learned historical spam patterns cross a fixed threshold, which words contributed, what warning cues appeared, and safe verification steps. It never calls a message safe. Short, non-ASCII or low-overlap inputs make the model abstain.

## Technical approach
A reproducible Python pipeline uses UCI historical SMS plus the CC BY 4.0 IMC2025 public smishing artifact. 19,090 unique usable English messages remain after normalization/filtering. Template-opening groups stay in one seeded 60/20/20 partition: 11,434 train, 3,754 validation, 3,902 test. TF-IDF and logistic regression export to JSON for local JavaScript inference. Validation compares models/thresholds and selects 0.80 before the final test. Separate warning heuristics and URL text parsing provide interpretable cues without network calls.

## Validation and limitations
Final mixed-source test: TP 2,710 / FP 4 / TN 908 / FN 280. Accuracy 92.72%, positive recall 90.64%, precision 99.85%, F1 95.02%. Old-design NB trained only on UCI rows in the same clean training split gives 55.79% accuracy and 42.34% recall. Data expansion and model changes are combined, not separately isolated. V1 historical-only metrics are not directly comparable. Benign controls remain old, sources differ, opening grouping is approximate, scores uncalibrated and heuristics not separately benchmarked. This is not representative real-world/Indian scam accuracy, identity verification or AI-generation detection. Thirteen engine tests and real Chrome UI checks pass.

## Impact
The prototype can help a user slow down, separate evidence from claims and independently verify a sensitive request. Local inference avoids uploading potentially private messages and removes the need for paid APIs. Impact has not yet been measured with real users. Future work should start with consented multilingual contemporary scam data, independent evaluation, calibration and careful error analysis, rather than promising perfect detection.

## Build and attribution
The app, model pipeline, interface, tests and documentation were created fresh during ForgeHacks on October 10, 2026 with AI coding assistance. The UCI SMS Spam Collection by Almeida and Hidalgo (2011) and IMC2025 public smishing reports by Agarwal et al. are reused with attribution; no earlier project code was reused. Coding assistance is disclosed separately from the app's learned ML.

## Submission checklist
- Public code repository: https://github.com/chkanubhav09/ForgeHacks-ScamLens (v2 update awaiting verification)
- Demo: public 2-4 minute recording pending from Anubhav
- Screenshots: pending visual verification
- Final entry review and user approval: pending
