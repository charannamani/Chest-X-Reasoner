# ChestX-Reasoner

**Multimodal Vision-Language Architecture for Explainable Thoracic Radiograph Interpretation**

ChestX-Reasoner is a multimodal deep learning framework that couples dense visual feature extraction with generative clinical reasoning. The system detects thoracic abnormalities from frontal chest radiographs and synthesizes structured, step-by-step diagnostic rationales using a vision-grounded Small Language Model (SLM).

---

## 🔬 System Architecture

```
                  [ Frontal Chest Radiograph (DICOM / PNG) ]
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │     Image Preprocessing      │
                       │  - Resize (224x224)          │
                       │  - ImageNet Normalization    │
                       └──────────────┬───────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │   DenseNet-121 Vision Spine  │
                       │  - Frozen DenseBlocks 1-3    │
                       │  - Fine-Tuned DenseBlock 4   │
                       │  - 7-Class Linear Classifier │
                       └──────────────┬───────────────┘
                                      │ Multi-Label Sigmoid Probs
                                      ▼
                       ┌──────────────────────────────┐
                       │ Clinical Thresholding (0.5)  │
                       │  - Present Findings Vector   │
                       │  - Absent Findings Vector    │
                       └──────────────┬───────────────┘
                                      │
[ Clinical Query ] ───────────────────┼──────────────────────────────┐
                                      ▼                              │
                       ┌──────────────────────────────┐              │
                       │ Structured Grounding Prompt  │              │
                       └──────────────┬───────────────┘              │
                                      │                              │
                                      ▼                              ▼
                       ┌──────────────────────────────┐    ┌──────────────────┐
                       │ Phi-3 Mini (4k-Instruct SLM) │    │  MongoDB Atlas   │
                       │  - Constrained Decoding      │───▶│  Patient History │
                       │  - Step-by-Step Rationale    │    │  & Audit Logs    │
                       └──────────────┬───────────────┘    └──────────────────┘
                                      │
                                      ▼
                       [ Structured Clinical Output ]
                       - Detected Finding Probabilities
                       - Step-by-Step Pathological Rationale
                       - Diagnostic Conclusion
```

---

## 📋 Clinical Finding Taxonomy

The vision classification head targets 7 high-prevalence thoracic pathologies derived via weakly-supervised NLP labeling of Indiana University (Open-I) radiology reports:

| Class Label        | Associated Clinical Keywords / Radiology Markers                    |
| ------------------ | ------------------------------------------------------------------- |
| `lung_opacity`     | Opacity, opacities, infiltrate, infiltration, airspace disease      |
| `consolidation`    | Consolidation, airspace consolidation                               |
| `pleural_effusion` | Pleural effusion, blunted costophrenic angles, effusions            |
| `cardiomegaly`     | Cardiomegaly, enlarged cardiac silhouette, cardiac enlargement      |
| `atelectasis`      | Subsegmental atelectasis, lung collapse, hypoinflation              |
| `edema`            | Pulmonary edema, interstitial edema, vascular congestion            |
| `support_devices`  | Endotracheal tube, PICC line, pacemaker leads, catheter, chest tube |

---

## 🧠 Methodological Pipeline

### 1. Weakly-Supervised Dataset Annotation

- Extracted and normalized frontal X-ray projections from the Indiana University Chest X-Ray cohort (3,818 studies).
- Applied deterministic clinical entity matching across free-text Findings and Impression sections to generate multi-label ground truth matrices.

### 2. Deep Visual Transfer Learning

- **Backbone:** DenseNet121 initialized with ImageNet weights.
- **Optimization Strategy:**
  - Early convolutional layers frozen to preserve generic low-level spatial features.
  - DenseBlock 4 and the custom 7-output linear head trained end-to-end.
- **Loss Function:** Multi-label `BCEWithLogitsLoss` using Adam optimizer (LR = 1×10⁻⁴, Batch Size = 16).

### 3. Vision-Grounded Language Reasoning (SLM)

- **Language Model:** `microsoft/Phi-3-mini-4k-instruct` (3.8B parameters, FP16 precision).
- **Hallucination Mitigation:** Rather than allowing open-ended text generation, Phi-3 is strictly conditioned on the visual encoder's verified presence/absence vector (≥0.5 probability threshold). Output decoding follows an enforced schema:

  ```
  Visual Findings → Step-by-Step Pathological Reasoning → Definitive Conclusion
  ```

---

## 📂 Repository Structure

```
Chest-X-Reasoner/
├── backend/
│   ├── app.py              # Flask REST API endpoints & Gradio client bridge
│   ├── auth.py             # Bcrypt password hashing & authentication logic
│   └── database.py         # MongoDB Atlas client connection setup
├── frontend/
│   ├── dashboard.html      # Analysis interface, dropzone & history feed
│   ├── login.html          # User authentication portal
│   └── signup.html         # User registration portal
├── notebooks/
│   ├── 01_data_preprocessing.ipynb           # Weakly-supervised report NLP extraction
│   ├── 02_ChestXreasoner_v1_training.ipynb   # DenseNet121 multi-label fine-tuning
│   └── 03_inference_pipeline.ipynb           # Multimodal Phi-3 reasoning integration
├── Screenshots/            # System demonstration visuals
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
└── requirements.txt        # Python dependency manifest
```

---

## 🛠 Tech Stack

| Category                 | Tools                                               |
| ------------------------ | --------------------------------------------------- |
| Deep Learning & CV       | PyTorch, Torchvision, DenseNet121, Pillow           |
| Language Modeling        | Hugging Face Transformers, Microsoft Phi-3 Mini     |
| Backend API & Middleware | Python, Flask, Flask-CORS, Gradio Client            |
| Database & Security      | MongoDB Atlas, PyMongo, Bcrypt                      |
| Frontend UI              | HTML5, CSS3 (Custom Dark Theme), Vanilla JavaScript |

---

## 🚀 Local Setup & Reproduction

### Prerequisites

- Python 3.10+
- MongoDB Atlas cluster connection string

### 1. Clone Repository

```bash
git clone https://github.com/charannamani/Chest-X-Reasoner.git
cd Chest-X-Reasoner
```

### 2. Configure Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
cp .env.example .env
```

Add your MongoDB connection URI inside `.env`:

```
MONGO_URI=your_mongodb_atlas_connection_string_here
```

### 5. Launch Backend Server

```bash
python backend/app.py
```

Open `frontend/login.html` in your browser to access the dashboard.

---

## ⚠️ Disclaimer

This project is a **research prototype** intended for educational and portfolio purposes only. It is **not** a certified diagnostic tool and should not be used for actual clinical decision-making.
