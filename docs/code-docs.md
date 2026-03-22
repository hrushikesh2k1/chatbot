<a id="architecture"></a>

# architecture

<a id="architecture.Diagram"></a>

## Diagram

<a id="architecture.Cluster"></a>

## Cluster

<a id="architecture.Users"></a>

## Users

<a id="architecture.Nginx"></a>

## Nginx

<a id="architecture.Docker"></a>

## Docker

<a id="architecture.Pod"></a>

## Pod

<a id="architecture.Ingress"></a>

## Ingress

<a id="architecture.PV"></a>

## PV

<a id="architecture.MongoDB"></a>

## MongoDB

<a id="architecture.VM"></a>

## VM

<a id="architecture.VirtualNetworks"></a>

## VirtualNetworks

<a id="log_anamoly_detector"></a>

# log\_anamoly\_detector

<a id="log_anamoly_detector.pd"></a>

## pd

<a id="log_anamoly_detector.np"></a>

## np

<a id="log_anamoly_detector.IsolationForest"></a>

## IsolationForest

<a id="log_anamoly_detector.log_file_path"></a>

#### log\_file\_path

Update with your file path if needed

<a id="log_anamoly_detector.data"></a>

#### data

<a id="log_anamoly_detector.df"></a>

#### df

<a id="log_anamoly_detector.level_mapping"></a>

#### level\_mapping

<a id="log_anamoly_detector.model"></a>

#### model

Lower contamination for better accuracy

<a id="log_anamoly_detector.anomalies"></a>

#### anomalies

<a id="app"></a>

# app

<a id="app.Flask"></a>

## Flask

<a id="app.render_template"></a>

## render\_template

<a id="app.request"></a>

## request

<a id="app.jsonify"></a>

## jsonify

<a id="app.MongoClient"></a>

## MongoClient

<a id="app.json"></a>

## json

<a id="app.re"></a>

## re

<a id="app.datetime"></a>

## datetime

<a id="app.random"></a>

## random

<a id="app.load_dotenv"></a>

## load\_dotenv

<a id="app.Swagger"></a>

## Swagger

<a id="app.random"></a>

## random

<a id="app.os"></a>

## os

<a id="app.app"></a>

#### app

<a id="app.swagger"></a>

#### swagger

<a id="app.client"></a>

#### client

<a id="app.db"></a>

#### db

<a id="app.cache_collection"></a>

#### cache\_collection

<a id="app.load_knowledge_base"></a>

#### load\_knowledge\_base

```python
def load_knowledge_base()
```

<a id="app.knowledge_base"></a>

#### knowledge\_base

<a id="app.find_matching_answer"></a>

#### find\_matching\_answer

```python
def find_matching_answer(question)
```

Search for matching keywords in knowledge base

<a id="app.get_cached_response"></a>

#### get\_cached\_response

```python
def get_cached_response(question)
```

Check if response is cached in MongoDB

<a id="app.generate_mock_ai_response"></a>

#### generate\_mock\_ai\_response

```python
def generate_mock_ai_response(question)
```

Generate a mock AI response based on question content (FREE - no API needed)

<a id="app.cache_response"></a>

#### cache\_response

```python
def cache_response(question, answer)
```

Store response in MongoDB cache

<a id="app.index"></a>

#### index

```python
@app.route("/")
def index()
```

<a id="app.health"></a>

#### health

```python
@app.route("/health")
def health()
```

<a id="app.ask"></a>

#### ask

```python
@app.route("/ask", methods=["POST"])
def ask()
```

