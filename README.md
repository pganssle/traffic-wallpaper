I like to make use of my desktop wallpaper to display some useful information. At work I have 3 monitors, and I don't usually have many (or any) windows open on the leftmost one, so I decided that I'd use it to monitor the traffic on my commute.

These scripts grab the traffic data from [Houston TranStar](http://www.houstontranstar.org/) - the traffic map, and a number of the traffic cameras and merges them into one image, the size of my monitor resolution:

<div align="center">
    <a href="https://raw.githubusercontent.com/pganssle/traffic-wallpaper/master/images/wallpaper/composite_map.png"><img src="https://raw.githubusercontent.com/pganssle/traffic-wallpaper/master/images/wallpaper/composite_map.png"></a>
</div>

The `run_updates.pyw` updates the images every 30 seconds (configurable time interval in the `settings.json` file), and sets it to my desktop background (Windows). There doesn't seem to be a good way to set the desktop backgrounds individually, but since I want a different background on each screen, I make a composite image out of the traffic map and the other backgrounds.

The `RunUpdates.bat` batch file is a wrapper for `run_updates.pyw`, and can be used if you want to use Task Scheduler to automatically start the script on startup. Unfortunately, it leaves a console window up - see [this SO question](https://stackoverflow.com/questions/324539/how-can-i-run-a-program-from-a-batch-file-without-having-the-console-open-after) for details on how to fix that, if that's your problem.

