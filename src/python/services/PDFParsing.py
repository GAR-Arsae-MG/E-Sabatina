#! python3

# Authors:  Túlio Ferreira Horta - (TFH, Duke).
# Last modification: DUKE-11_nov_25

import fitz
from collections import defaultdict
from typing import List, Dict, Tuple


class TableExtractor:
    """Advanced table extraction from PDF using PyMyPDF"""

    def __init__(self, pdf_path: str):
        self.doc = fitz.open(pdf_path)

    def close(self):
        self.doc.close()

    def get_text_blocks(self, page: fitz.Page) -> List[Dict]:
        """Extract all text blocks with positions"""
        blocks = []
        text_dict = page.get_text("dict")

        for block in text_dict["blocks"]:
            if block["type"] == 0:  # Text block
                for line in block["lines"]:
                    for span in line["spans"]:
                        blocks.append(
                            {
                                "text": span["text"].strip(),
                                "x0": span["bbox"][0],
                                "y0": span["bbox"][1],
                                "x1": span["bbox"][2],
                                "y1": span["bbox"][3],
                                "font_size": span["size"],
                            }
                        )
        return blocks

    def detect_rows(
        self, blocks: List[Dict], tolerance: float = 3.0
    ) -> Dict[float, List[Dict]]:
        """Group text blocks into rows based on y-coordinate"""
        rows = defaultdict(list)

        for block in blocks:
            # Round y-coordinate to group nearby blocks
            y_key = round(block["y0"] / tolerance) * tolerance
            rows[y_key].append(block)

        # Sort each row by x-coordinate
        for y_key in rows:
            rows[y_key].sort(key=lambda b: b["x0"])

        return dict(rows)

    def detect_columns(self, rows: Dict[float, List[Dict]]) -> List[float]:
        """Detect column boundaries by finding consistent x-positions"""
        x_positions = defaultdict(int)

        for row_blocks in rows.values():
            for block in row_blocks:
                # Round x-positions to find alignment
                x_key = round(block["x0"] / 2) * 2
                x_positions[x_key] += 1

        # Find x-positions that appear frequently (column starts)
        threshold = len(rows) * 0.3  # Appears in at least 30% of rows
        column_boundaries = sorted(
            [x for x, count in x_positions.items() if count >= threshold]
        )

        return column_boundaries

    def assign_to_columns(
        self,
        row_blocks: List[Dict],
        column_boundaries: List[float],
        tolerance: float = 10.0,
    ) -> List[str]:
        """Assign text blocks to columns"""
        if not column_boundaries:
            return [block["text"] for block in row_blocks]

        # Initialize columns
        num_cols = len(column_boundaries)
        columns = [""] * num_cols

        for block in row_blocks:
            # Find which column this block belongs to
            assigned = False
            for i, col_x in enumerate(column_boundaries):
                if abs(block["x0"] - col_x) < tolerance:
                    columns[i] += block["text"] + " "
                    assigned = True
                    break

            # If not assigned, put in nearest column
            if not assigned:
                distances = [abs(block["x0"] - col_x) for col_x in column_boundaries]
                nearest_col = distances.index(min(distances))
                columns[nearest_col] += block["text"] + " "

        # Clean up
        return [col.strip() for col in columns]

    def is_table_row(self, row_blocks: List[Dict], min_cols: int = 2) -> bool:
        """Heuristic to determine if a row is part of a table"""
        # Table rows typically have multiple aligned elements
        return len(row_blocks) >= min_cols

    def extract_tables_from_page(self, page_num: int) -> List[Dict]:
        """Extract tables from a single page"""
        page = self.doc[page_num]
        blocks = self.get_text_blocks(page)

        if not blocks:
            return []

        # Group into rows
        rows = self.detect_rows(blocks)

        # Detect column structure
        column_boundaries = self.detect_columns(rows)

        # Build table(s)
        tables = []
        current_table = []

        for y in sorted(rows.keys()):
            row_blocks = rows[y]

            # Check if this looks like a table row
            if self.is_table_row(row_blocks):
                # Assign to columns
                row_data = self.assign_to_columns(row_blocks, column_boundaries)
                current_table.append(row_data)
            else:
                # Gap in table - save current table if exists
                if len(current_table) >= 2:  # At least 2 rows
                    tables.append(
                        {
                            "page": page_num + 1,
                            "data": current_table,
                            "num_rows": len(current_table),
                            "num_cols": len(current_table[0]) if current_table else 0,
                        }
                    )
                current_table = []

        # Don't forget the last table
        if len(current_table) >= 2:
            tables.append(
                {
                    "page": page_num + 1,
                    "data": current_table,
                    "num_rows": len(current_table),
                    "num_cols": len(current_table[0]) if current_table else 0,
                }
            )

        return tables

    def extract_all_tables(self) -> List[Dict]:
        """Extract tables from all pages"""
        all_tables = []

        for page_num in range(len(self.doc)):
            page_tables = self.extract_tables_from_page(page_num)
            all_tables.extend(page_tables)

        return all_tables

    def extract_text_and_tables(self) -> Dict:
        """Extract both text and tables"""
        result = {"text": "", "tables": [], "pages": []}

        for page_num in range(len(self.doc)):
            page = self.doc[page_num]

            # Extract text
            page_text = page.get_text()
            result["text"] += f"\n=== Page {page_num + 1} ===\n{page_text}\n"

            # Extract tables
            page_tables = self.extract_tables_from_page(page_num)
            result["tables"].extend(page_tables)

            # Store page info
            result["pages"].append(
                {"page_num": page_num + 1, "text": page_text, "tables": page_tables}
            )

        return result
