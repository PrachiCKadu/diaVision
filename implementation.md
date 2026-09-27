# Diabetic Eye Disease Classification — Implementation Handoff

## 1. Project Title

**Automated Classification of Diabetic Eye Diseases Using an Optimized Deep Convolutional Model**

---

## 2. Project Goal

Build an AI-assisted web application that accepts a retinal fundus image and automatically classifies it into one of five diabetic retinopathy severity levels.

The system will:

1. Accept retinal fundus image.
2. Validate the image.
3. Preprocess the image.
4. Pass it through a trained deep-learning model.
5. Classify it into one of five classes.
6. Return disease name, severity and confidence.
7. Generate a Grad-CAM heatmap for explainability.
8. Store prediction history.
9. Generate a report.
10. Allow doctor review.

The system is an **AI-assisted screening/decision-support system**, not a replacement for professional ophthalmological diagnosis.

---

# 3. Five Classification Classes

The model will perform **5-class classification**:

| Label | Class                              |
| ----- | ---------------------------------- |
| 0     | No Diabetic Retinopathy            |
| 1     | Mild Diabetic Retinopathy          |
| 2     | Moderate Diabetic Retinopathy      |
| 3     | Severe Diabetic Retinopathy        |
| 4     | Proliferative Diabetic Retinopathy |

These labels correspond to the APTOS 2019 DR grading scheme.

---

# 4. Planned Dataset

## Primary Dataset

**APTOS 2019 Blindness Detection**

Source:

Kaggle APTOS 2019 Blindness Detection dataset.

Approximate labelled images:

**3,662**

Original class distribution is imbalanced:

* Class 0 ≈ 1,805
* Class 1 ≈ 370
* Class 2 ≈ 999
* Class 3 ≈ 193
* Class 4 ≈ 295

We will use the original dataset rather than relying on an already-resized 224×224 version.

---

# 5. Planned ML Approach

## Baseline

**ResNet50**

Purpose:

Establish baseline performance.

## Main Candidate / Proposed Model

**EfficientNet-B3**

Purpose:

Build the optimized deep convolutional model.

The final model will be selected based on actual experimental results rather than assuming EfficientNet is automatically superior.

---

# 6. Planned Preprocessing

Pipeline:

```text
Original Fundus Image
        ↓
Image Quality Check
        ↓
Remove unnecessary black borders
        ↓
Crop retinal region
        ↓
Resize
        ↓
Contrast Enhancement
        ↓
Normalization
        ↓
Model Input
```

Initial model input:

**224 × 224 × 3**

Possible enhancement:

**CLAHE** for contrast improvement.

CLAHE will be experimentally evaluated rather than automatically assumed to improve performance.

---

# 7. Planned Data Augmentation

Training data may use:

* Horizontal flip
* Small rotation
* Small zoom
* Mild brightness variation
* Mild contrast variation
* Small translation

Validation and test data:

**No random augmentation.**

---

# 8. Class Imbalance Strategy

APTOS is significantly imbalanced.

Planned solutions:

* Stratified train/validation/test split
* Class-weighted loss
* Appropriate augmentation
* Per-class Precision/Recall/F1
* Confusion Matrix
* Quadratic Weighted Kappa (QWK)

Accuracy will NOT be the only evaluation metric.

---

# 9. Planned Dataset Split

Initial planned split:

```text
70% → Training
15% → Validation
15% → Test
```

The split must be **stratified** so that all five classes are represented proportionally.

The test set must remain untouched until final evaluation.

---

# 10. Planned Training Experiments

## Experiment 1

Basic CNN / baseline.

Purpose:

Establish a simple reference.

## Experiment 2

ResNet50 with transfer learning.

## Experiment 3

EfficientNet-B3 with transfer learning.

## Experiment 4

EfficientNet-B3 + preprocessing improvements.

## Experiment 5

EfficientNet-B3 + augmentation + class weighting.

## Experiment 6

Fine-tuned EfficientNet-B3 + optimized hyperparameters.

Final model will be selected based on validation performance.

---

# 11. Transfer Learning Strategy

Initially use pretrained ImageNet weights.

Training:

```text
Pretrained Backbone
       ↓
Freeze Backbone
       ↓
Train Classification Head
       ↓
Unfreeze Selected Upper Layers
       ↓
Fine-Tune With Low Learning Rate
```

Possible starting values:

* Initial learning rate ≈ 1e-3 for classification head
* Fine-tuning learning rate ≈ 1e-5

These are starting values only and must be tuned experimentally.

---

# 12. Planned Model Architecture

Conceptual EfficientNet-B3 architecture:

```text
Input 224×224×3
       ↓
EfficientNet-B3
       ↓
Global Average Pooling
       ↓
Dense 512
       ↓
ReLU
       ↓
Dropout
       ↓
Dense 256
       ↓
ReLU
       ↓
Dropout
       ↓
Dense 5
       ↓
Softmax
```

Final architecture/hyperparameters can be adjusted during experiments.

---

# 13. Planned Training Controls

Optimizer:

**AdamW or Adam**

Other controls:

* Learning-rate scheduler
* Early stopping
* Model checkpointing
* Best validation model saving

Best model will be saved under:

```text
models/optimized/
```

---

# 14. Evaluation Metrics

Final model evaluation should include:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix
* Quadratic Weighted Kappa (QWK)

Important:

**Do not invent any final performance numbers before model training.**

Results must come from actual experiments.

---

# 15. Explainable AI

Use:

**Grad-CAM**

Purpose:

Show image regions that contributed strongly to the model's prediction.

Pipeline:

```text
Fundus Image
      ↓
EfficientNet-B3
      ↓
Prediction
      ↓
Grad-CAM
      ↓
Heatmap
      ↓
Overlay
```

