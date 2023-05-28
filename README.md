# resybot

A bot to get the reservations I want because eating in New York is so hard.

To get this to work, you need a couple things. The first is the restaurant ID. To find this, navigate to the Resy page of the restaurant you want to go to. Inspect the browswer and click on network. Refresh the page. Look through the network calls until you see the 'find?day=...' call. Look at the URL to see the venue_id.

Next, you will need to get your Resy API token. They stopped exposing this on your profile a couple years ago, so you also have to look in the browser network calls. On the same network call as above, look at the headers tab and scroll down to the 'Authorization' key. You should see your token there.

Now update those values, along with the day you want to go and the party size.

The last thing you have to find out is when the reservations drop. Most restaurants say this on their sites or someone on Reddit knows.

Put your script in the cloud, add a cron job and there you go!
