# RPi-CaptureBallsGame
![Capture_the_Balls](https://github.com/luizmanella/RPi-CaptureBallsGame/assets/39210022/86b102f3-b838-498d-8787-183de8ea328e)

Capture Balls Game is a game made with a joystick on a Raspberry Pi 4 where you race against a bot to see who can capture more balls in 60 seconds. You and the bot are both a circles, white and black respectively. Your goal is to run into as many target (red) balls in 60 seconds as you can. You are racing against an NPC who is constantly going after the closest balls to it. To make the game more difficult, the speed of the NPC increases relative to how much you are beating it by. If you are tied, or losing, it will go back to its default state. The spawns are random but they never spawn in a place that collides with any other ball or player (you or NPC). Three balls spawn at the same time, which can increase the difficulty of the game because the NPC travels in a straight line to the closest balls and therefore can quickly stack up points. 

This project was something I put together in about 3-4 hours in order to do something fun as I learn how to use RPis to build robots. This is a step along the journey to build my own drown. By no means is the code optimized nor is it pretty. I added things as I went and didn't want to backtrack and clean it up (object oriented programming would've been much better). This was super fun to build, and more can be done to improve it and make it more interesting. Some ideas for anyone who wants to build on this is to add an LED and a buzzer to blink and buzz as you score and even sync it with the count down so theres visual and audio cues.

<h3>Rasberry Pi Setup</h3>
A few things to note on setting up the game. You will need the following hardware components:
<ul>
  <li>Raspberry Pi</li>
  <li>Breadboard</li>
  <li>Jumper cables (male-male and female-male)</li>
  <li>A 10 kilo Ohm resistor</li>
  <li>A joystick (I used that which came with the Freenove kit)</li>
  <li>ADC module (I used the ADS7830)</li>
</ul>
To use the ADC module, I followed the Freenove tutorial to set it up and used their code to read the values produced by ADC and to covert to voltages. When setting up the breadboard, I chose to use the GPIO18 pin to connect to the joystick in order to read the Z-pin. As for the potentiometers of the joystick I used the pins A0, A1 on the ADC board.

<h3>Playing the Game</h3>
From the main menu, you can either use your mouse to click start or click down on the joystick. As you play, your points accumulate and are displayed on the top left. To the right of your score is the NPC's score. The game lasts for 60 seconds. Once it is done, it will stop the game and display your points and the NPC's points. You can then restart the game by clicking down on the joystick or using your mouse.

<h3>Editing the Game</h3>
Since the code isn't optimal, editing the number of balls or number of NPCs is not straight forward. What is very simple is editing the difficulty of the game. You can change the baseline speed of the NPC by going to the <i>move_npc()</i> function and editing the <b>npc_speed</b> variable. I would not recommend going below 2 as it becomes way too easy. For even more customization change the multiplier computation in the <b>if</b> statement underneath the speed variable. The <i>multiplier</i>  serves as a way to control the fluid ability of the NPC to improve if you are getting too far ahead of it. The way I currently handle this on-the-fly improvement is by increasing the speed of the NPC as a percentage of how much you are beating it by. Try messing with those two and find settings that you like.
