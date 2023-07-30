---
title: Using Llama 2 to Answer Questions About Local Documents
description: How to use open source large language models to ingest information from local files and generate AI responses to questions about their content
Date: 2023-07-30 09:30:00
tags: ["python", "ai"]
---

**This page describes how I use Python to ingest information from documents on my filesystem and run the Llama 2 large language model (LLM) locally to answer questions about their content.** My ultimate goal with this work is to evaluate feasibility of developing an automated system to digest software documentation and serve AI-generated answers to technical questions based on the latest available information.

**Quickstart:** The previous post [_Run Llama 2 Locally with Python_](/blog/2023-07-29-ai-chat-locally-with-python/) describes a simpler strategy to running Llama 2 locally if your goal is to generate AI chat responses to text prompts without ingesting content from local documents.

## Environment Setup

### Download a Llama 2 model in GGML Format

* I'm using [`llama-2-7b-chat.ggmlv3.q8_0.bin`](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q8_0.bin) (7 GB) 

* More models and descriptions are available in the [Hugging Face Readme](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML#provided-files)

The model I'm using (7B Q8 0) is good but heavy, requiring 7 GB disk space and 10 GB ram. Lighter and faster models are available. I recommend trying different models, and if your application can use a simpler model it may result in significantly improved performance.

### Create a Virtual Environment

* Install the latest version of Python from [python.org](https://www.python.org/)

* Create a virtual environment: `python -m venv .venv`

* Activate the virtual environment: `.venv/Scripts/activate`

### Install Required Packages

Altogether we will need the [`langchain`](https://pypi.org/project/langchain/), [`sentence-transformers`](https://pypi.org/project/sentence-transformers/), [`faiss-cpu`](https://pypi.org/project/faiss-cpu/), and [`ctransformers`](https://pypi.org/project/ctransformers/) packages:

```sh
pip install langchain, sentence_transformers, faiss-cpu, ctransformers
```

**Installing these packages requires a C++ compiler.** To get one:

* **Windows:** Install [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/) with the "Desktop development with C++" workload. It is free for individuals an open-source developers. See the [C++ installation guide](https://learn.microsoft.com/en-us/cpp/build/vscpp-step-0-installation) for more information.


* **Linux:** `apt install python3-dev`

* **MacOS:** `brew install python3-dev`

## Prepare Documents for Ingestion

**I created a few plain text files that contain information for testing.** I am careful to be specific enough (and absurd enough) that we can be confident when the AI chat is referencing this material when answering responses about it later.

#### info1.txt
> Scott William Harden is an open-source software developer. He is the primary author of ScottPlot, pyabf, FftSharp, Spectrogram, and several other open-source packages. Scott's favorite color is dark blue despite the fact that he is colorblind. Scott's advocacy for those with color vision deficiency (CVD) leads him to recommend perceptually uniform color maps like Viridis instead of traditional color maps like Spectrum and Jet.

#### info2.txt
> "JupyterGoBoom" is the name of a Python package for creating unmaintainable Jupyter notebooks. It is no longer actively developed and is now considered obsolete because modern software developers have come to realize that Jupyter notebooks grow to become unmaintainable all by themselves.

## Interpreting Content of Local Files

**We can use the MiniLM language model to interpret the content our documents and save that information in a vector database so AI chat has access to it.** The interpreted information is saved to disk in the [FAISS](https://github.com/facebookresearch/faiss) (Facebook AI Similarity Search) file format, a vector database optimized for searching for similarly across large and high dimensional datasets.

```py
"""
This script creates a database of information gathered from local text files.
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

## Prepare an AI That is Aware of Local File Content

**We can now prepare an AI Chat from a LLM pre-loaded with information contained in our documents** and use it to answer questions about their content.

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

# ask the AI chat about information in our local files
prompt = "Who is the author of FftSharp? What is their favorite color?"
output = qa_llm({'query': prompt})
print(output["result"])
```

## Results

Here are the answers the script above gave me the the following questions:

**Question:** _Who is the author of FftSharp? What is their favorite color?_

**Response:** _Scott William Harden is the author of FftSharp. According to Scott, his favorite color is dark blue despite being colorblind._

**Question:** _Why is JupyterGoBoom obsolete?_

**Response:** _JupyterGoBoom is considered obsolete because modern software developers have come to realize that Jupyter notebooks become unmaintainable all by themselves._

Both answers are consistent with the information written in the ingested text documents. The AI is successfully answering questions about our custom content!

## Jupyter Notebook

Here is a standalone Jupyter notebook that demonstrates how to ingest information from documents and interact with a large language model to have AI chat answer questions about their content. This notebook contains a few extra features to improve formatting of the output as well.

* **View Notebook:** [`llama2-qa.html`](https://swharden.com/static/2023/07/30/llama2-qa.html)

* **Download Notebook:** [`llama2-qa.ipynb`](https://swharden.com/static/2023/07/30/llama2-qa.ipynb.zip)

## Ideas and Future Directions

**The recent availability of open source large language models that can be run locally offers many interesting opportunities that were not feasible with cloud-only offerings like ChatGPT.** For example, consider that your application involves large amounts of sensitive data. You can ingest all the documents and ask AI chat specific questions about their content all on a local machine. This permits development of AI tools that can safely interact with high security operations requiring intellectual property protection, handling of medical data, and other sensitive applications where information security is paramount.

**As a maintainer of several open-source projects, I am curious to learn if this strategy may be useful for generating automated responses to questions posted in GitHub issues that have answers which already exist in the software documentation.** It would be interesting to incorporate AI content ingestion into the CI/CD pipeline of my software projects so that each software release would be paired with an AI chat bot that provides answers to technical questions with version-specific guidance based upon the documentation generated during that same build workflow. I am also curious about the effectiveness of pairing ingested documentation with GitHub Issues and Discussions so that responses to user questions can point to recommended threads where human conversation may be useful.

There are many avenues to explore from here, and I'm thankful for all of the developers and engineering teams that provide these models and tools for anyone to experiment with.

## Resources

* Meta: [Introducing Llama 2](https://ai.meta.com/llama/)

* Hugging Face: [Vigogne 2 13B Instruct - GGML](https://huggingface.co/TheBloke/Vigogne-2-13B-Instruct-GGML)

* OUseful.Info Blog: [Using langchain To Run Queries Against GPT4All in the Context of a Single Documentary Knowledge Source](https://blog.ouseful.info/2023/04/04/langchain-query-gpt4all-against-knowledge-source/)

* Pinecone: [Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/)

* GitHub: [Intuition for selecting optimal `chunk_size` and `chunk_overlap` for `RecursiveCharacterTextSplitter`](https://github.com/langchain-ai/langchain/issues/2026) (langchain-ai issue #206)

* Facebook: [Faiss: A library for efficient similarity search](https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/) 

* LangChain Documentation: [Document Loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders)

* LangChain Documentation: [Split by tokens](https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/split_by_token)

* dev.to: [What Chunk Size and Chunk Overlap Should You Use?](https://dev.to/peterabel/what-chunk-size-and-chunk-overlap-should-you-use-4338)

* Medium (paywall): [Running Llama 2 on CPU Inference Locally for Document Q&A](https://towardsdatascience.com/running-llama-2-on-cpu-inference-for-document-q-a-3d636037a3d8)

* Medium (paywall): [All you need to know about LangChain in 7 Minutes](https://medium.com/@meta_heuristic/all-you-need-to-know-about-langchain-in-7-minutes-bdd486487a79)
