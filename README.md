# Bot Car

## Privacy

As any discord bot functions, this bot will process every message internally, however none of these messages are logged. When a user direct messages or uses the command, their discord name and uid are sent — which is already public information — into a cached file. This is necessary to keep track of everyone's car lists. Any provider of this bot will also be able to see the list of all cars any given person has.

## Setup

1. Download and extract the full source code, or clone the repository:

```
git clone https://github.com/Emik03/BotCar.git
```

2. Include a .env file containing the private key of your discord bot in the same directory as `bot.py`.

3. Go into `edit.py` and edit the constants `DEFAULT` (the embed to post in the event of no cars), `VIDEO_DIRECTORY` (directory of all videos), and `IMAGE_DIRECTORY` (directory of all images) accordingly.

4. Run this command. The program will initialize and create a `user_data.json` file. When a command is queried, `frequency_data.json` and `name_data.json` will be created.

```
python bot.py
```

A linter is used to determine on startup if duplicate or illegal cars exist in `user_data.json`.

## Usage

The bot uses the syntax 🚗 (`:red_car:`) or 🚙 (`:blue_car:`) at the start of a message. Anything afterwards is called the **Query**.

- If the **Query** is empty, leaderboards are shown displaying the top 5 people with the most amount of cars.

- Otherwise, the **Query** is treated as a [`Regular Expression`](https://docs.python.org/3/library/re.html). The accuracy (%) car tells the **Query** result.

  - If the **Query** becomes empty, it posts the embed `DEFAULT`.

  - Otherwise, if the **Query** matches no car, the rightmost character is discarded until any match is found.

  - Otherwise, a random car of the set that match the **Query** is posted. The bot also states whether it is the first time the user has seen this car.

    - If the car hasn't been seen by the user ever, the car list increases for said user. This applies globally, meaning cars obtained in one server transfer over any other.

    - Otherwise, the embed will still posted but no increment is performed.
