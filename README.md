# Telegram Statistics
This word cloud is generated exclusively for Persian language.

It takes care of Non persian or strange characters and the most stop words in the Text preprocessing stage.

## How to Run
First, install the [required libraries](https://github.com/yasamangs/world-cloud-generater/blob/main/requirements.txt), using pip install.


Then, go to the repo directory in your terminal, run the following code to add `src` to your `PYTHONPATH`.

```
export PYTHONPATH=${PWD} 
```
Then run

```
python src/chat_statistics/chat_stat.py
```

to generate a word cloud of json data in `Data_dir`


