---
title: How to Run Llama 2 Locally with Python
description: How to use an open source large language model to answer questions about the content of local files using Python.
Date: 2023-07-29 18:30:00
tags: ["python", "ai"]
---

**The Llama 2 large language model was recently released, allowing users to engage in AI chat locally.** This page describes how to use the Llama 2 large language model (LLM) locally, without requiring internet, registration, or API keys. First we explore how to deliver prompts to the raw model and get AI-generated chat responses using only the [llama-cpp-python](https://pypi.org/project/llama-cpp-python/) package. Then we use the more extensive [langchain](https://pypi.org/project/langchain/) package to ingest information from documents so the language model can answer questions about their content. My ultimate goal with this work is to evaluate feasibility of developing an automated system to digest software documentation and serve AI-generated answers to technical questions based on the latest available information.

## TLDR

Jupyter Notebooks that demonstrate these concepts:

* LLama 2 Quickstart: [view online](https://swharden.com/static/2023/07/30/llama2-quickstart.html) or [download](https://swharden.com/static/2023/07/30/llama2-quickstart.ipynb)

* LLama 2 Document Ingestion and QA: [view online](https://swharden.com/static/2023/07/30/llama2-qa.html) or [download](https://swharden.com/static/2023/07/30/llama2-qa.ipynb)
  
## Quickstart

The following steps are a minimal complexity method for running the Llama 2 model locally to generate a AI chat responses to a user-provided prompts.

### Step 1: Download a Large Language Model
The Llama 2 model can be downloaded in [GGML format](https://github.com/ggerganov/ggml) from HuggingFace:

* Model I'm using: [`llama-2-7b-chat.ggmlv3.q8_0.bin`](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q8_0.bin) (7 GB)

* All models: [Llama-2-7B-Chat-GGML/tree/main](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main)

* Model descriptions: [Readme](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML#provided-files)

The model I'm using here is the largest and slowest one currently available. It is 7 GB in size and requires 10 GB of ram to run. Developers should experiment with different models, as simpler models may run faster and produce similar results for less complex tasks.

### Step 2: Install a C++ compiler

Some of the Python packages we will use require a C++ compiler to be installed on the system. Windows users can get what they need by installing Visual Studio with the C++ workload. 

* Download: [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/)
  * It is free for individuals an open-source developers
  * During setup install the "Desktop development with C++" workload ([tutorial](https://learn.microsoft.com/en-us/cpp/build/vscpp-step-0-installation))

### Step 3: Setup the Python Environment

* Install the latest version of Python from [python.org](https://www.python.org/)

* Create a virtual environment: `python -m venv .venv`

* Activate the virtual environment: `.venv/Scripts/activate`

* Install the [`llama-cpp-python`](https://pypi.org/project/llama-cpp-python/) package: `pip install llama-cpp-python`

### Step 4: Interact with the Llama 2 model in Python

Create a new python script and run it inside the virtual environment:

```py
# load the model
from llama_cpp import Llama
LLM = Llama(model_path="./llama-2-7b-chat.ggmlv3.q8_0.bin")

# create a text prompt
prompt = "Q: What are the names of the days of the week? A:"

# generate a response (takes several seconds)
output = LLM(prompt)

# display the response
print(output["choices"][0]["text"])
```

It took my system about 7 seconds to generate the following response:

```
Q: What are the names of the days of the week? 

A: The names of the days of the week, in order, are: 
   Monday Tuesday Wednesday Thursday Friday Saturday Sunday
```

## AI Responses About Content in Local Documents

The quickstart above produces AI-generated responses to prompts using the downloaded large language model, but content of the responses is limited to what information the model was trained with. What if we want to give our language model custom information then have it be able to answer questions about it? **This section explores how to have the AI "read" local documents** so it can answer questions about their content using AI chat.

### Setup the Environment

Altogether we will need the [`langchain`](https://pypi.org/project/langchain/), [`sentence-transformers`](https://pypi.org/project/sentence-transformers/), [`faiss-cpu`](https://pypi.org/project/faiss-cpu/), and [`ctransformers`](https://pypi.org/project/ctransformers/) packages, so let's install them now. Be sure you're using the activated virtual environment described above.

```sh
pip install langchain, sentence_transformers, faiss-cpu, ctransformers
```

### Example Information Files

To test these concepts I will create a few plain text files that contain example information. I am careful to be specific enough (and absurd enough) that we can be confident the AI chat is indeed referencing this material when providing responses to prompts later.

#### info1.txt
```
Scott William Harden is an open-source software developer.
He is the primary author of ScottPlot, pyabf, FftSharp, 
Spectrogram, and several other open-source packages.
Scott's favorite color is dark blue despite the fact 
that he is colorblind. Scott's advocacy for those 
with color vision deficiency (CVD) leads him to recommend 
perceptually uniform color maps like Viridis instead of 
traditional color maps like Spectrum and Jet.
```

#### info2.txt
```
"JupyterGoBoom" is the name of a Python package for 
creating unmaintainable Jupyter notebooks. 
It is no longer actively developed and is now 
considered obsolete because modern software developers 
have come to realize that Jupyter notebooks grow
to become unmaintainable all by themselves.
```

### Interpreting Content of Local Files

**We can use the MiniLM model to interpret the content our information files and save that information to a local file.** The interpreted information is saved to disk in the [FAISS](https://github.com/facebookresearch/faiss) (Facebook AI Similarity Search) file format, a vector database optimized for searching for similarly across large and high dimensional datasets.

```py
"""
This script creates a database of information from local text files.
"""

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# define what documents to load
loader = DirectoryLoader("./", glob="*.txt", loader_cls=TextLoader)

# interpret information in the documents
documents = loader.load()
splitter = RecursiveCharacterTextSplitter()
texts = splitter.split_documents(documents)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'})

# create and save the local database
db = FAISS.from_documents(texts, embeddings)
db.save_local("faiss")
```

Users may desire to customize arguments of the various methods listed here to improve behavior in application-specific ways. For example, `RecursiveCharacterTextSplitter()` has optional keyword arguments for `chunk_size` and `chunk_overlap` which are often customized to best suit the type of content being ingested. See [Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/), [What Chunk Size and Chunk Overlap Should You Use?](https://dev.to/peterabel/what-chunk-size-and-chunk-overlap-should-you-use-4338) and the [LangChain documentation](https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/split_by_token) for more information.

LangChain has advanced tools available for ingesting information in complex file formats like PDF, Markdown, HTML, and JSON. Plain text files are used in this example to keep things simple, but more information is available in the [official documentation](https://python.langchain.com/docs/modules/data_connection/document_loaders).

### Prepare an AI That is Aware of Local File Content

Now that a large language model is downloaded and the content of our local files has been interpreted, let's pre-load the LLM with this information so it can retrieve this information when answering questions about our custom content.

```py
"""
This script reads the database of information from local text files
and uses a large language model to answer questions about their content.
"""

from langchain.llms import CTransformers
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain import PromptTemplate
from langchain.chains import RetrievalQA

# prepare the template we will use when prompting the AI
template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Context: {context}
Question: {question}
Only return the helpful answer below and nothing else.
Helpful answer:
"""

# load the language model
llm = CTransformers(model='./llama-2-7b-chat.ggmlv3.q8_0.bin',
                    model_type='llama',
                    config={'max_new_tokens': 256, 'temperature': 0.01})

# load the interpreted information from the local database
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'})
db = FAISS.load_local("faiss", embeddings)

# prepare a version of the llm pre-loaded with the local content
retriever = db.as_retriever(search_kwargs={'k': 2})
prompt = PromptTemplate(
    template=template,
    input_variables=['context', 'question'])
qa_llm = RetrievalQA.from_chain_type(llm=llm,
                                     chain_type='stuff',
                                     retriever=retriever,
                                     return_source_documents=True,
                                     chain_type_kwargs={'prompt': prompt})

# execute ask the AI chat about information in our local files
prompt = "Who is the author of FftSharp? What is their favorite color?"
output = qa_llm({'query': prompt})
print(output["result"])
```

### Results

Here are the answers the script above gave me the the following questions:

**Question:** Who is the author of FftSharp? What is their favorite color?

**Answer:** Scott William Harden is the author of FftSharp. According to Scott, his favorite color is dark blue despite being colorblind.

**Question:** Why is JupyterGoBoom obsolete?

**Answer:** JupyterGoBoom is considered obsolete because modern software developers have come to realize that Jupyter notebooks become unmaintainable all by themselves.

## Generating Longer AI Chat Responses

To get longer responses, remove the response token limit and permit the language model to use a larger number of tokens for context. Here's an example of how to increase the length of responses using the[`llama-cpp-python`](https://pypi.org/project/llama-cpp-python/) package:

```py
from llama_cpp import Llama

# define n_ctx manually to permit larger contexts
LLM = Llama(model_path="./llama-2-7b-chat.ggmlv3.q8_0.bin", n_ctx=2048)

# create a text prompt
prompt = "Q: What are the names of the days of the week? A:"

# setting max_tokens to 0 limits response size to the model context
output = LLM(prompt, max_tokens=0)

# display the response
print(output["choices"][0]["text"])
```

### Example

**Question:** Why are Jupyter notebooks difficult to maintain? 

**Answer:**
> Jupyter notebooks can be challenging to maintain for several reasons: 
> 
> 1. Temporary file system: Jupyter notebooks reside on the user's local disk, which can make them unreliable and difficult to maintain over time. 
> 
> 2. Version control issues: As notebooks are updated frequently, it becomes challenging to keep track of changes and manage different versions of a notebook. This can lead to conflicts when working with others on the same project. 
> 
> 3. Lack of organization: Since Jupyter notebooks are created manually, it's easy to lose track of which files are included in the notebook and how they relate to each other. This makes it challenging to maintain a well-organized structure for large projects with many components. 
> 
> 4. Limited automation: There are limited tools available for automating tasks within Jupyter notebooks, making it more challenging to create reproducible builds or automate the testing process. 
> 
> 5. Security concerns: Since Jupyter notebooks contain sensitive data such as user credentials, personal information, and intellectual property, they must be protected against unauthorized access and breaches. This can further complicate maintenance efforts. 
> 
> 6. Interactive interfaces: Jupyter notebooks are designed for interactive use, which means that any changes to the code or visualizations will affect the interface in real-time. This can make it challenging to maintain a consistent appearance while working on a project. 
> 
> 7. Limited collaboration support: Jupyter notebooks are primarily designed as an individual tool, which limits their ability to accommodate multiple users and their contributions simultaneously. As a result, collaboration becomes more complicated with larger teams. 
> 
> 8. Lack of integration with other tools: Jupyter notebooks do not integrate well with other popular development tools like Git or IDEs (Integrated Development Environments). This can make it difficult to manage multiple projects, keep track of changes, and collaborate effectively with team members. 
> 
> 9. Limited scalability: As projects grow in size and complexity, Jupyter notebooks may become less efficient and more challenging to maintain. This is particularly true for large-scale data science or machine learning projects that require a lot of processing power and memory. 
> 
> 10. Lack of formalized workflows: Since Jupyter notebooks are primarily designed as an interactive environment, they don't provide standardized workflows or processes for managing projects. This can result in a less organized and more challenging maintenance experience for project teams. 
> 
> By understanding these challenges, you can better prepare yourself to manage the complexities of Jupyter notebooks and develop strategies to address them effectively.
> 
> _llama-2-7b-chat.ggmlv3.q2_K.bin generated this response in 76.26 sec_

## Using Llama 2 AI Chat in a Jupyter Notebook

Here are standalone Jupyter notebooks that demonstrate how to use the Llama 2 large language model to generate AI chat responses to plain text prompts. They contain features specific to IPython / Jupyter notebooks which improve the formatting of the output.

#### AI chat quickstart:

  * View: [`llama2-quickstart.html`](https://swharden.com/static/2023/07/30/llama2-quickstart.html)
  * Download: [`llama2-quickstart.ipynb`](https://swharden.com/static/2023/07/30/llama2-quickstart.ipynb)
  
#### AI chat that can Answer questions about documents:
  * View: [`llama2-qa.html`](https://swharden.com/static/2023/07/30/llama2-qa.html)
  * Download: [`llama2-qa.ipynb`](https://swharden.com/static/2023/07/30/llama2-qa.ipynb)


## Ideas and Future Directions

There are so many reasons one may want to run an AI chat locally. For example, consider that your application involves large amounts of sensitive data. You can ingest all the documents and ask AI chat specific questions about their content all on a local machine. This is a fantastic opportunity for high security operations requiring intellectual property protection, handling of medical data, and other sensitive applications where information security is paramount.

As a maintainer of several open-source projects, I am curious to learn if this strategy may be useful for generating automated responses to questions posted in GitHub issues that have answers which already exist in the software documentation. 

It would be interesting to incorporate AI content ingestion into the CI/CD pipeline of my software projects so that each software release would be paired with an AI chat bot that provides answers to technical questions with version-specific guidance based upon the documentation generated during that same build workflow. 

I am also curious about the effectiveness of pairing ingested documentation with GitHub Issues and Discussions so that responses to user questions can point to recommended threads where human conversation may be useful.

There are many avenues to explore from here, and I'm thankful for all of the developers and engineering teams that provide these models and tools for anyone to experiment with.

## Resources
* https://ai.meta.com/llama/
* https://blog.ouseful.info/
* https://towardsdatascience.com/running-llama-2-on-cpu-inference-for-document-q-a-3d636037a3d8
* https://www.pinecone.io/learn/chunking-strategies/
* https://medium.com/@meta_heuristic/all-you-need-to-know-about-langchain-in-7-minutes-bdd486487a79
* https://github.com/langchain-ai/langchain/issues/2026
* https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/
* https://python.langchain.com/docs/modules/data_connection/document_loaders
* https://www.pinecone.io/learn/chunking-strategies/
* https://dev.to/peterabel/what-chunk-size-and-chunk-overlap-should-you-use-4338
* https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/split_by_token
* https://huggingface.co/TheBloke/Vigogne-2-13B-Instruct-GGML