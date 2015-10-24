## week5 - task3

### How to run?

1. Open a terminal and type as follows:

		$ cd [your folder]
		$ python dict.py

2. Open another terminal and type:

		# 1. If you want to search a word
		# 	 for example, you want to search the word 'cat'
		
		$ curl localhost:8000/cat

		# ------
		
		# 2. If you want to modify the definition of a word
		#    for example, you want to change the defition of cat 
		#    from 'a cute animal' to 'A kind of cute animal'
		
		$ curl localhost:8000/cat -d 'newDefinition=A kind of cute animal'
