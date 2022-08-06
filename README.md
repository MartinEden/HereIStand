# Here I Stand metadata
[_Here I Stand: Wars of the Reformation 1517-1555](https://boardgamegeek.com/boardgame/242722/here-i-stand-500th-anniversary-edition)_ is a board game about the political and religious conflicts of 16th century Europe.

Various virtual implementations exist; I know of ones for [Vassal](https://vassalengine.org/wiki/Module:Here_I_Stand), [Wargameroom](http://www.wargameroom.com/), and [several for Tabletop Simulator](https://steamcommunity.com/workshop/browse/?appid=286160&searchtext=here+i+stand&childpublishedfileid=0&browsesort=textsearch&section=about).

In working on my own extension to an existing Tabletop Simulator mod, I wanted to create a programmatic model of all the spaces on the board. I was unable to find an existing data set for this that was not tangled up with the details of the other implementations. So I have created my own, available here, and I have endeavoured to make it:

* **Free of error** (by use of automatic validation to catch mistakes I made during manual transcription)
* **Easily consumable by others** (currently in CSV and JSON formats, but let me know if you need something else. Also, it is released under a permissive licence.)

# How to use
## Downloads
* **[spaces.csv](https://github.com/MartinEden/HereIStand/raw/main/spaces.csv)**. A spreadsheet of all the spaces on the board, as well as what type of space they are and who the home power is. Sea zones are included with type "sea".
* **[connections.csv](https://github.com/MartinEden/HereIStand/raw/main/connections.csv)**. A spreadsheet of all the connections between spaces, between ports and sea zones, and between adjacent sea zones.
* **[spaces.json](https://github.com/MartinEden/HereIStand/raw/main/spaces.json)**. A JSON file that contains all the spaces on the board, with associated metadata (space type, home power). Each space contains a list of all outgoing connections, including adjacent sea zones for ports. Also listed as "spaces" are the sea zones.

## Reciprocal connections
All connections on the board are represented twice. If Stirling has a connection to Edinburgh then two entries appear in `connections.csv` (and likewise in the JSON file): one linking Stirling to Edinburgh, and one linking Edinburgh to Stirling.

## Space types
These are 'normal', 'fortress', 'key', 'capital', 'electorate', 'sea'. A normal space is represented as a circle on the game board. Sea zones have type 'sea'. Note that a capital is always a key.

## Home powers
These appear in the files like so:

    england
    protestant
    scotland
    france
    papacy 
    hapsburg
    hapsburg/ottoman
    ottoman
    hungary
    genoa
    venice
    independent
    sea

Sea zones are listed with 'sea' as their home power. Oran and Tripoli are listed as 'hapsburg/ottoman' to show their switching allegiance after the _Barbary Pirates_ even has been played. Algiers is simply listed as 'ottoman', as it is not in play until that event is played, and when it does come into play it is always Ottoman.

## Connection types
These are 'normal', 'pass', 'port', 'sea'. Normal and pass should be self explanatory to anyone familiar with the game. If a space is a port, then a connection is listed with type 'port' linking the space and the sea zone. If a sea zone is adjacent to another this is also listed as a connection, this time with type 'sea'.

# Validation and generation
The CSV files were written by hand.

The python scripts included in this repository show how I validated the CSV files and generated the JSON, and allow others to extend the validation or add more target formats.

To run them yourself, run `process.py`. Learning how to run Python programs is beyond the scope of this README.

## Validation
* Duplication of spaces and connection is checked
* Space types, connection types and home powers are checked to ensure the values are one of the ones listed above. Additionally, I check that only sea zones use the special home power of "sea".
* I check that all the connections refer to spaces that exist in the space list, and that all connections are reciprocal. For reciprocal connections, I additionally check that they are of the same type (so not a normal connection one way and a pass the other).
* I check that connections between land spaces and sea zones are always ports, and that connections between adjacent sea zones are always of type 'sea'.

## Generation
The JSON file is generated with pretty printing on, so it could be compressed substantially.