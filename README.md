# MNDatus
A microservice suite for strengthening the world of software documentation and
becoming a prolific open source contributer in the process.

Python 3, Flask, Docker, bash

## Components
MNDatus operates as a suite of Dockerized applications.
### Orchestrator

### Inspector

### Finder

## Report Format

```json
{
  "metadata": {
    "repo_url": string,                 # URL of the associated git repo
    "created": integer,                 # Linux epoch timestamp as integer
    "version": string,                  # Version of MNDatus Inspector
    "status": string,                   # enum("closed", "new", "open")
    "last_viewed": integer              # Linux epoch timestamp as integer
  },
  "data": {
    "summary": {
      "count_typos": integer,           # Number of typos found
      "typos": list[tuple[]],           # List of (typo, correction) tuples
      "count_bad_links": integer,       # Number of links found with non-2XX status
      "bad_links": list[tuple[]],       # List of (URL, status code) tuples
    },
    "details": {
      $document1: {                     # 
        "typos": [],                    #
        "bad_links": []                 #
      },
      $document2: {},
      $document3: {},
      ...
    }
  }
}
```