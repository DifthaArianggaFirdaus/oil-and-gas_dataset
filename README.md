## Setup Environment - Anaconda
```bash
conda create --name main-ds python=3.12
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell / Terminal
```bash
mkdir oil-and-gas_dataset
cd oil-and-gas_dataset
pip install pipenv
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```bash
streamlit run dashboard/dashboard.py
```

## Dataset Source

Dataset yang digunakan dalam proyek ini berasal dari:

- https://www.kaggle.com/datasets/banlevan/oil-and-gas-production-data
