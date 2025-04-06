import pdfplumber
import os
import pandas as pd
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

cwd = os.getcwd()
pdf_folder = os.path.join(cwd, 'data')

def extract_ncids_from_pdf(pdf_filename):
    pdf_path = os.path.join(pdf_folder, pdf_filename)
    ncids = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in reversed(pdf.pages):
                tables = page.extract_tables()

                for table in tables:
                    headers = table[0]
                    headers_lower = [h.lower() if h else '' for h in headers]

                    if 'ncid' in headers_lower:
                        ncid_index = headers_lower.index('ncid')

                        for row in table[1:]:
                            if row and len(row) > ncid_index:
                                ncid_value = row[ncid_index]
                                if ncid_value:
                                    ncids.append({
                                        'filename': pdf_filename,
                                        'page': page.page_number,
                                        'ncid': ncid_value
                                    })
    except Exception as e:
        print(f"Error processing {pdf_filename}: {e}")

    return ncids

if __name__ == '__main__':
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]

    all_ncids = []

    with Pool(processes=cpu_count() - 1) as pool:
        for result in tqdm(pool.imap_unordered(extract_ncids_from_pdf, pdf_files), total=len(pdf_files)):
            all_ncids.extend(result)

    print(f"Done! Extracted {len(all_ncids)} NCIDs total.")

    # Save to CSV
    df = pd.DataFrame(all_ncids)
    df.to_csv('all_extracted_ncids.csv', index=False)

    print("Saved all NCIDs to 'all_extracted_ncids.csv'.")