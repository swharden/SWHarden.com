---
title: Summarizing Blog Posts with AI
description: How I used Python to run the Llama 2 large language model locally and convert my rambling childhood blog posts into concise summaries
Date: 2023-07-31 23:09:00
tags: ["python", "ai"]
---

**This page describes how I used a locally hosted generative AI to read blog posts I made as a child and summarize them using more professional language.** In the early 2000s there was no Twitter, and the equivalent was making short blog posts every few days. Today this website is effectively a technology blog, and although I'm proud to have been blogging for over twenty years, I'm embarrassed enough by some of the content I wrote as a child that I have hundreds of posts hidden. I like the idea of respecting my past by keeping those old posts up in some form, and I hope that generative AI can help me do that using more professional language more consistent with the present tone of this website.

## Background

This article builds upon my previous two articles:

* [Run Llama 2 Locally with Python](https://swharden.com/blog/2023-07-29-ai-chat-locally-with-python/)

* [Using Llama 2 to Answer Questions About Local Documents](https://swharden.com/blog/2023-07-30-ai-document-qa/)

Review the information on those pages for details about setting-up the Python environment required to use large language models and generative AI locally to answer questions about information contained in documents on the local filesystem.

## Code

**The following code uses [LangChain](https://python.langchain.com/) to provide the tools for interpretation and generative AI.** Specifically, the [all-MiniLM-L6-v2 sentence transformer](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) is used to interpret content of the old blog posts and store it in a [FAISS vector database](https://faiss.ai/index.html), then the [Llama 2 large language model](https://ai.meta.com/llama/) is used to answer questions about its content. I am thankful to have kept all of my original blog posts (translated into Markdown format), so processing them individually is not be too complicated:

```py
"""
This script uses AI to interpret old blog posts and generate 
new ones containing one-sentence summaries of their content.
"""

import pathlib
from langchain.document_loaders import DirectoryLoader, TextLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain import PromptTemplate
from langchain.chains import RetrievalQA

def analyze(file: pathlib.Path) -> FAISS:
    """
    Interpret an old blog post in Markdown format
    and return its content as a vector database.
    """
    loader = UnstructuredMarkdownLoader(file)
    data = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                              chunk_overlap=50)
    texts = splitter.split_documents(data)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'})
    return FAISS.from_documents(texts, embeddings)


def build_llm(db: FAISS) -> RetrievalQA:
    """
    Create an AI Chat large language model prepared
    to answer questions about content of the database
    """

    template = """
    Use information from the following blog post to answer questions about its content.
    If you do not know the answer, say that you do not know, and do not try to make up an answer.
    Context: {context}
    Question: {question}
    Only return the helpful answer below and nothing else.
    Helpful answer:
    """

    llm = CTransformers(model='../models/llama-2-7b-chat.ggmlv3.q8_0.bin',
                        model_type='llama',
                        config={'max_new_tokens': 256, 'temperature': 0.01})
    retriever = db.as_retriever(search_kwargs={'k': 2})
    prompt = PromptTemplate(
        template=template,
        input_variables=['context', 'question'])
    return RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=retriever,
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': prompt})

def summarize_article(file: pathlib.Path):
    """
    Summarize the content of an old markdown file and
    save the result in a new markdown file.
    """
    output_file = pathlib.Path("summaries").joinpath(file.name)
    if output_file.exists():
        return
    sw = Stopwatch("Total")
    db = analyze(file)
    qa_llm = build_llm(db)
    output = qa_llm(
        {'query': "What is a one sentence summary of this blog post?"})
    summary = str(output["result"]).strip()
    with open(output_file, 'w') as f:
        f.write(f"{summary}\n\n{sw.elapsed}")
    print(sw)
    print(f"Summary: {summary}")


if __name__ == "__main__":
    files = sorted(list(pathlib.Path("posts").glob("*.md")))
    for i, file in enumerate(files):
        print(f"summarizing {i+1} of {len(files)}")
        summarize_article(file)
```

## Performance

Summarizing 355 blog posts took a little over 6 hours, averaging about one minute each. Interestingly longer articles did not take significantly longer to summarize. The following chart shows the time it took for the [Q8 model](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML#provided-files) to summarize each of the 355 old blog posts.

<a href="https://swharden.com/static/2023/07/31/performance.png">
<img src="https://swharden.com/static/2023/07/31/performance.png" class="my-5">
</a>

Note that I used [ScottPlot.NET](https://ScottPlot.NET) to create this chart using C#.

```cs
// Read data about each post from the log file
string[] lines = File.ReadAllLines("log.tsv");
List<double> logWords = new();
List<double> times = new();
foreach (string line in lines)
{
    string[] strings = line.Split('\t');
    if (strings.Length != 6)
        continue;

    logWords.Add(Math.Log10(double.Parse(strings[3])));
    times.Add(double.Parse(strings[4]));
}

// Plot article length vs processing time
ScottPlot.Plot plot = new(600, 400);
plot.AddScatterPoints(logWords.ToArray(), times.ToArray());
plot.XAxis.MinorLogScale(true);
static string FormatTick(double value) => Math.Pow(10, value).ToString();
plot.XAxis.TickLabelFormat(FormatTick);
plot.SetAxisLimits(1, 4, 25, 100);
plot.Title("AI Blog Post Summary Performance");
plot.XLabel("Article Length (Number of Words)");
plot.YLabel("Processing Time (Seconds)");
plot.SaveFig("performance.png");
```

## Comparing Summaries by Model

**I found it interesting to compare summaries generated by the Q8 model against the smaller Q2_K model.** Model descriptions can be found on the [Hugging Face readme page](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML#provided-files). 

Metric | Larger Model | Smaller Model
---|---|---
Specific Model (Llama 2 7B) | chat.ggmlv3.q8_0 | chat.ggmlv3.q2_K
Model Size on Disk | 7.0 GB |2.8 GB
Mean Response Time | 62.4 ± 1.8 sec | 25.4 ± 0.8 sec

**The smaller model ran in less than half the time and typically produced adequate summaries,** but often the larger model produces summaries which were slightly better and had a little more personality. For this reason I used the larger model to generate all summaries I ended-up using in the end.

Larger Model | Smaller Model
---|---
The author has lost all their hard work and progress on their websites due to technical issues, and they are unsure if they will try to recreate them or keep this page as a reminder of their past efforts.|The author has lost all of their work on their websites, including thousands of lines of code, and is unlikely to try to recreate them. Instead, they will keep this page as a reminder of the time and effort that went into creating their websites.
The author is unsure of what they will do with their website in the future, but they plan to continue adding to it sporadically as a way to keep it updated and active.|The blog post is about the author's plans for their website, including creating a new page or section for it, and using it as an almost blog style format to share information with readers.
The author is trying to create a bootable CD with the original Quake game that supports soundcard and mouse functionality.|The author of the blog post is trying to create a bootable CD with the original Quake game on it that supports soundcards and mice, so that they can play the game at LAN parties without having to worry about setting up the operating system or dealing with any issues related to the game. 
The writer is experiencing hostility from their parents due to their online writing, specifically their weblog, and is finding it difficult to write normally as a result.|The writer is upset that their parents are reading and misinterpreting their blog posts, leading to incorrect assumptions about their intentions.
The writer is worried about something someone said to them and is trying to figure it out by writing it down and hoping to understand it better by morning.|The author is worried about something someone said to them and is trying to figure it out by going to sleep and thinking about it overnight.
The author of the blog post is claiming that someone stole pictures from their website and passed them off as their own, and they got revenge by creating fake pictures of the thief's room and linking to them from their site, causing the thief to use a lot of bandwidth. | The blog post is about someone who found pictures of their room on another person's website, claimed they were their own, and linked to them from their site without permission.

**About 1 in 50 summaries were totally off base.** One of them claimed my blog article described the meaning of a particular music video, and after watching it on YouTube I'm confident that I had never seen the video or heard the song.

**About 1 in 100 summaries lacked sufficient depth** for me to be satisfied with the result (because they were very long and/or very important to me) so I will be doing a paragraph-by-paragraph summarization and manual editing of the result to ensure the spirit of the article is sufficiently captured.

**Overall, this was an impressive amount of work achieved in a single day.** The source material contained almost half a million words in total, and I was able to adequately review all of that content in a single day!

## Amusing Findings From the Past

In the process of reviewing the AI-generated blog post summaries, I found found a few things that made me chuckle:

> November 25, 2003 (Summary): The author of the blog post is discussing how they were unable to find a good way to summarize their own blog posts, despite trying various methods.

Funny how that one came around full circle!

> March 21, 2005 (Summary): I can't believe I'm making so many audioblogs! Download the latest one on the Audioblogs page (a link is on the right side of the page).

The term "Audioblogs" was used before the word "podcast" was popular. I remember recording at least a few episodes, and I'm really disappointed they weren't preserved with the rest of my blog posts. I also found references to "Videoblogs" or "Vlogs", and I remember recording at least two episodes of that, but I think those too have been lost to history.

> June 4, 2005 (Summary): The author of the blog uses WordPress as their blogging engine instead of MovableType, which they previously used but grew to hate due to speed issues.

That one came full circle too! My blog started as a static site, went to a database-driven site, then worked its way all the back to static where it is today. My best guess at the dates of the various technologies is:

* 1997-2001: Static site (editing HTML files)
* 2001-2003: Locally hosted dynamic (classic ASP)
* 2003-2005: MovableType (static site with a PHP editor)
* 2005-2020: Wordpress (PHP with SQL content storage)
* 2020-2023: Flat file website with a [custom](https://swharden.com/blog/2020-09-13-leaving-wordpress/) PHP markdown parser
* 2023-present: Static site (built from Markdown by Hugo using GitHub Actions)

## Conclusion

**Completing this project allowed me to add 325 previously hidden blog posts back onto my website, bringing the total number of posts from 295 to 620!** It took several hours to run the AI tools over my old blog posts and a few of my hours spot-checking the summaries and tweaking them where needed, but overall I'm very satisfied by how how I was able to wield generative AI to assist the transformation of large amounts of text (almost half a million words) in a single day.