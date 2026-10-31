# Data directory

Place the manually supplied IBM Telco Customer Churn CSV in `data/raw/` when
the dataset implementation phase begins. Do not commit private or licensed
customer datasets. Generated/processed data belongs in `data/processed/` and
is ignored by Git as well. Phase 0 does not ingest, profile, preprocess, or
train on data. Dataset workflows should use configurable target and feature
selection so they are not coupled to telecom-specific column names.
