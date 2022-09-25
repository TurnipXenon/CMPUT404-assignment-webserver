Please do not look at my ramblings >.<

===
Sept 25 12:53 AM
===

(Don't judge the time. I work best after 9 PM >.<)

I may or may not have spent 50 minutes trying to debug why request.urlopen wasn't
being caught properly in test_405. I taught I was sending the wrong http format.
There were other attempts trying to understand the trace.
I checked out the error trace, and it says something like:

```
Remote end closed connection without response
```

Without response clicked, so I wasn't sending the response back lol.
I was just returning the string when I should have been doing a `sendall`.
To prevent this mistake in the future, I'll put the `sendall` as part of
`ResponseMaker`.