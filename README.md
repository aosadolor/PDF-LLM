This model is based on a ChatGPT prompt where I requested the agent to write a LLM with compiled PDF files, with a user interface to input queries into the model.
Anyone that has used ChatGPT for code prompts should understand that you generally have to make significant changes to code, including writing your own functions and callbacks
to get any of it to work. I am particularly proud of this effort because getting it to work required a major amount of debugging and problem solving. It showed me the necesity of 
understanding programming concepts to even make prompt engineering accessible and efficient.

It is a simple model written in python3, that uses Langchains and OpenAI's LLM API libraries. The user interface is written in python3 using the tkinter library.
The pdf file used in the example is a USMC manual on strategy. I chose this particular document because military writing is engaging and to the point, and some of the most inspiring
writing I've read. The idea was to see if my LLM would generate responses like the generals that write these manuals. You be the judge of that. 
