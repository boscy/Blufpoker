# This is the repository for the game 'Blufpoker' for the course Logical Aspects of Multi-Agent Systems.
Website can be found at https://boscy.github.io/Blufpoker/

Ivar Mak (S2506580)   Oscar de Vries (S2713748)   Joost Warmerdam (S2591367)

<img src="https://i.pinimg.com/originals/f5/95/f6/f595f6e121085652d5118eaf3a20e8e1.jpg" class="img-responsive" alt=""> 

## Running Instructions
This program has various dependencies. The dependencies can be installed by running the command:
<br/>```pip3 install -r requirements.txt``` 

Note that Tkinter (for the GUI) is usually pre-installed with Python, otherwise it should be manually installed

Following, the code can be executed with the following command:
<br/>```python main.py``` 

(NOTE, we found that the GUI could have problems initializing when runnnng by pressing the 'run' button inside an environment such as PyCharm. Executing from terminal by ```python main.py```  did not cause this problem)

The GUI updates by pressing [Enter] in the terminal. To ensure every visualization can be seen, it is suggested to place the GUI next to the terminal (or on another screen).


##  Installing a Virtual Environment
Run the following commands in sequence (in linux add ```sudo```):
<br/>```pip3 install virtualenv```
<br/>```virtualenv venv```
<br/>```source venv/bin/activate```
<br/>```pip3 install -r requirements.txt```