Grad-CAM is an explanation/visualization technique and should not be presented as definitive clinical evidence.

---

# 16. Expected Prediction Output

Conceptual backend response:

```json
{
    "prediction": "Moderate Diabetic Retinopathy",
    "class": 2,
    "confidence": 0.87,
    "severity": "Moderate",
    "heatmap": "path/to/heatmap"
}
```

The actual confidence value will come from the trained model.

---

# 17. Planned Django Architecture

Django will be responsible for:

* Authentication
* Patient management
* Doctor management
* Image upload
* Image validation
* Preprocessing
* Model inference
* Grad-CAM
* Prediction storage
* Report generation
* API endpoints
* Database operations

Frontend will be developed by another team member.

Frontend will communicate with Django through APIs.

---

# 18. Planned Database

Database choice:

**PostgreSQL**

Main entities:

### User

```text
id
name
email
password
role
```

### Patient

```text
patient_id
user_id
age
gender
diabetes_duration
```

### Doctor

```text
doctor_id
user_id
hospital
specialization
```

### EyeImage

```text
image_id
patient_id
image_path
upload_date
```

### Prediction

```text
prediction_id
image_id
disease_class
disease_name
confidence
severity
heatmap_path
created_at
```

### Report

```text
report_id
prediction_id
doctor_id
report_path
created_at
```

---

# 19. Planned Project Folder Structure

Current root structure:

```text
diabetic-eye-detection/
│
├── dataset/
│   ├── metadata/
│   ├── processed/
│   └── raw/
│
├── django_backend/
│
├── ml/
│   ├── training/
│   └── utils/
│
├── models/
│   ├── baseline/
│   └── optimized/
│
├── notebooks/
│
└── results/
    ├── confusion_matrix/
    ├── gradcam/
    ├── reports/
    └── training_curves/
```

This structure has already been successfully created.

---

# 20. Current Environment — COMPLETED

Project directory:

```text
C:\Users\HP\Desktop\Projects\Python Projects\diabetic-eye-detection
```

Virtual environment:

```text
.venv
```

Virtual environment is active.

Terminal currently shows:

```text
(.venv) PS C:\Users\HP\Desktop\Projects\Python Projects\diabetic-eye-detection>
```

---

# 21. Python Version — COMPLETED

```text
Python 3.13.7
```

pip:

```text
pip 25.2
```

---

# 22. Installed Packages — COMPLETED

### Deep Learning

```text
TensorFlow 2.21.0
```

TensorFlow import successfully tested.

Command:

```powershell
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
```

Output:

```text
TensorFlow: 2.21.0
```

---

### Backend

```text
Django 6.1
Django REST Framework 3.18.0
psycopg2-binary 2.9.12
```

Django successfully tested.

Output:

```text
Django: 6.1
```

---

### ML/Data packages

Successfully imported:

```text
OpenCV
NumPy
Pandas
Scikit-learn
```

Verification output:

```text
ML packages: OK
```

---

### Jupyter

Installed:

```text
Jupyter
JupyterLab
Notebook
IPykernel
```

Installation completed successfully.

---

# 23. CURRENT PROJECT STATUS

## Completed

* [x] Main project folder created
* [x] `dataset/` created
* [x] `ml/` created
* [x] `models/` created
* [x] `notebooks/` created
* [x] `results/` created
* [x] `django_backend/` created
* [x] Dataset subfolders created
* [x] ML subfolders created
* [x] Model folders created
* [x] Results folders created
* [x] Python virtual environment created
* [x] Virtual environment activated
* [x] Python 3.13.7 verified
* [x] pip 25.2 verified
* [x] TensorFlow 2.21.0 installed and working
* [x] Django 6.1 installed and working
* [x] Django REST Framework installed
* [x] PostgreSQL Python driver installed
* [x] OpenCV working
* [x] NumPy working
* [x] Pandas working
* [x] Scikit-learn working
* [x] Jupyter installed

---

# 24. NOT YET DONE

Do NOT assume these are completed:

* [ ] `requirements.txt`
* [ ] Git repository
* [ ] Jupyter kernel registration
* [ ] APTOS dataset download
* [ ] Dataset placement
* [ ] Dataset inspection
* [ ] EDA
* [ ] Image preprocessing code
* [ ] Train/validation/test split
* [ ] ResNet50 training
* [ ] EfficientNet-B3 training
* [ ] Optimization experiments
* [ ] Final model selection
* [ ] Model evaluation
* [ ] Confusion matrix
* [ ] QWK evaluation
* [ ] Grad-CAM
* [ ] Saved `.keras` model
* [ ] Django project creation
* [ ] Django apps
* [ ] Database configuration
* [ ] Django models
* [ ] REST APIs
* [ ] Prediction API
* [ ] Report generation
* [ ] Frontend integration
* [ ] Deployment

---

# 25. EXACT NEXT STEP

The next chat should NOT start by recreating the project.

Start from:

> **"Project folder and Python environment are already created. TensorFlow 2.21.0, Django 6.1, Django REST Framework, OpenCV, NumPy, Pandas, Scikit-learn and Jupyter are installed and verified. The folder structure is already complete. Now continue with the next implementation step."**

The logical next implementation steps are:

```text
1. Create requirements.txt
        ↓
2. Register Jupyter kernel
        ↓
3. Verify TensorFlow environment
        ↓
4. Download exact APTOS 2019 dataset
        ↓
5. Place dataset in dataset/raw/
        ↓
6. Inspect train.csv + images
        ↓
7. Create EDA notebook
```

Do not jump directly to Django.

The ML dataset and model should be developed and validated first.
