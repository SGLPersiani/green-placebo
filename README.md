# Physiological and Subjective Responses to Indoor Greenery

This repository contains the data, processing scripts, and manuscript material for the controlled crossover experiment reported in:

**Physiological and subjective responses to indoor greenery: A controlled crossover experiment**  
Sandra G. L. Persiani and Bilge Kobas

The study examines whether indoor greenery influences occupants' physiological state and subjective experience under controlled, office-like indoor environmental conditions. Participants completed four 90-minute experimental scenarios: no plants, real indoor plants, artificial plants as a visual placebo, and real plants placed outside the window as a visual control.

## Repository structure

```text
.
├── 00_data/
│   ├── raw/
│   │   ├── EMPATICA/        # Raw and intermediate Empatica E4 exports
│   │   └── IAQ/             # Indoor air-quality and environmental sensor exports
│   └── processed/           # Processed questionnaire, attention, EDA, and merged datasets
├── 01_codes/                # Python scripts for formatting, processing, and visualization
├── 02_figures/              # Manuscript and analysis figures
├── 03_text/                 # Manuscript draft
├── README.md
├── requirements.txt
├── DATA_DICTIONARY.md
├── CITATION.cff
└── .gitignore
```

## Study overview

The experiment used a within-subject crossover design in a controlled climate chamber. Each participant experienced the same four scenarios in randomized order:

1. **No plants**: baseline office-like room.
2. **Real indoor plants**: living plants inside the room.
3. **Artificial plants**: visual placebo condition.
4. **Real plants outside the window**: visual greenery without direct indoor plant interaction.

Physiological data were recorded using Empatica E4 wristbands, including electrodermal activity, skin temperature, acceleration, blood volume pulse, and heart-rate-derived features. Indoor environmental quality was monitored using IAQ sensors. Subjective and cognitive outcomes include PANAS, comfort/satisfaction ratings, and an attention task.

## Data contents

### Raw data

`00_data/raw/EMPATICA/` contains Empatica E4 session folders. Typical files include:

- `EDA.csv`: electrodermal activity
- `BVP.csv`: blood volume pulse
- `HR.csv`: heart rate
- `TEMP.csv`: wrist skin temperature
- `ACC.csv`: acceleration
- `IBI.csv`: inter-beat intervals
- `tags.csv`: event markers
- `info.txt`: device/session metadata

Some folders also contain generated intermediate files such as `EDA2b.csv`, `EDAClean.csv`, `BVP2b.csv`, or HRV feature files.

`00_data/raw/IAQ/` contains converted indoor air-quality and environmental sensor files.

### Processed data

`00_data/processed/` contains derived analysis files, including:

- `01_Panas.xlsx`: PANAS affect questionnaire data
- `02_Comfort.xlsx`: comfort and indoor-experience questionnaire data
- `03_Attention.xlsx`: attention-task outcomes
- `10_MergedEDAIAQSessID.csv`: merged EDA, IAQ, and session-level data

See [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) for a compact description of the main processed files and variables.

## Code

The main scripts are located in `01_codes/`:

- `EDA_format_and_process.py`: reshapes Empatica EDA files and extracts cleaned EDA features using NeuroKit2.
- `HRV_format_process.py`: reshapes Empatica BVP files and derives HRV-related features using HeartPy.
- `HRV_format_process_v2.py`: segment-wise BVP/HRV processing.
- `Datasets.py`: merges questionnaire, session, EDA, and IAQ datasets.
- `Vis.py`: exploratory analysis and visualization code.

The scripts were originally written as research-analysis scripts and may require path adjustments before being run on a new machine. Several paths use Windows-style separators. On macOS/Linux, replace paths such as:

```python
".\\EMPATICA"
```

with:

```python
"00_data/raw/EMPATICA"
```

or use `pathlib.Path` for platform-independent paths.

## Python environment

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Core dependencies are:

- pandas
- numpy
- matplotlib
- seaborn
- scipy
- statsmodels
- neurokit2
- heartpy
- openpyxl
- pytz

## Suggested reproducibility workflow

A typical reconstruction workflow is:

1. Place the repository root as the working directory.
2. Process raw Empatica EDA data with `01_codes/EDA_format_and_process.py`.
3. Process raw Empatica BVP/HRV data with `01_codes/HRV_format_process.py` or `01_codes/HRV_format_process_v2.py`.
4. Merge processed physiological, questionnaire, and IAQ files using `01_codes/Datasets.py`.
5. Generate exploratory and manuscript figures using `01_codes/Vis.py`.

At present, the scripts are not yet packaged as a single automated pipeline. For archival reproducibility, users should record any local path edits, exclusion rules, and generated intermediate files.

## Data protection and ethics note

This repository contains human-participant physiological and questionnaire data. Although participant labels are pseudonymized, physiological time series can still be sensitive. Before making the repository public, confirm that:

- participant consent covers public data sharing;
- institutional ethics approvals permit the proposed level of sharing;
- indirect identifiers have been removed or minimized;
- raw high-resolution physiological files are suitable for open release;
- any manuscript-review or journal embargo requirements are respected.

If full public release is not appropriate, consider keeping raw data private and sharing only processed/aggregated datasets, a codebook, and reproducible analysis scripts.

## Large-file note

The repository contains several large CSV files, especially processed BVP files. GitHub currently blocks individual files above 100 MB and warns for files above 50 MB. The current files appear to be below the hard limit, but Git Large File Storage may still be preferable if the repository grows.

## Citation

Please cite the manuscript or repository record associated with this project. A preliminary citation metadata file is provided in [`CITATION.cff`](CITATION.cff). Update it with the final publication title, DOI, and repository DOI when available.

## License

No explicit license is assigned in this repository yet. Until a license is added, reuse rights are not formally granted. Before public release, add an appropriate software/data license after confirming author, institutional, ethics, and journal requirements.

Common choices are:

- **MIT License** for analysis code;
- **CC BY 4.0** for openly reusable documentation and non-sensitive derived data;
- a more restrictive data-use statement for human-participant raw data, where necessary.
