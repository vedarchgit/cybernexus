# CyberNexus

## What is CyberNexus?
**CyberNexus** is an open-source platform designed to make **timely, accurate, and actionable cyber threat intelligence** accessible to everyone.  
Startups, NGOs, universities, and small companies can securely **submit, search, and visualize global cyber threats** — including phishing, ransomware, malware, and DDoS — without expensive tools or barriers.  

Powered by **MariaDB** and **Python**, CyberNexus is **affordable, transparent, and community-driven**.

---

## Project Status (MVP Implemented)

This repository now contains a functional Minimum Viable Product (MVP) for CyberNexus, including:

*   **Containerized Backend & Database:** The entire backend (FastAPI) and database (MariaDB) are containerized with Docker, allowing for a one-command setup.
*   **RESTful API:** A backend API with endpoints to create, list, and search for cyber threats.
*   **Persistent Storage:** Threat data is stored in a MariaDB database.
*   **Audit Trail:** The backend now logs all new threat submissions for security and transparency.
*   **React + TailwindCSS Frontend:** A functional user interface for submitting, viewing, and searching for threats.

## Getting Started

### Prerequisites
*   **Docker and Docker Compose:** Required to run the backend and database. [Install Docker](https://docs.docker.com/get-docker/).
*   **Python:** Required for the CLI tool.
*   **Node.js and npm:** Required to run the frontend. [Install Node.js](https://nodejs.org/en/download/).

### How to Run

1.  **Start the Backend & Database:**
    From the project root directory, run:
    ```bash
    docker-compose up --build -d
    ```
    The API will be available at `http://localhost:8000`.

2.  **Install Python Dependencies (for CLI):**
    In a new terminal, install all Python dependencies from the central requirements file:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Using the Application:**
    You can interact with CyberNexus through the Web UI or the new CLI.

    *   **Web UI:**
        Navigate to the `frontend` directory and run:
        ```bash
        cd frontend
        npm install
        npm run dev
        ```
        The web application will be accessible at `http://localhost:5173`.

    *   **Command-Line Interface (CLI):**
        Once the backend is running and dependencies are installed, you can use the CLI from the project root:
        ```bash
        # See all available commands
        python -m cli.main --help

        # Search for a threat
        python -m cli.main search --type phishing

        # Submit a new threat
        python -m cli.main submit evil.com malware manual-report
        ```

---

## Key Features We Plan to Build

### Easy-to-Use Web Dashboard (React + TailwindCSS)
- Submit new threats, search existing indicators, and visualize attack trends in real-time.

### Scalable Backend (FastAPI / Flask + MariaDB)
- Handles millions of threat records (IPs, URLs, file hashes) securely with fast search and storage.

### ML-Based Analytics
- Python modules to cluster threats, detect emerging campaigns, and analyze attack patterns by location, type, or trend.

### Open APIs
- Encourage public contributions, integrations, and community-built tools.

---

## Good-to-Have Features

- **Mobile App:** Instantly report threats and receive push notifications or alerts.  
- **Live Notifications:** Customizable alerts via WhatsApp, SMS, or app notifications.  
- **AI for Zero-Day Detection:** Identify unknown or emerging threats before databases update.  
- **Multilingual Dashboard:** Localized UI for global participation.  
- **Blockchain Logging:** Tamper-proof, auditable record trails for transparency.

---

## Constraints

- **High Compute Requirements:** Advanced ML analyses need strong servers.  
- **Data Normalization:** Integrating multiple sources demands standardized formats.  
- **Network Latency:** Real-time sharing may lag on slow or unstable connections.

---

## Known Issues

- **Early Adoption:** Limited datasets until more users join.  
- **ML Model Tuning:** Continuous improvement needed to reduce false alerts.  
- **User Experience:** Onboarding and help documentation require refinement.

---

## Applications

### Budget-Friendly Cyber Defense
- Ideal for startups, SMEs, and NGOs lacking enterprise-grade security tools.

### Academic & Research Datasets
- Supports universities and cybersecurity research institutions worldwide.

### Security Team Collaboration
- Teams can coordinate globally, detect major campaigns, and share urgent updates.

---

## Final Result (MVP)

- **Secure Threat Submission & Search APIs**  
- **Interactive Dashboard** with global analytics  
- **ML-Driven Threat Clustering**  
- **Powered by MariaDB** for scalable, modern data handling  

---

## Future Expansions

- **Mobile-First Reporting & Alerts** for all environments  
- **Advanced AI/ML Models** for unseen threats and automated defense insights  
- **Open-Source Growth:** Encourage contributors to build new feeds, visualizations, and modules  
- **Global Reach:** Multi-language and multi-region MariaDB support  

---

## MariaDB’s Role

- **Central Intelligence Store:** Structured, high-speed threat analytics and sharing.  
- **Scalable Analytics:** Supports rapid queries, schema evolution, and millions of users.  
- **Community Collaboration:** Open access for researchers and developers for custom data exploration.

---

## Impact on the Community

- Democratizes access to critical threat intelligence.  
- Empowers under-resourced organizations with enterprise-level insights.  
- Expands MariaDB’s footprint in cybersecurity and open-source innovation.

---

## MariaDB Community Benefits

- New open datasets and query patterns for AI and academic security research.  
- Increased engagement from developers, security professionals, and students.  
- Positions MariaDB as a **core enabler** of next-generation, data-driven cybersecurity.

