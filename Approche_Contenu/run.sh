#! /bin/bash
(
    echo "Extract features"
    ./extract_features.py
    echo "Create models"
    ./create_models.py
) 