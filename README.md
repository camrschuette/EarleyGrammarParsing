EarleyGrammarParsing
====================

Using a file of strings and a grammar specification file as input, determine if the string is correct with the grammar

The program takes in the grammar file first and reads it in and converts the terminals into a list and the nonterminals into a dictionary. The terminals need to be in a list so that they are in order when going through a tokenizing. I use regular expressions to find the terminals and nonterminals.

I use a 2D list of sets to hold the information. The program only needs to work with one column at a time, making it easier to compute and move on to the next column until complete.

I use three helper functions to complete the parsing:
  1. Scan - have matched an input token so we accept and consume it
  2. Predict - guess the next nonterminal the parser will take
  3. Complete - at the end of a production/rhs of a nonterminal


