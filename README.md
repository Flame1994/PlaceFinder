# Add to your server
https://discord.com/oauth2/authorize?client_id=959590134897053727&permissions=0&scope=bot

# How it works
Type the command
!place x1 y1 x2 y2 image seconds

Where you specify the coordinates of the top left corner of the grid and bottom right corner
as well as the image you want to assign to people
and then the amount of seconds you want to wait for people to opt-in.

Example:
!place 10 10 20 20 https://i.imgur.com/2zwSk0t.jpg 60

![Example](https://i.imgur.com/2zwSk0t.jpg)


This will wait for people to opt-in to place pixels in the grid starting at coordinates 10,10 (top left corner) till 20,20 (bottom right corner). It will wait 60 seconds for people to opt in before assigning pixels to them.
