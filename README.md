# sentiment-gap

## Create and Activate Conda Environment
```
conda env create -f environment.yml
conda activate sentiment-gap
conda install -c conda-forge pytest
```

## Download resources
```
python -m nltk.downloader punkt stopwords wordnet
```
