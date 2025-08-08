\# Diachronic Linguistics Platform \& Corpus Builder



\## Project Vision

This repository houses the code for a comprehensive, open-source platform for diachronic linguistic analysis. The project aims to collect, preprocess, and analyze a large corpus of influential texts across multiple Indo-European languages and chronological periods, with a primary focus on verb valency and argument structure.



\## Master Plan



\### Phase 1: Foundation (Local \& Cloud)

\* \*\*\[COMPLETED] 1.1: Portable Python Environment:\*\* A self-contained WinPython "workshop" on a portable drive for all tools and data.

\* \*\*\[IN PROGRESS] 1.2: Central Code Repository:\*\* This new, unified GitHub repository will serve as the single source of truth for all project code.



\### Phase 2: Data Acquisition \& Integration

\* \*\*\[IN PROGRESS] 2.1: The "MEGA Scraper" Agent:\*\* An advanced script to automatically gather unannotated texts from multiple sources, including Project Gutenberg, the Perseus Digital Library, and the Internet Archive. It will be enhanced with Optical Character Recognition (OCR) for digitizing manuscripts.

\* \*\*\[TO DO] 2.2: The "Professional Corpus Importer":\*\* A specialized agent (`importer.py`) to ingest and harmonize pre-parsed corpora, including \*\*Jana Beck's PPCHiG (Hellenistic Greek)\*\* and the \*\*Penn-Helsinki Parsed Corpora\*\* (Historical English).



\### Phase 3: Quality Control \& Curation

\* \*\*\[TO DO] 3.1: The "Gatekeeper" Agent:\*\* A validation script (`validator.py`) to automatically scan all acquired texts for errors, incorrect languages, or boilerplate text and quarantine them for manual review.



\### Phase 4: AI Preprocessing \& Analysis

\* \*\*\[IN PROGRESS] 4.1: The "PROIEL Engine" (`preprocessor.py`):\*\* This agent processes all curated raw texts, performing deep linguistic analysis (tokenization, lemmatization, morphology, dependency parsing) in the style of \*\*PROIEL\*\*.

\* \*\*\[TO DO] 4.2: The Valency \& Contact Extractor:\*\* A module to specifically extract verb valency patterns and identify loanwords based on the parsed data.



\### Phase 5: Structured Storage

\* \*\*\[IN PROGRESS] 5.1: The Unified Database:\*\* A portable SQLite database (`corpus.db`) to store all harmonized linguistic data from both our custom preprocessing and imported professional corpora.



\### Phase 6: The "Lightside-Style" Digital Tools Platform

\* \*\*\[TO DO] 6.1: The Interactive Interface:\*\* A password-protected web platform with a menu of tools to browse, search, and run analyses on the corpus, built with a framework like \*\*Streamlit\*\*.

\* \*\*\[TO DO] 6.2: Open-Source Toolkit:\*\* The backend Python scripts will be structured as a reusable, open-source toolkit for digital humanities research.



\### Phase 7: The Diachronic AI-Agent

\* \*\*\[FUTURE GOAL] 7.1: Conversational Research Interface:\*\* The ultimate goal of the platform—an AI agent that can answer high-level research questions (e.g., "How did the arguments of verb X change between period A and B?") by querying the database and synthesizing the results.

