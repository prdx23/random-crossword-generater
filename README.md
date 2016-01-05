# Random Crossword Generator 
This is a Python Flask App that crawls different sites for words and their definitions and then generates an many crosswords as possible in the given time, then displays the best one. 

####To see the output click [Here](https://random-crossword.herokuapp.com)

## How to run :

To run this app on your local machine :

1. Clone this github

2. Activate the virtual environment

      ```sh
      $ . venv/bin/activate
       ```

3. To run the server:

   1. Excecute this command:

      ```sh
      $ uwsgi --http-socket 127.0.0.1:5000 --module app --callable app --enable-threads
      ```
      
   2. now the website can be accessed on 127.0.0.1:5000/
   
4. To run just the crossword script without the server or interface:

    1. open python console :
  
       ```sh
       $ python
       ```
       
    2. run these commands : 
    
       ```python
       >>> from classes import *
       >>> import code as code
       >>> code.main()
       ```

