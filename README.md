# learn-jp-with-python

* Sample script for "Learn Japanese🇯🇵 with Python🐍"
* Set up your environment variable for AWS Access Key and DeepL API Key
  * [Managing access keys for IAM users - AWS Identity and Access Management](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
  * [API Key for DeepL's API – DeepL Help Center | How Can We Help You?](https://support.deepl.com/hc/en-us/articles/360020695820-API-Key-for-DeepL-s-API)

```bash
$ cp export.sh.sample export.sh
$ vi export.sh
$ source export.sh
```

* Run sample script

```bash
$ python3.12 -m venv env
$ . env/bin/activate
(env) pip install -r requirements.txt
(env) streamlit run learn_jp.py
```
