---
title: Local AI Chat with C#
description: How to run a LLM locally to power AI chat and answer questions about documents
Date: 2024-02-28 21:15:00
tags: ["ai", "csharp"]
featured_image: https://swharden.com/static/2024/02/28/planets.png
---

**This page describes how I use C# to run the LLama2 large language model (LLM) locally to achieve AI chat, including the ability to answer questions about local documents.** I previously described how I [run LLama2 locally using Python](https://swharden.com/blog/2023-07-29-ai-chat-locally-with-python/) (and how I use it to [answer questions about documents](https://swharden.com/blog/2023-07-30-ai-document-qa/)). Although the Python ecosystem is fantastic for end-users who are strong programmers, setting-up the development environment required to run Python scripts can be a challenge. Maintaining Python projects can be cumbersome too, and I received numerous emails over the last several months indicating that the code examples I posted just a few months ago no longer run as expected. Although I intend to go back and update those old Python tutorials to try to keep them current, I was very happy to learn I can achieve similar functionality using the .NET ecosystem. This article shows the free and open-source tools I use to create C# applications that leverage locally-hosted LLMs to provide interactive chat, including searching, summarizing, and answering questions about information in local documents.

## Key Resources

* [LLaMA](https://llama.meta.com/) (Large Language Model Meta AI) is a family of LLMs created by Meta.

* [HuggingFace](https://huggingface.co/) is a website that hosts different versions of LLaMA models, including _quantized_ models which trade accuracy for reduced size, faster processing, and a smaller memory footprint. This project will use models in the GGUF format.

* [llama.cpp](https://github.com/ggerganov/llama.cpp) is an open-source C++ project (maintained by [Georgi Gerganov](https://github.com/ggerganov)) that provides a simple API for interacting with LLMs in a variety of different file formats.

* [LLamaSharp](https://github.com/SciSharp/LLamaSharp) is an open-source project (maintained by [Martin Evans](https://github.com/martindevans) as part of the [SciSharp stack](https://scisharp.github.io/SciSharp/)) which provides a simple .NET interface to llama.cpp, making it easy to interact with LLMs in C# projects. This project evolves alongside the llama.cpp project, incorporating new features and performance enhancements.

* [KernelMemory](https://github.com/microsoft/kernel-memory) is an open-source project (maintained by Microsoft) which acts as a high level AI service that uses LLMs to index documents and retrieve information from them using LLMs.

## TLDR

* [Download a GGUF file from HuggungFace](https://huggingface.co/models?search=gguf). I'll be using `llama-2-7b-chat.Q5_K_M.gguf` (4.67 GB) for many of the examples on this page, but try different models to identify one that has the best balance of size, performance, and accuracy to meet your needs. Note that CodeLLama models are available which are especially knowledgeable about programming.

* Create a new .NET project and add the [`LLamaSharp`](https://www.nuget.org/packages/LLamaSharp) and [`LLamaSharp.Backend.Cpu`](https://www.nuget.org/packages/LLamaSharp.Backend.Cpu) NuGet packages. Although CUDA backend packages support GPU-accelerated processing on some systems, start with the CPU package to avoid confusing hardware-related memory errors.

* For AI chat, use LLamaSharp classes to load the model and start a chat session as outlined below. Additional functionality is demonstrated in the example app available as source code in the [LLamaSharp GitHub repository](https://github.com/SciSharp/LLamaSharp).

* To ingest documents and use AI to search, summarize, or chat about them, also install the [LLamaSharp.kernel-memory](https://www.nuget.org/packages/LLamaSharp.kernel-memory) and [`Microsoft.KernelMemory.Core`](https://www.nuget.org/packages/Microsoft.SemanticKernel.Core/) NuGet packages. Create a `KernelMemoryBuilder` using the `WithLLamaSharpDefaults()` extension method as shown below.

* Examples on this page are available as standalone .NET projects: https://github.com/swharden/Local-LLM-csharp

## AI Chat

To create an interactive AI chat bot that answers user questions:

1. [Download a GGUF file from HuggungFace](https://huggingface.co/models?search=gguf) (I'm using `llama-2-7b-chat.Q5_K_M.gguf`)

2. Create a new .NET console application and add the [`LLamaSharp`](https://www.nuget.org/packages/LLamaSharp) and [`LLamaSharp.Backend.Cpu`](https://www.nuget.org/packages/LLamaSharp.Backend.Cpu) NuGet packages

3. Add the following your code to your main program:

```cs
using LLama.Common;
using LLama;

// Indicate where the GGUF model file is
string modelPath = @"C:\path\to\llama-2-7b-chat.Q5_K_M.gguf";

// Load the model into memory
Console.ForegroundColor = ConsoleColor.DarkGray;
ModelParams modelParams = new(modelPath);
using LLamaWeights weights = LLamaWeights.LoadFromFile(modelParams);

// Setup a chat session
using LLamaContext context = weights.CreateContext(modelParams);
InteractiveExecutor ex = new(context);
ChatSession session = new(ex);
var hideWords = new LLamaTransforms.KeywordTextOutputStreamTransform(["User:", "Bot: "]);
session.WithOutputTransform(hideWords);
InferenceParams infParams = new()
{
    Temperature = 0.6f, // higher values give more "creative" answers
    AntiPrompts = ["User:"]
};

while (true)
{
    // Get a question from the user
    Console.ForegroundColor = ConsoleColor.Green;
    Console.Write("\nQuestion: ");
    string userInput = Console.ReadLine() ?? string.Empty;
    ChatHistory.Message msg = new(AuthorRole.User, "Question: " + userInput);

    // Display answer text as it is being generated
    Console.ForegroundColor = ConsoleColor.Yellow;
    await foreach (string text in session.ChatAsync(msg, infParams))
    {
        Console.Write(text);
    }
}
```

_Note: some lines of code related to styling have been omitted. See the [GitHub repository for this blog post](https://github.com/swharden/Local-LLM-csharp) for full source code._

### Example Output 

A basic question about planets yields a concise response:

<a href='https://swharden.com/static/2024/02/28/planets.png'>
<img src="https://swharden.com/static/2024/02/28/planets.png">
</a>

Chat sessions preserve history, enabling "follow-up" questions where the model uses context from previous discussion:

<a href='https://swharden.com/static/2024/02/28/planets2.png'>
<img src="https://swharden.com/static/2024/02/28/planets2.png">
</a>

## Chat about Documents

To create an AI chat bot that answers user questions about documents:

1. [Download a GGUF file from HuggungFace](https://huggingface.co/models?search=gguf) (I'm using `llama-2-7b-chat.Q5_K_M.gguf`)

2. Create a new .NET console application and add the [`LLamaSharp`](https://www.nuget.org/packages/LLamaSharp) and [`LLamaSharp.Backend.Cpu`](https://www.nuget.org/packages/LLamaSharp.Backend.Cpu) NuGet packages

3. Add the following your code to your main program:

```cs
using LLamaSharp.KernelMemory;
using Microsoft.KernelMemory.Configuration;
using Microsoft.KernelMemory;
using System.Diagnostics;

// Setup the kernel memory with the LLM model
string modelPath = @"C:\path\to\llama-2-7b-chat.Q5_K_M.gguf";
LLama.Common.InferenceParams infParams = new() { AntiPrompts = ["\n\n"] };
LLamaSharpConfig lsConfig = new(modelPath) { DefaultInferenceParams = infParams };
SearchClientConfig searchClientConfig = new() { MaxMatchesCount = 1, AnswerTokens = 100 };
TextPartitioningOptions parseOptions = new() { MaxTokensPerParagraph = 300, MaxTokensPerLine = 100, OverlappingTokens = 30 };
IKernelMemory memory = new KernelMemoryBuilder()
    .WithLLamaSharpDefaults(lsConfig)
    .WithSearchClientConfig(searchClientConfig)
    .With(parseOptions)
    .Build();

// Ingest documents (format is automatically detected from the filename)
string documentFolder = @"C:\path\to\documents";
string[] documentPaths = Directory.GetFiles(documentFolder, "*.txt");
for (int i = 0; i < documentPaths.Length; i++)
{
    await memory.ImportDocumentAsync(documentPaths[i], steps: Constants.PipelineWithoutSummary);
}

// Allow the user to ask questions forever
while (true)
{
    Console.Write("\nQuestion: ");
    string question = Console.ReadLine() ?? string.Empty;
    MemoryAnswer answer = await memory.AskAsync(question);
    Console.WriteLine($"Answer: {answer.Result}");
}
```

_Note: some lines of code related to styling have been omitted. See the [GitHub repository for this blog post](https://github.com/swharden/Local-LLM-csharp) for full source code._

### Example Output

I gave this program a PDF copy of the [About Scott](/about/) page from my website, then asked who Scott is. I think the phrase "skilled computer programmer and electrical engineer" is a bit dramatic, but overall the information returned lines up pretty well!

<a href='https://swharden.com/static/2024/02/28/scott.png'>
<img src="https://swharden.com/static/2024/02/28/scott.png">
</a>

I then provided information about a fictitious Python package as a text file and asked about it. The information I provided is quoted below, and the response to my question about it is pretty good!

> "JupyterGoBoom" is the name of a Python package for creating unmaintainable Jupyter notebooks. It is no longer actively developed and is now considered obsolete because modern software developers have come to realize that Jupyter notebooks grow to become unmaintainable all by themselves.

<a href='https://swharden.com/static/2024/02/28/document-qa.png'>
<img src="https://swharden.com/static/2024/02/28/document-qa.png">
</a>

## Document Ingestion with Local Storage

Users who run the code above to perform document ingestion will find that it takes a long time to ingest large documents (on the oder of minutes), and restarting the program requires reanalyzing those files all over again.

The Kernel Memory package has functionality to allow allows the information gathered from documents to be stored, then re-loaded into memory almost instantly the next time the program is loaded. There are extensions to allow memory to be stored in various cloud engines and databases (Azure AI Search, Elasticsearch, Postgres, SQL Server, etc.), but in this example we will store and retrieve this information using the local filesystem.

To enable local storage of ingested document information for quick retrieval, modify the code example above to include the `WithSimpleFileStorage()` and `WithSimpleVectorDb()` methods when building the kernel memory:

```cs
SimpleFileStorageConfig storageConfig = new()
{
    Directory = "./storage/",
    StorageType = FileSystemTypes.Disk,
};

SimpleVectorDbConfig vectorDbConfig = new()
{
    Directory = "./storage/",
    StorageType = FileSystemTypes.Disk,
};

IKernelMemory memory = new KernelMemoryBuilder()
    .WithSimpleFileStorage(storageConfig) // store information locally
    .WithSimpleVectorDb(vectorDbConfig)   // retrieve information locally
    .WithLLamaSharpDefaults(lsConfig)
    .WithSearchClientConfig(searchClientConfig)
    .With(parseOptions)
    .Build();
```

When the code is run it will be slow to start the first time as it ingests the documents, but once ingested the information will be saved to disk (in the `./storage/` folder) and rapidly loaded into memory the next time the application starts.

## Conclusions

The [LLamaSharp](https://scisharp.github.io/LLamaSharp/) and [Kernel Memory](https://microsoft.github.io/kernel-memory/) packages can be easily combined to create small C# projects which are able to run LLMs locally to enable AI chat functionality, including summarizing and answering questions about documents. Unlike Python-centric strategies that require end users to have development tools installed and maintain system-wide or virtual environments for package management just to run basic scripts, the .NET-centric strategy described here makes it possible to create compiled apps that are simple to distribute and easy to run by non-technical users. Much of the AI/ML documentation and discussion in recent users has been dominated by Python, but I'm thrilled to see C#/.NET tools like these growing in the AI/ML landscape! I'm excited to watch how these projects will continue to evolve in the years to come.

## Resources

* Full code examples from this article are available on GitHub: https://github.com/swharden/Local-LLM-csharp

* [LLamaSharp](https://github.com/SciSharp/LLamaSharp) is an open-source project (maintained by [Martin Evans](https://github.com/martindevans) as part of the [SciSharp stack](https://scisharp.github.io/SciSharp/)) which provides a simple .NET interface to llama.cpp, making it easy to interact with LLMs in C# projects. 

* [KernelMemory](https://github.com/microsoft/kernel-memory) is an open-source project (maintained by Microsoft) which acts as a high level AI service that uses LLMs to index documents and retrieve information from them using LLMs. It seems to be favored over the older Semantic Memory package for many applications.

* [Run Llama 2 Locally with Python](https://swharden.com/blog/2023-07-29-ai-chat-locally-with-python/) - A blog post I made several months ago

* [Using Llama 2 to Answer Questions About Local Documents (Python)](https://swharden.com/blog/2023-07-30-ai-document-qa/) - A blog post I made several months ago

* [HuggingFace](https://huggingface.co/) is a website that hosts different versions of LLaMA models, including quantized models which trade accuracy for reduced size, faster processing, and a smaller memory footprint.

* [llama.cpp](https://github.com/ggerganov/llama.cpp) is an open-source C++ project (maintained by [Georgi Gerganov](https://github.com/ggerganov)) that provides a simple API for interacting with LLMs in a variety of different file formats.

* [Massive Text Embedding Benchmark (MTEB) Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) - Thanks m0nsky from the LLamaSharp Discord for pointing this page out

* [LLaMA on Wikipedia](https://en.wikipedia.org/wiki/LLaMA) has an interesting write-up about the path toward releasing LLama to the public (It was initially leaked via torrents)

* [LLaMA: Open and Efficient Foundation Language Models](https://arxiv.org/abs/2302.13971) (Touvron et al. 2023) is the seminal paper describing the theory behind LLaMA.

* LLamaSharp Discord: View the [LLamaSharp GitHub repo](https://github.com/SciSharp/LLamaSharp) for information about how to join

* KernelMemory Discord: https://aka.ms/KMdiscord