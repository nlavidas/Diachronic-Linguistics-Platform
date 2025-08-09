Master Plan v2.2: The Diachronic Valency Platform
Project Lead: nlavidas
AI Assistant: Gemini

Vision: To create a comprehensive, open-source platform for diachronic linguistic analysis, focusing on verb valency, argument structure, and language contact across Indo-European languages. The platform will feature a suite of AI-enhanced digital tools and will unify newly processed texts with existing professional corpora.

Phase 1: Foundation (Local Workshop & Cloud Blueprint)
[COMPLETED] 1.1: Portable Python Environment (Z: Drive): A self-contained WinPython environment for all tools and data.

[COMPLETED] 1.2: Central Code Repository (GitHub): The private Diachronic-Linguistics-Platform repository serves as the single source of truth for all project code.

Phase 2: Data Acquisition & Integration
[IN PROGRESS] 2.1: Automated Raw Text Collection (The "MEGA Scraper"): This agent finds and downloads unannotated texts from sources like Project Gutenberg, the Perseus Digital Library, and the Internet Archive. It will be enhanced with Optical Character Recognition (OCR) for digitizing manuscripts.

[TO DO] 2.2: Ingestion of Pre-Parsed Corpora (The "Professional Data Importer"): A specialized agent (importer.py) to download and parse existing professional corpora, such as Jana Beck's PPCHiG (Hellenistic Greek) and the Penn-Helsinki Parsed Corpora (Historical English).

Phase 3: Quality Control & Curation
[TO DO] 3.1: Automated Validation Tool (The "Gatekeeper" Agent): A new agent (validator.py) will automatically scan all acquired texts to check for errors, incorrect languages, or boilerplate, and quarantine bad files for manual review.

Phase 4: AI Preprocessing (The PROIEL Engine)
[IN PROGRESS] 4.1: The preprocessor.py Agent: Processes all curated raw texts and performs deep linguistic analysis (tokenization, lemmatization, morphology, dependency parsing) in the style of PROIEL.

[TO DO] 4.2: The Valency & Contact Extractor: A module to specifically extract verb valency patterns and identify loanwords based on the parsed data.

Phase 5: Structured Storage (The Unified Database)
[IN PROGRESS] 5.1: The corpus.db File: A portable SQLite database on the Z: drive that acts as the central, unified store for all project data.

[TO DO] 5.2: Harmonized Schema: The database will be structured to merge data from our own preprocessor and the imported professional corpora, tracking the source of every annotation.

Phase 6: The "Lightside-Style" Digital Tools Platform
[TO DO] 6.1: The Interactive Interface: A password-protected web platform with a menu of tools to browse, search, and run analyses on the corpus, built with a framework like Streamlit.

[TO DO] 6.2: Open-Source Toolkit: The backend Python scripts will be structured as a reusable, open-source toolkit for digital humanities research.

Phase 7: The Diachronic AI-Agent
[FUTURE GOAL] 7.1: The Conversational Interface: A chat-based agent integrated into the platform.

[FUTURE GOAL] 7.2: The AI Query Engine: The agent will translate natural language research questions into complex database queries and synthesize the results.