# Methodology Explanation

## Overview
This platform combines automated NLP, academic resource integration, and open-access text collection to build a diachronic valency corpus for Indo-European languages.

## Steps
1. **Data Collection**: Agents collect texts from open-access sources and academic resources.
2. **Preprocessing**: Texts are cleaned, normalized, and language/year detected.
3. **Valency Extraction**: NLP tools (Stanza, WebLicht, spaCy, or web APIs) extract verb argument structures.
4. **Annotation**: Patterns are stored in JSON and imported into the database.
5. **Web Platform**: Data and annotations are served via API and visualized in the frontend.
6. **Automation**: Orchestrator runs all steps 24/7, with error handling and daily updates.

## Academic Rigor
- All resources are cited and open-access.
- Extraction and alignment algorithms are documented and reproducible.
- Data formats are transparent and versioned.

## Citation
If you use this methodology, cite:
Lavidas, N. et al. (2025). "Diachronic Valency Corpus: An Open Platform for Historical Linguistics."
