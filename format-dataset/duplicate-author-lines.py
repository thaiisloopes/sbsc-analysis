import pandas as pd

def explode_authors(input_csv: str, output_csv: str):
    # Read input CSV
    df = pd.read_csv(input_csv)

    # Identify author and affiliation columns
    author_cols = [col for col in df.columns if "author-name" in col.lower()]
    affil_cols = [col for col in df.columns if "affiliation" in col.lower()]

    # Create a long-format dataframe
    exploded_rows = []

    for _, row in df.iterrows():
        for i, author_col in enumerate(author_cols):
            author_name = row.get(author_col)
            if pd.isna(author_name) or str(author_name).strip() == "":
                continue  # skip empty author slots

            # Match with affiliation (if exists)
            affil = None
            if i < len(affil_cols):
                affil = row.get(affil_cols[i])

            # Copy all columns
            new_row = row.to_dict()

            # Keep only single author and its affiliation
            new_row["author"] = author_name
            new_row["affiliation"] = affil

            exploded_rows.append(new_row)

    # Build normalized dataframe
    exploded_df = pd.DataFrame(exploded_rows)

    # Drop original multiple-author columns
    cols_to_drop = author_cols + affil_cols
    exploded_df = exploded_df.drop(columns=[c for c in cols_to_drop if c in exploded_df.columns])

    # Save result
    exploded_df.to_csv(output_csv, index=False)


explode_authors("../sbsc_dataset.csv", "../sbsc_dataset_normalized.csv")
