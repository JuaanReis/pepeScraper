# pepeScraper - 4chan scraper  <img src="./assets/4chan-logo.png" style="height: 20px; width: 20px; margin: 0 0 0 5px">

*A complete scraper for 4chan (Now that's fast.)*

pepeScraper is a scraper that uses context for your searches and returns exactly what you want. *(I'm learning how to make an item look cooler than it actually is)*

- Enter keywords, anything you can think of *(just be careful what you search for 👀)*
- Control the results by date and exclude what you don't want to appear.
- Control the search speed of this program *(do not confuse the processing thread with the 4chan thread)*

## Table of contents

- [Installation](#installation)
- [Flags](#flags)
- [Privacy and data storage](#careful-with-nsfw-content)
- [Care](#careful-with-nsfw-content)

## Weird stuff

[![Stars](https://img.shields.io/github/stars/JuaanReis/pepeScraper?style=social)](https://github.com/JuaanReis/pepeScraper) &nbsp;
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/JuaanReis/pepeScraper/pulls) &nbsp;
[![Last Commit](https://img.shields.io/github/last-commit/JuaanReis/pepeScraper)](https://github.com/JuaanReis/pepeScraper/commits/main) &nbsp;
![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)&nbsp;
[![License: GPL](https://img.shields.io/badge/License-GPL-blue.svg)](LICENSE) &nbsp;
[![Play Random Video](https://img.shields.io/badge/pepeScraper-V1-darkred?style=flat-square&logo=youtube)](https://www.youtube.com/watch?v=dQw4w9WgXcQ) &nbsp;
[![Play Random Video](https://img.shields.io/badge/pepeScraper-V2-darkred?style=flat-square&logo=youtube)](https://www.youtube.com/watch?v=QwLvrnlfdNo)

## Installation

If you use Windows, just go to releases and download the latest version and then install the dependencies. *If you want to help and have access to the source code, use the code below.*

```bash
    git clone https://github.com/JuaanReis/pepeScraper.git
    cd ./pepeScraper
    pip install -r requirements.txt
    py main.py --help
```

## Flags

```
    "--key <w>": keywords used as the base for search and scraping. 
    "--date <YYYY/MM/DD>": exact date when the OP post was made.  
    "--before <YYYY/MM/DD>": posts before the given date up to today.  
    "--after <YYYY/MM/DD>": posts after the given date up to today.  
    "--min-replies <n>": minimum number of replies the thread must have.  
    "--max-replies <n>": maximum number of replies the thread can have.  
    "--board <board_name>": name(s) of the board(s) to search.  
    "-T <n>": number of threads that the program will work with (This will change the speed, not the outcome.).  
    "--op-only, -op": only consider the original post (OP).
    "--no-op, -nop": It's the same as above but the opposite.
    "--nsfw, -n": to enable vulgar posts.
    "--nsfw-title, -nt": to enable title vulgar posts.
    "--output, -o": to save the results to a text file (on your computer, just the link).
    "--download_image, -di": download all images from the thread.
    "--log <w>": saves the logs in "pepescraper/src/data/logs"
    "--all-boards, -ab": Show all boards.
    "--proxy, -p <w>": connects to proxy.
    "--title, -t": Apply the search term to the title.
```

## Example

<img src="./assets/1-1-6.png" style="background-align: center">

> I don't even know what this meme means (and fuck you if you do).

## Privacy and Data Storage

PepeScraper does NOT automatically store anything. <br>
it only uses the API and creates a direct link to 4chan. <br>
No logs, no history, no databases, no Facebook copy (maybe you understand). <br>
You have the option to save images of the boards, logs, and output results, but nothing is automatic 
(*unless you choose this option in the configuration file*)

*Everything is stored in RAM and deleted when the program finishes. (That's right, your mom won't find out what you searched for.)*

> Please don't sue me, I don't have the money to pay a lawyer. *(Sometimes there isn't even enough money to buy food.)*

## Careful with NSFW Content

> I'm serious, pornography can destroy your brain, your body, and your family (no matter how many times I write this, you'll ignore it).
'
```bash
    python main.py --keyword "pepe" --date 01/01/2025
```
*This can make your research perhaps safer (I don't know if I programmed this right).*

---
<br>
<samp>"Sometimes, longing for the past is due to a lack of money (or friends).<br>
Do something different from me, leave the house and go live."</samp>