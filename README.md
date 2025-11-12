# pepeScreper - 4chan scraper  <img src="./assets/4chan-logo.png" style="height: 20px; width: 20px; margin: 0 0 0 5px">

*A complete scraper for 4chan (Now that's fast.)*

pepeScraper is a scraper that uses context for your searches and returns exactly what you want. *(I'm learning how to make an item look cooler than it actually is)*

- Enter keywords, anything you can think of *(just be careful what you search for 👀)*
- Control the results by date and exclude what you don't want to appear.
- Control the search speed of this program *(do not confuse the processing thread with the 4chan thread)*

## Table of contents

- [installation](#installation)
- [care](#beware-of-nfsw-content)

## Weird stuff

[![Stars](https://img.shields.io/github/stars/JuaanReis/pepeScreper?style=social)](https://github.com/JuaanReis/pepeScreper) &nbsp;
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/JuaanReis/pepeScreper/pulls) &nbsp;
[![Last Commit](https://img.shields.io/github/last-commit/JuaanReis/pepeScreper)](https://github.com/JuaanReis/pepeScreper/commits/main) &nbsp;
![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)&nbsp;
[![License: GPL](https://img.shields.io/badge/License-GPL-blue.svg)](LICENSE) &nbsp;
[![Play Random Video](https://img.shields.io/badge/pepeScreper-V1-darkred?style=flat-square&logo=youtube)](https://www.youtube.com/watch?v=dQw4w9WgXcQ) &nbsp;
[![Play Random Video](https://img.shields.io/badge/pepeScreper-V2-darkred?style=flat-square&logo=youtube)](https://www.youtube.com/watch?v=QwLvrnlfdNo)

## installation

If you use Windows, just go to releases and download the latest version and then install the dependencies. *If you want to help and have access to the source code, use the code below.*

```bash
    git clone https://JuaanReis/pepeScreper.git
    pip install -r requirements.txt
```

If you use Linux it will also be the same thing above (but Linux sometimes forces you to use that damn venv) so use the code below.

```bash
    git clone https://github.com/JuaanReis/pepeScreper.git
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
```

## Flags

```
    "--key <w>": keywords used as the base for search and scraping  
    "--thread <n>": 4chan thread where the posts are located  
    "--exclude <w>": keywords to be excluded from the results  
    "--date <YYYY/MM/DD>": exact date when the OP post was made  
    "--before <YYYY/MM/DD>": posts before the given date up to today  
    "--after <YYYY/MM/DD>": posts after the given date up to today  
    "--min-replies <n>": minimum number of replies the thread must have  
    "--max-replies <n>": maximum number of replies the thread can have  
    "--board <board_name>": name(s) of the board(s) to search  
    "-T <n>": number of threads that the program will work with (workers in the ThreadPoolExecutor)  
    "--op-only, -op": only consider the original post (OP)  
    "--no-op, -nop": It's the same as above but the opposite
    "--no-nfsw, -nn": to prohibit vulgar images
```

## Beware of NFSW content

> I'm serious, pornography can destroy your brain, your body, and your family (no matter how many times I write this, you'll ignore it).

```bash
    python main.py --keyword "pepe" --exclude "nsfw" --no-nfsw --date 01-01-1970
```
*This can make your research perhaps safer (I don't know if I programmed this right).*

---
<br>
<a href="https://youtu.be/HWjCStB6k4o?si=C6TMFRuCYLvrzyJH" style="color:white; text-decoration: None; cursor: text">The end?</a>