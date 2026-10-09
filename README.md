# ScamLens

A second opinion before you tap. Built fresh on October 10, 2026 for ForgeHacks Online 2026, AI + Cybersecurity.

## Run locally (free, no install or API key)

Download this repository as ZIP and extract it, or clone it. In the extracted folder run:

```powershell
py -m http.server 8000 --bind 127.0.0.1
```

Open http://localhost:8000 in your browser. On Linux/macOS use `python3` instead of `py`. Do not open index.html as a file: the browser must fetch the bundled model from the local server.

## What actually works

- Browser-local multinomial Naive Bayes inference from bundled learned parameters.
- Separate transparent rules for urgency, credentials, KYC, money, authority, reward, remote-access and family-impersonation cues.
- Text-only URL parsing: actual host, username disguise, HTTP, shorteners, numeric IPs and punycode clues. Links are never opened or checked online.
- Word contributions, model abstention for short/non-ASCII/low-vocabulary-overlap messages, explicit non-safety verdicts.
- Synthetic examples, clear control, responsive layout and visible benchmark report.
- No backend, cookies, message storage, paid API, analytics, remote fonts or runtime external requests. Initial requests only load local app/model files. After loading, inference works offline while the page remains open. This is not an installed offline PWA.

## Architecture

```
Message -> local tokenizer -> learned Naive Bayes -> spam score & word evidence
        -> separate warning rules -> caution signals & safe actions
        -> URL parser -> host clues (no network)
All outputs -> cautious triage UI; no 'safe' verdict
```

## Model and reproducibility

`python3 train.py` downloads the UCI source, deduplicates normalized message text, stratifies a 75/25 split with seed 42, trains Laplace-smoothed multinomial Naive Bayes, and exports model.json and metrics.json. Standard library only. Threshold 0.90 was set before evaluation. Test data is excluded from fitting. The bundled evaluation has 3,846 training messages and 1,284 test messages: TP 144, FP 0, TN 1,126, FN 14. Spam precision 100% on this sample, recall 91.14%, F1 95.36%. **Not a scam-detection accuracy claim.** Zero false positives in this sample does not promise zero false positives in use. Scores are uncalibrated; model word evidence describes spam tendencies, not causal proof of fraud.

`node test.js` runs 13 deterministic engine tests. Node is only needed for development tests, not to run the app. The benchmark is historical English SMS spam, not a contemporary scam benchmark. Exact normalized duplicates are removed before splitting; related templates may remain across the split. Non-ASCII messages abstain conservatively, including English containing smart punctuation. Rule cues are heuristic and unvalidated on a representative scam dataset.

## Dataset attribution

Almeida, T. & Hidalgo, J. (2011). SMS Spam Collection [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84

Dataset: https://archive.ics.uci.edu/dataset/228/sms%2Bspam%2Bcollection

UCI states CC BY 4.0; the original dataset readme and its attribution/use terms are preserved in DATASET_LICENSE.txt. Raw messages are not included in the repository. The trained parameter file contains word weights, not message records.

## Limits and safe use

ScamLens cannot verify a sender, prove fraud or safety, infer whether AI generated a message, scan attachments or check domain reputation. It may miss scams and flag legitimate urgent messages. Non-English and new scam patterns are not validated. Do not paste secrets. The tool is an educational triage prototype, not a bank, legal adviser or security guarantee. Verify money or credential requests through an independently found official contact.

## Build provenance

This application, model training/export code, rule layer, interface, tests and documentation were created during the event, with AI coding assistance. Public research data was reused and attributed. No prior VayuDrishti code or model was reused. The app itself uses actual learned ML, not merely an AI coding tool.

No project-code license has been granted yet; dataset terms remain separate.
