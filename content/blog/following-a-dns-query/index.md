---
title: Following a DNS query through the stack
description: A layout specimen for technical writing, from the first symptom to a useful next question.
date: 2026-09-12
draft: true
preview: true
format: Lab note
tags: [Kubernetes, DNS, Troubleshooting]
toc: true
---
This is **sample content for the website prototype**. It demonstrates paragraphs, code, lists, tables, and navigation. It does not describe Marvin's production experience or a verified incident.

## Start with a smaller question

“DNS is broken” is a starting point. A more useful question is which lookup failed, where it originated, and what the caller actually observed.

Keep the initial observation separate from the explanation. A timeout and an unexpected answer may point to very different investigations.

> Write down what you observed before deciding what it means.

## Make the observation reproducible

A notebook can begin with a few fields. The following shell example only prints a checklist; it does not inspect a cluster or run a DNS test.

```bash
#!/usr/bin/env bash
set -euo pipefail

fields=(timestamp source query resolver result)
for field in "${fields[@]}"; do
  printf '%-12s %s\n' "$field" '<record observation>'
done
```

Record the actual command and its output alongside these fields. Include enough context for someone else to understand what was measured.

### Keep a short evidence log

| Observation | Still unknown |
| --- | --- |
| An application reports a lookup timeout | Which component introduced the delay |
| A later query succeeds | Whether the same path and cache state were used |
| The symptom follows a change | Whether the change caused the symptom |

The table separates an observation from a conclusion. It is deliberately incomplete: a useful investigation should make the missing evidence visible.

## Decide what to test next

1. Write down one hypothesis.
2. Identify an observation that would contradict it.
3. Choose a test that can distinguish it from another explanation.
4. Record the result, including results that do not support the hypothesis.

A long identifier such as `an-intentionally-long-example-service-name.platform-infrastructure.svc.cluster.local` should wrap in prose. Code keeps its formatting and scrolls within its own block on narrow screens.

## Leave a useful trail

The final note should explain what is known, what remains uncertain, and what the next test would resolve. Not every investigation needs a neat ending to be worth documenting.

---

*End of layout specimen. Real articles will be based on the author's own notes and technical review.*
