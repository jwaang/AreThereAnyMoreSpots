# AreThereAnyMoreSpots  
Sends an email notification if there are spots available for the class. Works for both PC and Mac.

# Problem
Texas A&M classes get taken up very fast, however some spots open up randomly. I don't have time to constantly check if any spots are open for the classes I want to take, so I decided to make this. I've also always been very interested in web scraping so this is my first attempt at it.

# Requirements
Selenium  
ChromeDriver  
A&M login  
Python 2.7

# Problems
This was my first real project I ever did with Python so the code might be a little bit messy and inefficient, but I honestly had a lot of fun making this. I first tried to use requests library however I could not get past the login page, because my school's robot.txt was set to "Disallow: /" and I couldn't find a workaround. My second attempt was with mechanize, however after successfully logging in, I realized that mechanize could not run Javascript (which was required by the website). My third attempt was to use Selenium which <i>finally</i> worked.  
The procedure was fairly simple, all I had to do was tell Selenium what elements to press and what to look out for. My main trouble was not finding what elements to press, but how to syntactically tell Selenium what elements to press. In the end, things started becoming easier as I slowly got the hang of it.

# Tasks
[x] Log in  
[x] Search if class has spots  
[x] Email  
[x] Loop for multiple class searches  
[ ] Auto Register
