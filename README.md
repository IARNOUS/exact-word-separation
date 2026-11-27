# Exact word separation

Ibrahim Arnous  
Embry-Riddle Aeronautical University, Daytona Beach, Florida, USA

Code accompanying the manuscript *A Counterexample to Exact Word Separation by Two-State Quantum Finite Automata* (November 2026).

The counterexample is the pair

```
u = abbabaabbababa
v = bababaabbabaab
```

The manuscript proves that the minimum relative trace over SU(2) is 47/64. The proof is analytical and does not rely on the code in this repository. The code verifies the trace identity and checks the minimality and classification of the length-14 counterexamples.

## Running the code

Tested with Python 3.13.5, NumPy 2.3.5 and SymPy 1.14.0. Use the pinned dependencies in `requirements.txt`.

```bash
python -m pip install -r requirements.txt
python verify_counterexample.py
```

- `verify_counterexample.py`: symbolic and exact integer-arithmetic verification.
- `verification.log`: recorded verification results.
- `requirements.txt`: Python dependencies.

## Citation

I. Arnous, *A Counterexample to Exact Word Separation by Two-State Quantum Finite Automata*, preprint, November 2026. [https://doi.org/10.5281/zenodo.24601703](https://doi.org/10.5281/zenodo.24601703).

## License

The verification software is available under the MIT license (see `LICENSE`).

## Disclosure and reproducibility

Generative AI was used to assist with the development and checking of computational code, mathematical exposition, and preparation of the manuscript in LaTeX. The authors are responsible for the mathematical arguments, results, and conclusions presented herein. This manuscript is a draft circulated for expert feedback and has not been peer reviewed.
