Composing text with a guitar
----------------------------

As a new guitarist, I've had a hankering to make a project that integrates my guitar. 

Eventually, an idea hit: what if you could type on your keyboard by playing particular notes?

It's a terrible idea, but it sure is fun. This is off-keyboard in action:

(twitter link)

I learned interesting things over the course of implementing off-keyboard, like the basics of digital signal processing,
and some unintuitive things about the way instruments produce sound.

The goal we want to achieve can be split up into 3 tasks:

1) Map notes to a keyboard key
2) Identify what note is being played
3) Send the key as a keyboard event

Let's go through each of these.

Deciding key placement
-----------------------

Before I wrote any code, I wanted to plan ahead and figure out where each keyboard key
would be placed on the guitar. 

To do this, there are some basic facts to keep in mind about music. A given note played on an instrument has two components: a _note_, and an _octave_. 
An octave describes how 'high' or 'low' a note sounds. The same notes are repeated across an infinite selection of octaves to play them in. In practice, though,
modern music generally only uses 5 octaves, as higher and lower frequencies than that are out of our hearing range.
A note, with the octave that describes it, is called a _pitch_. We could talk about an abstract note `E`, but we don't know 
what it sounds like exactly unless we give the octave, such as `E2` or `E3`. 

Mathematically, each note in the 12-tone Western scale corresponds to a particular sound-wave frequency. To move any note one octave up,
you double the frequency. That is, the frequency of the sound-wave that we call `C1` is half the frequency of the sound-wave we call `C2`, and so on.

Additionally, pitches are repeated on the guitar -- that is, the pitch `C3` is available in multiple places along the guitar's fretboard.

In fact, there are many less unique pitches on the guitar than there are positions that can be played. 
While there are 108 playable positions on an 18-fret 6-string guitar, there are only 44 unique semitones.

Thankfully, this is more than enough for the English alphabet of 26 letters, plus a few extra for punctuation and spacing.

The first thing we did was visually mark where the unique pitches lay: [image1.png]

Next, let's throw some letters on each of these! To optimize playability, I referenced the 
list of most frequenctly used English letters, and tried to give 'optimal' positions to the most common letters.

Here, I arranged the most common letters vertically along the strings: [attempt1.png]
This failed as it means my fingers all had to cramp up around the first fret for the most common letters. Can we do better?

This time, I arranged the most frequently used letters horizontally, so it became easier for the fingers to move around words. [attempt2.png]

Finally, I settled on this arrangement, which gave comfortable access to the most commonly used symbols, along with easily access
to space/enter/punctuation. [attempt3.png]

Next up, the fun stuff: note detection!

Identify A Playing Note
-----------------------

