# Data Dictionary

This file summarizes the main datasets currently included in the repository. It is intended as a compact orientation file, not a complete variable-level codebook.

## `00_data/processed/01_Panas.xlsx`

Session-level affect questionnaire data based on PANAS items.

Key columns include:

- `Participant`: pseudonymized participant identifier
- `Session`: session number
- `SessionID`: combined participant-session identifier
- `Test`: experimental scenario identifier
- PANAS item scores, including `Interested`, `Distressed`, `Excited`, `Upset`, `Strong`, `Guilty`, `Scared`, `Hostile`, `Enthusiastic`, `Proud`, `Irritable`, `Alert`, `Ashamed`, `Inspired`, `Nervous`, `Determined`, `Attentive`, `Jittery`, `Active`, and `Afraid`
- `Positive affect`: summed positive affect score
- `Negative affect`: summed negative affect score
- `Possible distraction errors`: quality-control or note field for potential questionnaire issues

## `00_data/processed/02_Comfort.xlsx`

Session-level indoor-experience and comfort questionnaire data.

Key columns include:

- `Participant`
- `Session`
- `SessionID`
- `Test`
- `Comfort`
- `Atmosphere`
- `Layout`
- `Size`
- `Colors`
- `Textures`
- `Lighting`
- `Temperature`
- `Air quality`
- `Acoustic`
- `Cleanliness`
- `Total score`
- `Interiors score`
- `Comfort score`
- `Possible distraction errors`
- `Note`

## `00_data/processed/03_Attention.xlsx`

Session-level attention-task outcomes.

Key columns include:

- `Participant`
- `Ref Table`
- `Session`
- `SessionID`
- `Test`
- `Attempted matches`
- `Correct matches`
- `Errors`
- `Errors %`
- `Perseveration errors`
- `Perseveration errors %`
- `Non-p errors`
- `Non-p errors %`
- `Rule runs`

## `00_data/processed/10_MergedEDAIAQSessID.csv`

Merged physiological and indoor-environmental dataset.

Main groups of variables include:

- Identifiers and timing: `Participant`, `SessionID`, `UNIX`, `datetime`, `Date`, `Time`, `ElapsedMinutes`
- EDA variables: `EDA`, `EDA_Raw`, `EDA_Clean`, `EDA_Tonic`, `EDA_Phasic`, `SCR_Onsets`, `SCR_Peaks`, `SCR_Height`, `SCR_Amplitude`, `SCR_RiseTime`, `SCR_Recovery`, `SCR_RecoveryTime`
- IAQ/environmental variables: `temperature`, `humidity`, `co2`, `tvoc`, `pm1`, `pm2_5`, `pm10`, `oxygen`, `co`, `o3`, `no2`, `sound`, `pressure`, and associated error/quality columns where available
- Device/status variables: `DeviceID`, `Status`, `uptime`, `bat`, `health`, `performance`

## Experimental scenario coding

The `Test` column identifies the experimental scenario. According to the manuscript draft:

1. No plants / baseline
2. Real indoor plants
3. Artificial plants / visual placebo
4. Real plants outside the window / visual control

## Notes for future improvement

For publication-grade reuse, this file should be expanded with:

- exact units for each environmental variable;
- exact questionnaire scale ranges;
- missing-data codes;
- preprocessing and exclusion rules;
- sensor model and calibration information;
- participant inclusion/exclusion criteria;
- links between raw Empatica folders and participant/session identifiers.
