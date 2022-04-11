---
title: "Diagrams In Blog"
date: 2017-07-21 17:34:12
draft: false
categories:
  - Technology
tags:
  - web
  - blogging
alias:
  - 2017/07/21/diagrams-in-hugo.html
  - 2017/07/21/diagrams-in-blog.html

thumbnail: uml.png
---

I use a text to diagram tool called [PlantUML](https://plantuml.com). It's perfect!
Now, I want to use it with my hugo site, through a short code. So, I I type a
code like below, I should see out like as the image.

<!-- more -->

```markdown
@startuml
A -> B : Hello
A <- B : Hi There!
@enduml
```

**Update**: I spend many hours trying to work this out. Created a firebase function to process posting and converting
and yada yada. But finally gave up on Hugo. Until there is a plugin support in the core, this will be a very challenging
thing.

During my (failed) research, I ran into [Hexo](https://hexo.io) and [PlantUML filter plugin](https://www.npmjs.com/package/hexo-filter-plantuml). I saw a a [WordPress Migration](https://www.npmjs.com/package/hexo-migrator-wordpress) plugin. I decided to give it a go.

In less than 20 minutes, I managed to install hexo, create a project, migrate wordpress items and got plantuml working.


```
        ```plantuml
        @startuml
        A -> B : Hello
        A <- B : Hi There!
        @enduml
        ```
```
{{< puml "sample/Test Sequence.png" >}}

I guess I will have to wait for hugo to mature a bit more. I really liked the speed and simplicity of hugo. But lack of
plugin support in processing really killed it!

**Update**: I am now using a [hexo-local-plantuml](https://www.npmjs.com/package/hexo-local-plantuml) instead. This
generates plantuml files and svg locally. So overall page rendering is fast. Downside, I need to have Java and graphviz
working locally. I have created a working Docker image ([yogendra/blog-toolbox:latest](https://hub.docker.com/yogendra/blog-toolbox))
to help me work around this

**Update**: Trying client side rendering

[uml-diagram]: diagrams-in-blog/uml.png


**Update 11 Apr 2022**: Here is a something new

Hugo introduced support codeblock rendering extension in 0.93.0. Check [here](https://gohugo.io/content-management/diagrams/)

So now a code block like below will generate a diagram. Its based on mermaidjs.

    ```mermaid

    graph TD;
        A-->B;
        A-->C;
        B-->D;
        C-->D;

    ```
```mermaid

graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;

```

** 11 Apr 2022**: Another attempt to PlatUML in Client Side

```
    ```plantuml
    @startuml
    A -> B : Hello
    A <- B : Hi There!
    @enduml
    ```
```

```plantuml
@startuml
A -> B : Hello
A <- B : Hi There!
@enduml
```
