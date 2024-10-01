---
tech: ["python", "makefile"]
libs: ["questionary"]
tools: ["vscode", "ruff", "pytest"]
---

# Unifying browser bookmark exports

## TL;DR

I built an extendable browser-bookmark parser CLI tool using Python and DDD. The tool takes existing bookmarks and bookmark folders from a given browser and outputs a simple and unified notation of the bookmark tree in JSON regardless of the input format. The tool also supports whitelisting to only extract approved bookmarks.

## Introduction

When people come up to me and ask me if I have any resources to a certain topic, more often than not I will provide them with a number of useful websites from my browser bookmarks. However, this process tends to come with a few inconveniences.

Firstly, the process of copying the bookmarks one by one into a chat message is somewhat tedious and I would like to streamline this process. Additionally, unless the person I shared the bookmarks with goes out of their way to save them somewhere for later use, they will most likely message me again when they are trying to remember the website names, creating redundancy on my end.

## Idea

To eliminate the inconveniences mentioned above I want to create a static website which makes all my accumulated bookmarks easily accessible and traversable. With such a platform, I would ideally only need to share one link which will contain all the relevant bookmarks to a certain topic. Finding said link again when needed is also a lot easier than individually reexporting selected bookmarks. Finally, as an additional benefit, such a site also provides the possibility for my peers to explore my bookmarks collection by themselves, potentially allowing for new ideas and insights. However, before I can start building such a website I first need a consistent data source I can retrieve my current bookmarks from.

My first idea to achieve this was to version the proprietary bookmark export of my browser (currently I am using [Brave](https://brave.com/)), but the landscape of internet browsers is ever evolving and I do tend to switch my browser from time to time or try out something new. Therefore, if I were to only rely on the export provided by Brave, I will have to refactor my business logic parsing bookmarks every time I change to a browser with a different export format. To contest this, I want to add an additional layer of abstraction by creating a tool which can be extended to accept any browser bookmark export and output a very simple and unified bookmark tree in JSON.

## Requirements

Since I want to be able to use this tool during the build CD-pipeline of my website later on, implementing this tool to be accessible by the CLI was a given. In addition to this, I usually do not want to export all of my existing bookmarks, since they include bookmarks that I would like to stay private, such as a number of work-related URLs for example. Therefore, I want to be able to exempt certain bookmarks from being exported and since the number of bookmarks I approve to be exported is usually in the minority. Using a whitelist for this cause seems appropriate. As previously mentioned, the main purpose of this tool is to return a unified JSON for any given browser bookmarks export, an example of this resulting notation would look like the following:

```json
{
    "created": "2024-09-23T13:31:10.312132",
    "bookmarks": [
        {
            "name": "Root level bookmark",
            "url": "https://bookmark.com"
        },
        {
            "name": "Root level folder",
            "children": [
                {
                    "name": "1. level deep bookmark",
                    "url": "https://bookmark.com"
                },
                
            ]
        }
    ]
}
```

In this notation the ISO time of creation in the `created` field allows the for easy assessment of the topicality of the current export. The `bookmarks` field contains the actual data of the export. In it, folders can be easily distinguished by checking if they contain the `children` attribute and bookmarks by looking for the `url` field.

### Usage

The usage of this tool should be as easy as possible for someone using it for the first time but also allow fast usage when necessary. Therefore when ran with no CLI flags, the tool should go through a number of prompts to retrieve any necessary inputs. However, the tool should also be able to accept all of these inputs via CLI flags.

## Implementation

Since maintainability is one of the primary non-functional requirements and I (or other users of the tool) will most likely want to extend the it to support additional browsers, I opted to use [Domain Driven Design](https://en.wikipedia.org/wiki/Domain-driven_design) to set up the project structure. Additionally, I will also do my best to adhere to the [SOLID](https://en.wikipedia.org/wiki/SOLID) principles, mainly by making everything that will probably be extended in the future based on interfaces, these can then be implemented on a per browser basis. A simplified project file structure will look like this:

```text
application/
└── services/
    └── WriterService.py
domain/
├── entities/
│   ├── Bookmark.py
│   ├── Folder.py
│   └── Whitelist.py
├── interfaces/
│   └── JSONable.py
└── repositories/
    ├── IBookmarkRepo.py
    └── IWhitelistRepo.py
presentation/
└── cli.py
infrastructure/
└── persistence/
    └── adapters/
        ├── bookmark/
        │   └── BraveBookmarkRepo.py
        └── whitelist/
            └── FSWhitelistRepo.py
```

The `domain` directory contains all entities required in the context of this project as well as all necessary repository interfaces used to retrieve these entities. Various adapters for these repository interfaces can then be implemented in the `infrastructure/persistence/adapters` directory. The `application` directory provides the WriterService which uses parts of the domain and infrastructure layer to build the final JSON output string. Lastly we have the `presentation` directory which houses everything necessary for a user to interact with our project. Since we only provide a CLI interface, we only have a single implementation here.

Another benefit of splitting or code like this is that is also greatly facilitates creating unit tests for the individual components of our application. To run these test, I utilized the [`pytest`](https://pytest.org/) testing framework.

Implementing the aspect of interactivity was on the one hand done with the help of the questionary library, to prompt the user with questions concerning how they want to use the tool, and the native argparse library, to process any passed CLI flags.

Finally, there is the aspect of whitelisting bookmarks. Fortunately, [cpburnz](https://github.com/cpburnz) has already done an amazing job implementing a gitignore-esque whitelisting library for filepaths named [`pathspec`](https://github.com/cpburnz/python-pathspec). Since we are also dealing with a directory-tree we will have no problems using this library as long as we keep track of the *path* of each bookmark and bookmark folder.

## Try it out

After implementation the only thing left to do is to make it publicly available. For this, I have set up a CD pipeline to automatically publish the script to [PyPi](https://pypi.org/) (Python package repository) whenever a new release and tag are created in the GitHub repository. The creation of these releases and corresponding changelog is automatically handled by the [release-please](https://github.com/googleapis/release-please) GitHub action.

After all these pipelines have run `bkmks` can then be installed via [pip](https://pypi.org/project/pip/):

```shell
pip install bkmks
```

You can run it by just calling it in the console:

```shell
bkmks
```
