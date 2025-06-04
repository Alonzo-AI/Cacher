
# Data Transformation & Anonymization Model

## Overview
This tool helps anonymize sensitive data in CSV files by hashing specified identifier columns and dropping unnecessary columns. It outputs a clean CSV suitable for model training or sharing without exposing private information.

---

## Features

- Hash sensitive identifier columns using SHA-256 (configurable hash length).
- Drop unneeded columns specified in the configuration.
- Save mapping files linking original values to hashed values for traceability.
- Configurable via a simple JSON file.

---

## Example Configuration (`config.json`)

```json
{
  "ids": ["MRN"],
  "remove": ["Age", "Marital Status", "State"]
}
```

- **ids:** List of columns to anonymize by hashing (e.g., `"MRN"`).
- **remove:** List of columns to remove from the output (e.g., `"Age"`, `"Marital Status"`, `"State"`).

---

## Internal Workflow

1. **Hashing Identifiers:**
   - Hashes each unique value in the specified `ids` columns using SHA-256.
   - Uses only the first 8 characters of the hash (default, configurable).
   
2. **Mapping Files:**
   - Saves a CSV file mapping original values to hashed values for each ID column (e.g., `mrn_map.csv`).
   
3. **Column Dropping:**
   - Removes columns listed under `remove` in the configuration.
   
4. **Output:**
   - Saves the transformed CSV as `transformed_output.csv` (or your specified output filename).

---

## How to Use:

1. Open terminal
2. Run:

   ./anonymizer mock_dataset.csv --config config.json
   
   	-mock_dataset.csv — your input dataset
	-config.json — configuration file specifying columns to transform/anonymize

3. Output files:
   - transformed_output.csv — the anonymized dataset
   - <column>_map.csv — mapping file(s) for each anonymized column



Given a CSV with columns:

| MRN    | Name | Age | Marital Status | State    | Diagnosis |
|--------|------|-----|----------------|----------|-----------|
| 123456 | John | 45  | Married        | Texas    | Flu       |
| 789012 | Jane | 29  | Single         | Florida  | Cold      |

Running the tool with the config above will:

- Hash the `MRN` column, replacing values with hashed versions.
- Drop `Age`, `Marital Status`, and `State` columns.
- Save a mapping file `mrn_map.csv`.
- Output a CSV with columns:

| MRN       | Name | Diagnosis |
|-----------|------|-----------|
| A1B2C3D4  | John | Flu       |
| E5F6G7H8  | Jane | Cold      |

---


