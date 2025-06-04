import pandas as pd
import hashlib
import argparse
import json

def hash_id(value, algo="sha256", length=8):
    return hashlib.new(algo, str(value).encode()).hexdigest()[:length].upper()

def generate_mappings(df, columns, hash_type, hash_length):
    mappings = {}
    for col in columns:
        unique_vals = df[col].dropna().astype(str).unique()
        mappings[col] = {val: hash_id(val, hash_type, hash_length) for val in unique_vals}
    return mappings

def save_mapping_file(mapping_dict, col_name, output_path):
    df_map = pd.DataFrame(list(mapping_dict.items()), columns=[f'Original_{col_name}', f'Transformed_{col_name}'])
    df_map.to_csv(output_path, index=False)

def process_csv(cfg, input_file, output_file, hash_type="sha256", hash_length=8):
    df = pd.read_csv(input_file)

    ids = cfg.get("ids", [])
    remove_cols = cfg.get("remove", [])

    for col in ids:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' specified in config 'ids' is not found in the CSV.")

    mappings = generate_mappings(df, ids, hash_type, hash_length)

    # Save separate mapping files
    for col in ids:
        col_safe = col.lower().replace(" ", "_")
        out_map_file = f"{col_safe}_map.csv"
        save_mapping_file(mappings[col], col.replace(" ", "_"), out_map_file)
        print(f" Saved mapping file: {out_map_file}")

    # Replace original IDs with hashed ones
    for col in ids:
        df[col] = df[col].astype(str).map(mappings[col])

    # Drop specified columns
    df.drop(columns=[c for c in remove_cols if c in df.columns], inplace=True)

    # Save final transformed CSV
    df.to_csv(output_file, index=False)
    print(f"Saved transformed file: {output_file}")
    return df

def main():
    parser = argparse.ArgumentParser(description="Transform and anonymize medical CSV using JSON config")
    parser.add_argument("input_file", help="Input CSV file path")
    parser.add_argument("--config", required=True, help="JSON config file path")
    parser.add_argument("-o", "--output", default="transformed_output.csv", help="Output CSV file path")
    parser.add_argument("--hash", choices=["md5", "sha1", "sha256"], default="sha256", help="Hash algorithm")
    parser.add_argument("--length", type=int, default=8, help="Length of hash prefix")

    args = parser.parse_args()

    #  Properly load JSON config
    with open(args.config, 'r') as f:
        config = json.load(f)

    process_csv(config, args.input_file, args.output, args.hash, args.length)

if __name__ == "__main__":
    main()
