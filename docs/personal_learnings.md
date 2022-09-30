Please do not look at my ramblings >.<

===
2022 Sept 25 Sun 12:53 AM
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

===
2022 Sept 25 Sun 7:46 AM
===

Not me wasting another 50 minutes T.T

Anyway, this time I was having issues with `test_deep_no_end`. I'm gonna admit
I don't completely understand how redirecting works? Anyway, based on what passed
and what my assumptions of how it works is:
(1) We tell the client that we moved to a new relative address!
(2) We use the new relative address and expect something in return!
Ahh... I'll ask the TA or professor about this to make sure I'm understanding this
correctly >.<
