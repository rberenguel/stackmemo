# StackMemo

A simple spaced repetition system for M5Stack Core2 devices and similar devices with an ESP32, some storage and a screen based on the SuperMemo2 algorithm.

## Functionality

Provided a python file `qa.py` with questions and answers as the one provided as an example, this will automatically generate a file `memos.json` with intervals and ease factors for each question, as you answer them.

> **Note**
> _Why a python file and not a json file?_ No particular good reason. I started with python and left it like that, it works.

The UI is very simple:
- *Turn off button*: the button on top left; saves the current SuperMemo weights and powers off the device.
- *Show answer*: only available in questions, of course. Shows the answer and enables right/wrong buttons. Also hides the power button because answers tend to be more verbose than questions.
- *Right/wrong*: only available in answers. Depending on what you pick, it will update the supermemo weights internally. Right uses `q=4.5` (almost perfect, perfect would be 5) and wrong uses `q=2` (quite wrong but not horribly wrong)
- *Question/answer area*: click it to show card information:
    - `n`: number of times you have answered this question.
    - `ef`: ease factor for this question.
    - `i_n`: next "interval".

Questions are shown starting from the smallest interval, but I don't use the Core2 RTC, I just keep showing questions ordered by `i_n`. Hacky: it won't give the full benefits of spaced repetition unless you "stop reviewing". But kind of gets the job done in showing "worse" questions first, which is what I wanted.

## Installing

You need to get some form of micropython with lvgl on your board. In my case, I used this one.

Next, easiest is to install `adafruit-micropython` (see [here](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy)) and execute `make upload DEVICEPATH`, device path will be something like `/dev/...`.

## Some images

...

...

## Algorithm

This thingy uses SuperMemo 2:

   Algorithm SM-2, (C) Copyright SuperMemo World, 1991.

   https://www.supermemo.com
   https://www.supermemo.eu
"
