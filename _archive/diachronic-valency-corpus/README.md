# Diachronic Valency Corpus Platform

## Project Overview
A fully automated, open-source platform for diachronic valency corpus research. Integrates NLP agents, academic resources, open-access collectors, and a web platform for tracking verb argument structure changes over time across Indo-European languages.

- 24/7 agent-based data collection and processing
- Valency pattern extraction (Stanza, WebLicht, spaCy, web APIs)
- Academic resource integration (ValPaL, DiGrec, Diorisis)
- Open-access text collectors (Perseus, First1KGreek, PROIEL, etc.)
- FastAPI backend, React frontend, PostgreSQL database
- Automated CI/CD, Docker, and GitHub integration

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/nlavidas/diachronic-indo-european-corpus.git
   cd diachronic-indo-european-corpus
   ```
2. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   pip install psycopg2-binary
   ```
3. Install Node dependencies for frontend:
   ```sh
   cd web_frontend && npm install
   ```
4. Set up PostgreSQL and run migrations:
   ```sh
   psql $DATABASE_URL -f migrations/add_ai_discovered_column.sql
   ```
5. (Optional) Build and run with Docker Compose:
   ```sh
   docker-compose up --build
   ```

## Usage Examples
- Start the orchestrator:
  ```sh
  python master_orchestrator.py
  ```
- Access the web platform at [http://localhost:3000](http://localhost:3000)
- Use the API (see below)

## Academic Citations
If you use this platform in research, please cite:
- Lavidas, N. et al. (2025). "Diachronic Valency Corpus: An Open Platform for Historical Linguistics." (preprint)
- [ValPaL Project](https://valpal.info/), [Diorisis](https://diorisis.org/), [PROIEL](https://proiel.github.io/)

---

## API Documentation
See [API_DOCS.md](API_DOCS.md)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)

## Data Format
See [DATA_FORMAT.md](DATA_FORMAT.md)

## Methodology
See [METHODOLOGY.md](METHODOLOGY.md)
