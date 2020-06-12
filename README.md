# Who to follow?

App that analyze people you recently follows and recommend new users to follow.

![](demo.gif)

## How to run

```
pipenv shell
pipenv install
python3 server.py
```

Visit `http://localhost:3000`.

## How it works

The algorithm works by finding the **largest and most recent** following intersections between the people you recently followed.
