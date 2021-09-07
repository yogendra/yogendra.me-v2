---
title: Kotlin - Baby Steps
date: 2017-09-19 22:49:47
category:
- Technology
- Programming
tags:
- kotlin
thumbnailImage: https://kotlinlang.org/assets/images/open-graph/kotlin_250x250.png
---
I was at [Kotlin SG Meetup](https://www.meetup.com/kotlinsg/events/243293562/) tonight. It had a lot of content. I will post more about that later.

On my way back home (now), I started reading Kotlin website about various features ([here](https://kotlinlang.org/docs/tutorials/)).

<!--more-->
[![Kotlin](https://kotlinlang.org/assets/images/twitter-card/kotlin_800x320.png)](https://kotlinlang.org/)

I was curious about command line usage of Kotlin. How will I complile kotlin classes outside an IDE? How to run this? What about the runtime libraries? etc.

It turns out to be very straight forward. No surprises.

1. Just write your code in a `.kt` file
1. Run kotlin compiler
  a. For Apps, use `-include-runtime` flag
  b. For libraries, **DON'T** include runtime
1. Run app with `java`

## But I want *moar*

I have Kotlin installed via [SDKMAN](https://sdkman.io). So, on the ["Command Line" Tutorial](https://kotlinlang.org/docs/tutorials/command-line.html) page I saw ([here](https://kotlinlang.org/docs/tutorials/command-line.html#using-the-command-line-to-run-scripts)) how to run kotlin as a script. Cool!


Now, I was more curious. I wanted to see if I could do one better. Can I write a script and execute it directly by filename? Lets try. Created a file `list_folders.kts`, as below.

```kotlin list_folders.kts
#!/usr/bin/env kotlinc -script
import java.io.File

val folders = File(args[0]).listFiles { file -> file.isDirectory() }
folders?.forEach { folder -> println(folder) }

```

And, run this.

``` shell
$ chmod a+x ./list_folders.kts
$ ./list_folders.kts .
./kotlin-koans
```

Wow! that worked. Trick is in the first line

``` shell
#!/usr/bin/env kotlinc -script
```

This causes shell the use `kotlinc` interpreter for this script.

