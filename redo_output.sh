#!/bin/bash

python main.py --charInfo="CharacterInfo_Combat.json" --allGear > Combat_AllGear.txt
python main.py --charInfo="CharacterInfo_Combat.json" > Combat_Upgrades.txt
python main.py --charInfo="CharacterInfo_Assassination.json" > Assassination_Upgrades.txt
python main.py --charInfo="CharacterInfo_Assassination.json" --allGear > Assassination_AllGear.txt
