# Exact word separation — Manuscript 1

**Ibrahim Arnous — Embry-Riddle Aeronautical University**

Computational companion to *A Counterexample to Exact Word Separation by Two-State Quantum Finite Automata* (25 November 2026), a research manuscript awaiting independent review.

The exhibited binary words are:

```
u = abbabaabbababa
v = bababaabbabaab
```

Their relative SU(2) trace has a sharp global minimum of 47/64, as proved analytically in the manuscript. This repository contains the supplementary exact symbolic and exhaustive computational certificate, not the main analytical proof.

## Reproduce

Python 3.11 or later is recommended.

```bash
python -m pip install -r requirements.txt
python verify_counterexample.py
```

- `verify_counterexample.py`: symbolic trace identity and exact integer-quaternion checks of trimmed equal-composition pairs through length 14.
- `verification.log`: recorded successful execution.
- `requirements.txt`: pinned NumPy and SymPy dependencies.

The program certifies the reported minimum counterexample length and the four unordered length-14 counterexamples. The manuscript also derives exact three-state real-amplitude separation for the exhibited pair, the optimal equal-prior two-state error, and an infinite family by positive power substitution. The universal three-state question remains open.

## Citation and status

Arnous, Ibrahim (2026). *A Counterexample to Exact Word Separation by Two-State Quantum Finite Automata*. Manuscript 1. Zenodo DOI to be added following deposit.

This is research code accompanying an independently unrefereed manuscript. Publication priority is pending verification. Generative AI (OpenAI ChatGPT) assisted substantively in discovery, proof development, writing and verification code, as disclosed in the manuscript. No license has been selected yet.
