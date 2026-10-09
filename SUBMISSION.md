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
A reproducible Python standard-library training pipeline uses the attributed UCI SMS Spam Collection. Normalized-text duplicates are removed before a stratified 75/25 split with seed 42. Laplace-smoothed multinomial Naive Bayes parameters are exported to JSON and evaluated in JavaScript inside the browser. A separate heuristic layer checks urgency, credentials, identity, payments, claimed authority, rewards, remote access and family impersonation. A URL parser extracts the true hostname and selected syntax warnings without visiting the link. HTML/CSS/JavaScript are enough to run the interface; no model API, cloud backend or secret key is required.

## Validation and limitations
The held-out historical English SMS-spam set contains 1,284 messages: TP 144, FP 0, TN 1,126, FN 14. Spam recall is 91.14%, precision 100% in this sample and F1 95.36%. This is not modern scam-detection accuracy, sender verification or AI-generation detection. Scores are uncalibrated. Similar message templates may still cross the split. The warning rules have not been benchmarked on a representative scam set. Non-English support is intentionally not claimed. Thirteen deterministic engine tests cover caution cues, abstention, length limits and URL parsing.

## Impact
The prototype can help a user slow down, separate evidence from claims and independently verify a sensitive request. Local inference avoids uploading potentially private messages and removes the need for paid APIs. Impact has not yet been measured with real users. Future work should start with consented multilingual contemporary scam data, independent evaluation, calibration and careful error analysis, rather than promising perfect detection.

## Build and attribution
The app, model pipeline, interface, tests and documentation were created fresh during ForgeHacks on October 10, 2026 with AI coding assistance. The UCI SMS Spam Collection by Almeida and Hidalgo (2011) is reused with attribution; no earlier project code was reused. Coding assistance is disclosed separately from the app's learned ML.

## Submission checklist
- Public code repository: pending verified upload
- Demo: public 2-4 minute recording pending from Anubhav
- Screenshots: pending visual verification
- Final entry review and user approval: pending
