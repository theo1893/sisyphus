from typing import Dict

from tools.data_provider.base import RapidDataProviderBase, EndpointSchema


class TwitterProvider(RapidDataProviderBase):
    def __init__(self):
        endpoints: Dict[str, EndpointSchema] = {
            "Twitter User Info": {
                "route": "/screenname.php",
                "method": "GET",
                "description": "Get information about a Twitter user by screenname or user ID.",
                "payload": {
                    "screenname": "Twitter username without the @ symbol",
                    "rest_id": "Optional Twitter user's ID. If provided, overwrites screenname parameter."
                }
            },
            "User Timeline": {
                "route": "/timeline.php",
                "method": "GET",
                "description": "Get tweets from a user's timeline.",
                "payload": {
                    "screenname": "Twitter username without the @ symbol",
                    "rest_id": "Optional parameter that overwrites the screenname",
                    "cursor": "Optional pagination cursor"
                }
            },
            "User Following": {
                "route": "/following.php",
                "method": "GET",
                "description": "Get users that a specific user follows.",
                "payload": {
                    "screenname": "Twitter username without the @ symbol",
                    "rest_id": "Optional parameter that overwrites the screenname",
                    "cursor": "Optional pagination cursor"
                }
            },
            "User Followers": {
                "route": "/followers.php",
                "method": "GET",
                "description": "Get followers of a specific user.",
                "payload": {
                    "screenname": "Twitter username without the @ symbol",
                    "cursor": "Optional pagination cursor"
                }
            },
            "Twitter Search": {
                "route": "/search.php",
                "method": "GET",
                "description": "Search for tweets with a specific query.",
                "payload": {
                    "query": "Search query string",
                    "cursor": "Optional pagination cursor",
                    "search_type": "Optional search type (e.g. 'Top')"
                }
            },
            "User Replies": {
                "route": "/replies.php",
                "method": "GET",
                "description": "Get replies made by a user.",
                "payload": {
                    "screenname": "Twitter username without the @ symbol",
                    "cursor": "Optional pagination cursor"
                }
            },
            "Check Retweet": {
                "route": "/checkretweet.php",
                "method": "GET",
                "description": "Check if a user has retweeted a specific tweet.",
                "payload": {
                    "screenname": "Twitter username without the @ symbol",
                    "tweet_id": "ID of the tweet to check"
                }
            },
            "Get Tweet": {
                "route": "/tweet.php",
                "method": "GET",
                "description": "Get details of a specific tweet by ID.",
                "payload": {
                    "id": "ID of the tweet"
                }
            },
            "Get Tweet Thread": {
                "route": "/tweet_thread.php",
                "method": "GET",
                "description": "Get a thread of tweets starting from a specific tweet ID.",
                "payload": {
                    "id": "ID of the tweet",
                    "cursor": "Optional pagination cursor"
                }
            },
            "Get Retweets": {
                "route": "/retweets.php",
                "method": "GET",
                "description": "Get users who retweeted a specific tweet.",
                "payload": {
                    "id": "ID of the tweet",
                    "cursor": "Optional pagination cursor"
                }
            },
            "Get Latest Replies": {
                "route": "/latest_replies.php",
                "method": "GET",
                "description": "Get the latest replies to a specific tweet.",
                "payload": {
                    "id": "ID of the tweet",
                    "cursor": "Optional pagination cursor"
                }
            }
        }
        base_url = "https://twitter-api45.p.rapidapi.com"
        super().__init__(base_url, endpoints)
