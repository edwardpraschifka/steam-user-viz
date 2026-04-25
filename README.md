# Steam Friend Graph Explorer

## Overview

A Python project that uses the Steam Web API to build a graphical map of a user's friendship network (friends, friends-of-friends, and beyond).

## Features

* Fetch Steam friend network data
* Explore networks to configurable depth
* Uses multithreading for faster API requests
* Generates an interactive graph visualization

## Project Structure

```text
steam_project/
├── main.py
├── api.py
├── workers.py
├── graph.py
├── cache/
└── output/
```

## Run

```bash
python main.py --user YOUR_STEAM_ID --depth 2
```
