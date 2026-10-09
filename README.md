# ScamLens

A second opinion before you tap. Built fresh on October 10, 2026 for ForgeHacks Online 2026, AI + Cybersecurity.

## Run locally (free, no install or API key)

Download this repository as ZIP and extract it, or clone it. In the extracted folder run:

```powershell
py -m http.server 8000 --bind 127.0.0.1
```

Open http://localhost:8000 in your browser. On Linux/macOS use `python3` instead of `py`. Do not open index.html as a file: the browser must fetch the bundled model from the local server.

## What actually works

- Browser-local TF-IDF logistic regression inference from bundled learned parameters.
- Separate transparent rules for urgency, credentials, KYC, money, authority, reward, remote-access and family-impersonation cues.
- Text-only URL parsing: actual host, username disguise, HTTP, shorteners, numeric IPs and punycode clues. Links are never opened or checked online.
- Word contributions, model abstention for short/non-ASCII/low-vocabulary-overlap messages, explicit non-safety verdicts.
- Synthetic examples, clear control, responsive layout and visible benchmark report.
- No backend, cookies, message storage, paid API, analytics, remote fonts or runtime external requests. Initial requests only load local app/model files. After loading, inference works offline while the page remains open. This is not an installed offline PWA.

## Architecture

```
Message -> local tokenizer/TF-IDF -> logistic regression -> score & word evidence
        -> separate warning rules -> caution signals & safe actions
        -> URL parser -> host clues (no network)
All outputs -> cautious triage UI; no 'safe' verdict
```

## Model v2: expanded data, honest evaluation

19,090 unique usable English messages after normalization and deduplication. The sources contain 5,574 UCI rows plus 33,869 IMC2025 rows; only 22,077 English rows with nonempty text/scam labels from IMC are eligible. Non-English rows and one unlabeled report are excluded. Raw totals are NOT independent training examples. Spam and smishing are combined into one positive class, not differentiated.

`pip install -r requirements-training.txt` then `python3 train_v2.py` reproduces training. Runtime remains zero-install, browser only. The new pipeline exports TF-IDF (sublinear counts, L2 normalization) and logistic-regression coefficients to JSON. Browser inference matches Python probabilities within 1.2e-16 on 20 held-out fixtures. Original train.py remains the historical v1 baseline pipeline; running it overwrites model files, so use train_v2.py for the current model.

Splits are group-disjoint by the normalized first eight words (URLs and placeholders normalized): 11,434 training / 3,754 validation / 3,902 test; seeds 42/43. Vocabulary and weights fit training only. Compare logistic regression and NB at seven thresholds on validation; select validation F1 subject to at most 1% benign false-positive rate. Selected threshold 0.80, then evaluate the final test once. Approximate opening-template grouping reduces leakage but cannot guarantee all related campaigns are separate.

| Same new held-out set | UCI-only old-design NB | Expanded TF-IDF logistic |
|---|---:|---:|
| Accuracy | 55.79% | 92.72% |
| Recall (spam/smishing) | 42.34% | 90.64% |
| Precision | 99.92% | 99.85% |
| F1 | 59.48% | 95.02% |
| False positives / 912 benign | 1 | 4 |
| Missed positives / 2,990 | 1,724 | 280 |

The baseline is retrained using only UCI rows in the same NEW training partition, so it does not have access to new validation/test rows. Expanded data and a stronger model change together, so this comparison does not isolate their individual effects. V1's 98.91% accuracy/91.14% recall were on a different historical UCI-only split and cannot be compared directly. More useful data exposes harder cases; a lower headline number can be a more honest benchmark.

**Not a real-world fraud probability or guarantee.** Benign controls remain historical UCI SMS while newer positives come from public user reports. Source/time imbalance can inflate separability. No modern benign control, multilingual benchmark, external Indian validation, campaign-complete grouping or score calibration. The rule layer is separately heuristic and has not been benchmarked. Spam is not the same as fraud. Non-ASCII messages conservatively abstain.

`node test.js`: 13 deterministic engine tests. Chrome UI checks cover examples, abstention, clear, HTML escaping, local-only requests and 320/390px overflow. The app cannot detect whether AI wrote a message.

## Dataset attribution

Almeida, T. & Hidalgo, J. (2011). SMS Spam Collection [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84

Dataset: https://archive.ics.uci.edu/dataset/228/sms%2Bspam%2Bcollection

UCI states CC BY 4.0; the original dataset readme and its attribution/use terms are preserved in DATASET_LICENSE.txt. Raw messages are not included in the repository. The trained parameter file contains word weights, not message records.

### Added source: IMC 2025 public smishing reports

Agarwal, Sharad; Papasavva, Antonis; Suarez-Tangil, Guillermo; Vasek, Marie (2025). *Fishing for Smishing: Understanding SMS Phishing Infrastructure and Strategies by Mining Public User Reports*. ACM IMC. https://doi.org/10.1145/3730567.3764431

Author artifact: https://github.com/reportsmishing/Smishing-Dataset-IMC25 . CC BY 4.0, full license in IMC2025_LICENSE.txt. We filter English/labeled rows, remove placeholders during feature extraction and deduplicate. No raw reports or active links are shipped.

Not used: the 73,470-row Indian mixed synthetic dataset requires sharing contact information/requesting access; the 10,191-row Mendeley expansion is LLM-generated, so adding it would pad volume with synthetic data; Sting9's linked public dump returned not found. We use the maximum useful verified accessible data found in this bounded build, not claim the world's largest dataset.

## Limits and safe use

ScamLens cannot verify a sender, prove fraud or safety, infer whether AI generated a message, scan attachments or check domain reputation. It may miss scams and flag legitimate urgent messages. Non-English and new scam patterns are not validated. Do not paste secrets. The tool is an educational triage prototype, not a bank, legal adviser or security guarantee. Verify money or credential requests through an independently found official contact.

## Build provenance

This application, model training/export code, rule layer, interface, tests and documentation were created during the event, with AI coding assistance. Public research data was reused and attributed. No prior VayuDrishti code or model was reused. The app itself uses actual learned ML, not merely an AI coding tool.

No project-code license has been granted yet; dataset terms remain separate.
