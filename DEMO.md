# Recording plan (about 3 minutes)

Use localhost in Chrome/Edge. Start the server first. Wait until 'Check message locally' is enabled. Record your screen and narrate live. Do not paste a real private message. Keep result text readable at normal zoom.

0:00-0:25 - 'I'm Anubhav. ScamLens is for people who receive urgent KYC, prize or family impersonation messages and need a second opinion before clicking or paying. It runs locally in your browser, without uploading the message.'

0:25-1:05 - Click KYC pressure. Point out High caution, sensitive-code/urgency/identity cues, and the actual hostname. 'These are separate warning rules. A bank name in a message does not verify the sender. The links are only parsed, never opened.'

1:05-1:40 - Click Prize SMS. Point at the ML likelihood and positive word evidence. 'This is a real Naive Bayes model trained on a public SMS spam dataset. The number is an uncalibrated spam likelihood, not the probability of fraud. The model and explicit rules provide different evidence.'

1:40-2:05 - Click Everyday message, then Unknown language. 'We do not label a message safe. Unsupported-language and short messages make the model abstain rather than invent confidence.'

2:05-2:35 - Open Model evaluation and limits. 'The normalized-deduplicated held-out set has 1,284 messages: 144 correctly flagged spam, 14 missed spam and no false positives in this sample. Recall is 91.1%. This old English spam benchmark is not evidence of modern scam performance.'

2:35-3:00 - Show the GitHub README and architecture. 'I built the app fresh during ForgeHacks with AI coding assistance. There are no keys or API charges. Next, I would evaluate on consented modern scam examples, add language support and study errors before making stronger claims. The immediate value is pausing and verifying through a known contact.'

Public demo video must be 2-4 minutes and show the actual working app. No video has yet been recorded or submitted.
