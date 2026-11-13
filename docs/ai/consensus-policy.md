# Numeros Vision — Cross-System Consensus Policy
**Document Type:** Algorithmic Policy

## 1. System Family Grouping
To prevent correlation bias (e.g. Parashari Jyotish and BNN sharing planetary affinities), systems are grouped into 6 independent families:
1. `numerology_core`: Lo Shu 3x3 Magic Square
2. `acoustics`: Chaldean Name Sound Frequencies
3. `numerology_comparative`: Cheiro Canon, Pythagorean, Vedic Sankhya
4. `astrology_classical`: Vedic Parashari & KP Sub-Lord
5. `astrology_nadi`: Bhrigu Nandi Nadi
6. `astrology_remedial`: Lal Kitab

## 2. Convergence Statuses
- `convergent`: >= 2 independent families support the same theme in an overlapping time window with no opposing families.
- `partially_convergent`: Supporting families exist, but some systems report neutral or narrower scope.
- `conflicted`: At least one family indicates positive flow while another indicates severe challenge/delay.
- `single_system`: Exactly one family provides data for the theme.
- `insufficient_evidence`: Zero eligible claims exist for the theme.
- `not_comparable`: Claims possess non-overlapping time windows.

## 3. Convergence Ratio
$$\text{convergence\_ratio} = \frac{\text{supporting\_family\_count}}{\text{eligible\_family\_count}}$$
- Returns `null` if eligible family count is 0.
- STRICT INVARIANT: Never displayed to users as a probability of an event or prediction accuracy percentage.
