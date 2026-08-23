import os
import pandas as pd

def generate_simple_md_table(df, max_rows=5):
    """Converts a DataFrame slice into a basic Markdown table string without external dependencies."""
    headers = [str(c) for c in df.columns]
    md_lines = []
    md_lines.append("| " + " | ".join(headers) + " |")
    md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    
    for _, row in df.head(max_rows).iterrows():
        clean_row = [str(val).replace('\n', ' ').replace('|', '\\|') for val in row]
        md_lines.append("| " + " | ".join(clean_row) + " |")
        
    return "\n".join(md_lines)


def generate_data_overview_report(target_dir=None, output_filename="data_overview_report.md"):
    """
    Scans the target directory for tabular files (.csv, .xlsx, .tsv), 
    analyzes their structure, and generates a Markdown data profiling report.
    """
    if target_dir is None:
        if '__file__' in globals():
            target_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            target_dir = os.getcwd()

    markdown_output = []
    markdown_output.append("# Data Inspection & Overview Report\n")
    markdown_output.append(f"**Root Directory:** `{target_dir}`\n")
    markdown_output.append("---\n")

    supported_extensions = ('.csv', '.tsv', '.xlsx', '.xls')
    data_files = []

    # Find all supported data files
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.lower().endswith(supported_extensions):
                data_files.append(os.path.join(root, file))

    if not data_files:
        print("[-] No tabular files found.")
        markdown_output.append("No dataset files (.csv, .xlsx, etc.) were found.\n")
        return

    print(f"[*] Found {len(data_files)} dataset(s) to analyze.\n")

    for file_path in data_files:
        relative_path = os.path.relpath(file_path, target_dir)
        print(f"[*] Analyzing: {relative_path}")

        markdown_output.append(f"## Dataset: `{relative_path}`\n")

        try:
            # Read dataset according to extension
            if file_path.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)

            total_rows, total_cols = df.shape
            duplicate_count = df.duplicated().sum()
            dup_percentage = (duplicate_count / total_rows * 100) if total_rows > 0 else 0.0

            # 1. Dataset Dimensions and Duplicates
            markdown_output.append("### 1. General Info")
            markdown_output.append(f"- **Total Rows:** `{total_rows:,}`")
            markdown_output.append(f"- **Total Columns:** `{total_cols:,}`")
            markdown_output.append(f"- **Duplicate Rows:** `{duplicate_count:,}` ({dup_percentage:.2f}%)\n")

            # 2. Columns Profiling for Data Cleaning
            markdown_output.append("### 2. Columns Profiling")
            markdown_output.append("| Column Name | Data Type | Non-Null | Missing Count | Missing % | Unique Values | Sample Value |")
            markdown_output.append("| --- | --- | --- | --- | --- | --- | --- |")

            for col in df.columns:
                dtype = str(df[col].dtype)
                non_null_cnt = df[col].notnull().sum()
                missing_cnt = df[col].isnull().sum()
                missing_pct = (missing_cnt / total_rows * 100) if total_rows > 0 else 0.0
                unique_cnt = df[col].nunique(dropna=True)
                
                # Sample non-null value
                sample_series = df[col].dropna()
                sample_val = str(sample_series.iloc[0]) if not sample_series.empty else "N/A"
                sample_val_clean = sample_val.replace('\n', ' ').replace('|', '\\|')
                if len(sample_val_clean) > 30:
                    sample_val_clean = sample_val_clean[:27] + "..."

                markdown_output.append(
                    f"| `{col}` | `{dtype}` | {non_null_cnt:,} | {missing_cnt:,} | {missing_pct:.2f}% | {unique_cnt:,} | {sample_val_clean} |"
                )
            markdown_output.append("\n")

            # 3. Numeric Summary (if numeric columns exist)
            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                markdown_output.append("### 3. Numerical Summary")
                desc = numeric_df.describe().T[['min', '25%', '50%', '75%', 'max', 'mean', 'std']]
                desc_reset = desc.reset_index().rename(columns={'index': 'Column'})
                markdown_output.append(generate_simple_md_table(desc_reset, max_rows=len(desc_reset)))
                markdown_output.append("\n")

            # 4. Preview Data (First 5 rows)
            markdown_output.append("### 4. Data Preview (Head 5 Rows)")
            markdown_output.append(generate_simple_md_table(df, max_rows=5))
            markdown_output.append("\n---\n")

            print(f"    [+] Completed profiling ({total_rows} rows x {total_cols} cols).")

        except Exception as err:
            markdown_output.append(f"**Error analyzing file:** `{err}`\n\n---\n")
            print(f"    [-] Failed to process {relative_path}: {err}")

    # Save output to Markdown file
    output_path = os.path.join(target_dir, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_output))

    print(f"\n[✔] Analysis complete! Report saved as: {output_filename}")

if __name__ == "__main__":
    generate_data_overview_report()