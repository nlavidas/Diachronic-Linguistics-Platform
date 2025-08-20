import argparse
from lingpy import LexStat

def run_cognate_detection(input_file, output_file):
    try:
        lex = LexStat(input_file)
        lex.get_scorer(runs=1000)
        lex.cluster(method='lexstat', threshold=0.55, ref='cognateset_id')
        lex.output('tsv', filename=output_file.replace('.tsv', ''), ignore='all', prettify=False)
        print(f"? Cognate detection complete. Results written to {output_file}")
    except Exception as e:
        print(f"? An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run cognate detection on a wordlist.")
    parser.add_argument("--input", default="wold/cldf/forms.csv", help="Path to the input wordlist file (e.g., forms.csv).")
    parser.add_argument("--output", default="wold_cognates.tsv", help="Path for the output TSV file.")
    args = parser.parse_args()
    
    run_cognate_detection(args.input, args.output)
