S
=
*Your very own URL shortening service*

This is a Python2.7 based flask application which is a different take at url shorteners. Most url shortening scripts use on-the-fly base conversion or simple hashing for generation of short urls. S precomputes all possible combinations on a set of url safe characters with appropriate n and r values. It is very simple and configurable.

Setup
-----
* Clone this git repo into your intended folder.
* Install requirements ``` pip install -r requirements.txt```
* Download and setup Redis database from http://redis.io/download
* Open config.py and...
    * Change the ```short_url_domain``` to your desired domain name
    * Set the ```r_min``` and ```r_max``` values
    * Check to correct ```redis``` db details if required
    * Add more ```blocked_short_codes``` as necessary
* Start redis database service
* [IMPORTANT] Run the ```generate_short_code.py``` script and wait until it is complete (This might take a few seconds to a few hours based on your char_set, r_min and r_max values. Check below for benchmarks)
* Start flask app
* Point your domain to this location and you are done!!

PS 1: You do not have to worry about having a proxy for serving requests as there are no static files involved anywhere.
PS 2: You should as easily be able to deploy it on a subdomain if desired.

Endpoints
---------
1. ```POST | <your.domain>/get``` takes the url you want to convert and gives you a converted url.<br>
Method: POST<br>
Params: url<br>
Output:<br>
['failure', 'No url sent'] -- When you do not pass valid parameter<br>
['failure', 'Url length not accepted'] -- When a url is longer than the charaters allowed in config<br>
['failure', 'Url does not seem to be valid'] -- When you pass an invalid url<br>
['failure', 'Some error occured'] -- In case of previously unknown exceptions<br>
['success', 'your_short_url'] -- When all is well!!<br>

2. ```GET | <your.short.url>``` takes your short url and looks up the actual url and redirects it.<br>
Method: GET<br>
Params: None<br>
Output:<br>
404 page not found -- If URL not found in database<br>
301 redirection -- If a valid actual url is found for the short url<br>

Approach
--------
As explained above, S precomputes all possible combinations of the character set provided and generates a key value set using a counter. A prefix character outside of the character set is used so that there are no collisions between used short codes and new ones. Also, all the blocked_short_codes in the config are skipped. It looks something like
```(<prefix><count>, <short_code>)```

When you call /get method to generate the short url, it simply increments a counter and sets a new short code to the given long url and makes 2 db entries for lookup. The awesomeness of redis makes this almost non trivial
```(<short_code>, <actual_url>)```<br>
```(<actual_url>, <short_code>)```

This way all the computation of generation of short_codes are transferred to outside of user thread. Since all redis operations used in both user exposed endpoints are atomic. The time complexity of O(1) is achieved effortlessly.

Metrics & Benchmarks
--------------------
**1. How many URLs??**<br>
In order to calculate the number of urls your service can actually cater to, you need the following variables...<br>
n = Number of characters in ```char_set```. In default case this is 64<br>
r_min = Min number of characters in the ```short_code```<br>
r_max = Max number of characters in the ```short_code```<br>
no_of_blocked_words = In the default case this is 3<br>
Using these you can calculate the max nuber of urls you can service using<br>
```
(Sum(n^r) for all r between r_min to r_max) - no_of_blocked_words
```

In the default case...
```
n = 64
r_min = 1
r_max = 3
no_of_blocked_words = 3

Then...

(n^1 + n^2 + n^3) - no_of_blocked_words
= (64^1 + 64^2 + 64^3) - 3
= (64 + 4096 + 262144) - 3
= 266304 - 3
= 266301
```
Therefore,
* With 64 characters and 1 to 3 repetitions and 3 blocked words, S can serve 266,301 URLs
* With 64 characters and 1 to 4 repetitions and 3 blocked words, S can serve 17,043,517 URLs
* With 64 characters and 1 to 5 repetitions and 3 blocked words, S can serve over 1.07 billion URLs
<br>and so on...

**2. Time taken to generate codes**<br>
On my Mac with 8 GB RAM (and not dedicatedly running this app) took ~35 seconds to generate 266,301 URLs. That means it will take roughly 39 hours to generate 1 billion short codes. Don't be alarmed because...<br>
* You can start running your flask server as soon as (after ~35 secs to be safe) you start running the short code generator as you will have significant number of short codes being generated by the second.
* Your dedicated hosting setup might generate it faster than my benchmarks.
* You can limit r_max to 4 if you are not planning to exceed 17 million URLs
* You should look at parallelising the short code generator if you do expect huge scale.

Ideas to Scale
--------------
If you do want to scale your service beyond a billion URLs it is possible by one of the following ways.<br>
1. Increase the r_max and regenerate codes. With an r_max of 6 you can serve ~69 billion URLs. Just imagine if you push r_max of 10!! All you'll need is proper infra to support such scale.<br>
2. If you are willing to spend some time in tinkering with the code, then you can introduce the logic of a prefix for your short_urls. Ex:
```http://your.domain/xjgkt``` will now look like ```http://your.domain/s/xjjng```

Regeneration of Short Codes
---------------------------
Let's say you started with an r_max of 4 and now you have realised that you need more short codes. This is also very straightforward. All you have to do is **ensure that no other parameters in the config is changed from your previous run to this except for the r_max** and then run the short_code_generator again with your deisred r_max. This will...<br>
1. Overwrite existing new keys generated and add extra new keys as per your new r_max.<br>
2. Your old short codes or url mappings will not get affected because new url mappings will be created based on counter which maintains a running pointer to the new short code to be taken for the next url shortening request.
<br>Neat, isn't it?!

Improvements
------------
All in all it took me about 2 hours to get this up from naught to whatever is committed here. In fact it took me more time to write this read me file than the whole service, so there is definitely room for improvements. Please please please open an issue here on github or send me a mail at vinay@askvinay.com if you find any missed corner cases, bugs or typos.
