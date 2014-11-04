Project
=======

Here is short explanation of the project work going to be done in the second
period.

Current Status
--------------

Current status of the color naming Twitter bot lays somewhere in the between of 
acceptable and inadequate. The bot is acceptable in the sense, that it has been coded quite 
modularly, i.e. it should be easy to plug new functionalities in the existing core.
On the other hand, it is inadequate because the currently coded bot's main 
functionalities are not good enough to represent a dynamic and truly (in the
computational creativity sense) self-creating system.

Currently, the bot's instantiation consists of five main objects, each of which 
contributes to the functionality in their own way:

**Reasoning:** 

	Reasoning-class contains accumulated information about the 
	generated Tweet during its construction. Other modules take it as an input and 
	alter its contents on the fly.

**Muse:** 

	Muse is an object, which on demand inspires the bot to create new content.
	In its most basic form it will give and new color code for the bot (inside the 
	Reasoning-object), which other modules will flesh out to make a complete new Tweet.
	However, Muse can also add other information, such as mood or image, to go with
	the Reasoning-object.

**ColorSemantics:** 

	ColorSemantics-object names the color code given to it. 
	It can take into account other side information in the Reasoning-object if it seems 
	it necessary.

**Context:** 

	Context-object gives framing for the Tweet. It handles the
	information in the Reasoning-object in order to create good context for the Tweet. 
	In its most basic form, the context is a text output where the name of the color 
	appears, but it can also contain created images.

**Core:** 

	TweetCore is the main class which should mostly appear as an invisible glue
	between other modules. It handles passing of the Reasoning-object to other 
	modules in right order and takes care of tweeting for the Tweets that are
	seen good enough.

It should be noted, that Muse, ColorSemantics and Context objects are easily 
replaceable by instantiations of derived classes which conform to same interfaces.

Personality
...........

In its current form, the bot tries to show a personality that is interested in 
new age and other spiritual concepts. This is mostly done by the Context-object
which creates an semi-random sentence template from its possible choices and
adds the color name to a suitable place in the template. Furthermore, the Muse 
adds a slight twist to the color name picking as it generates a random mood and
aura color, both of which vary with the moon phase and time of the year. The 
color codes are more appreciated, if they are closer to the current aura color,
if no close enough color is found, then the Tweet generation is halted.
 

Project's Contributions
-----------------------

As in its current form, the Twitter bot merely generates new Tweets and has very 
little sense, or knowledge, of the world: **the main contribution of the project
will be to add more knowledge and more sophisticated appreciation methods for the 
different phases in the Tweet generation (to make the personality more prominent).** 
These might include, e.g.

* Add at least one more knowledge source for the bot. Possible sources:

	* Use one/some of the Tony's resources
	* Use Google search / bigrams / trigrams (more exhaustively)
	* Use Wikipedia's category information for colors
	* Do Wikipedia searches of the interesting topics on the fly
	* Mine WordNet more thoroughly
	* Use (from the New Age perspective) interesting corpuses
	
* Alter color name creation to build more spiritual names:

	* Automatically (how?)
	* Construct vocabulary by hand 
	
* Alter sentence generation to be more personal and show more clearly the current mood of the bot:

	* Add attribute (sentiment, etc.) analysis to the sentences constructed by Context-object
	* Use a heuristic search algorithm to find the sentence which most suits the current mood of the bot
	* Add notes of the aura colors and characteristics associated with that color to the textual framing
	* Add more sentence templates
	* Alter sentence vocabularies

	
* Make the bot more social in Twitter, by adding Muses which:

	* Listen other specific accounts 
	* React to the most recent Tweets with certain keywords (color names?)
	* React to certain (fixed) hashtags
	* React to currently trending topics

* Change the image added to the Tweet:

	* Create new interesting image to go with the Tweet 
	
		* Make "motivational images" with the Tweet as a text
		
	* Search for the best image to go with the Tweet and add it
