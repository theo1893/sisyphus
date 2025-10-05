from typing import Dict

from tools.data_provider.base import RapidDataProviderBase, EndpointSchema


class LinkedinProvider(RapidDataProviderBase):
    def __init__(self):
        endpoints: Dict[str, EndpointSchema] = {
            "Profile Detail": {
                "route": "/profile/detail",
                "method": "GET",
                "description": "Fetch user profile data by username",
                "payload": {
                    "username": "Required. The username to search.",
                }
            },
            "Profile Posts": {
                "route": "/profile/posts",
                "method": "GET",
                "description": "Fetch user posts data by username",
                "payload": {
                    "username": "Required. The username to search.",
                    "page_number": "Optional. The page number to get.",
                    "pagination_token": "Optional. Token from previous page response for paginated requests (optional, only needed for pages after first). For example, to get result from page 2, use pagination token from response of page 1",
                }
            },
            "Profile Comments": {
                "route": "/profile/comments",
                "method": "GET",
                "description": "Fetch user comments data by username",
                "payload": {
                    "username": "Required. The username to search.",
                    "page_number": "Optional. The page number to get.",
                    "pagination_token": "Optional. Token from previous page response for paginated requests (optional, only needed for pages after first). For example, to get result from page 2, use pagination token from response of page 1",
                }
            },
            "Profile Reactions": {
                "route": "/profile/reactions",
                "method": "GET",
                "description": "Fetch user reaction data by username",
                "payload": {
                    "username": "Required. The username to search.",
                    "page_number": "Optional. The page number to get.",
                    "pagination_token": "Optional. Token from previous page response for paginated requests (optional, only needed for pages after first). For example, to get result from page 2, use pagination token from response of page 1",
                }
            },
            "Company Details": {
                "route": "/companies/detail",
                "method": "GET",
                "description": "Fetch company details",
                "payload": {
                    "identifier": "Required. Company name (youtube) OR LinkedIn URL (https://www.linkedin.com/company/youtube/) OR Urn (1035)"
                }
            },
            "Company Posts": {
                "route": "/company/posts",
                "method": "GET",
                "description": "Fetch company posts",
                "payload": {
                    "company_name": "Required. Company name can be: - Company name (youtube) - LinkedIn URL (https://www.linkedin.com/company/youtube/) - Urn : (1035)"
                }
            },
            "Company Search": {
                "route": "/companies/search",
                "method": "GET",
                "description": "Fuzzy searching for companies by keyword",
                "payload": {
                    "keyword": "Required. Company name can be: - Company name (youtube) - LinkedIn URL (https://www.linkedin.com/company/youtube/) - Urn : (1035)",
                    "page_number": "Optional. The page number to get.",
                    "location_ids": "Optional. Comma-separated list of LinkedIn location IDs to filter companies by (e.g., '106693272,103644278')",
                    "industry_ids": "Optional. Comma-separated list of LinkedIn industry IDs to filter companies by (e.g., '6,4')",
                }
            },
            "Post Comments": {
                "route": "/post/comments",
                "method": "GET",
                "description": "Fetch post comments",
                "payload": {
                    "post_url": "Required. Urn (e.g: 7289521182721093633 ) or url (e.g : 'https://www.linkedin.com/posts/satyanadella_mayo-clinic-accelerates-personalized-medicine-activity-7285003244957773826-TrmI/')",
                    "page_number": "Optional. The page number to get",
                    "sort_order": "Optional. Sort order (Most relevant, Most recent)"
                }
            },
            "Post Details": {
                "route": "/post/detail",
                "method": "GET",
                "description": "Fetch post details",
                "payload": {
                    "post_url": "Required. The post url (e.g : 'https://www.linkedin.com/posts/satyanadella_mayo-clinic-accelerates-personalized-medicine-activity-7285003244957773826-TrmI/')"
                }
            },
            "Post Search": {
                "route": "/post/search",
                "method": "GET",
                "description": "Fuzzy searching for posts by keyword",
                "payload": {
                    "keyword": "Required. The keyword to search for",
                    "page_number": "Optional. The page number to get.",
                    "sort_type": "Optional. Can be one of the following: date_posted, relevance.",
                    "date_filter": "Optional. Can be one of the following: past-24h, past-week, past-month."
                }
            },
            "Post Reposts": {
                "route": "/post/reposts",
                "method": "GET",
                "description": "Fetch the reposts of specified post",
                "payload": {
                    "post_url": "Required. Urn (e.g: 7289521182721093633 ) or url (e.g : 'https://www.linkedin.com/posts/satyanadella_mayo-clinic-accelerates-personalized-medicine-activity-7285003244957773826-TrmI/')",
                    "page_number": "Optional. The page number to get.",
                }
            },
            "Post Reactions": {
                "route": "/post/reactions",
                "method": "GET",
                "description": "Fetch reactions of specified post",
                "payload": {
                    "post_url": "Required. Urn (e.g: 7289521182721093633 ) or url (e.g : 'https://www.linkedin.com/posts/satyanadella_mayo-clinic-accelerates-personalized-medicine-activity-7285003244957773826-TrmI/')",
                    "page_number": "Optional. The page number to get.",
                    "reaction_type": "Optional. Can be one of the following: ALL."
                }
            },
            "Search Job": {
                "route": "/jobs/search",
                "method": "GET",
                "description": "Search jobs",
                "payload": {
                    "keywords": "Required. Job keywords.",
                    "location": "Optional. Country or City name or geoId (eg: United States).",
                    "sort": "Optional. Sort order (relevant, recent)",
                    "page_number": "Optional.",
                    "date_posted": "Optional. Posted time range (month, week, day).",
                    "remote": "Optional. Workplace type (onsite, remote, hybrid).",
                    "experience": "Optional. Experience level (internship, entry, associate, mid_senior, director, executive).",
                    "job_type": "Job type (fulltime, parttime, contract, internship, other)."
                }
            },
            "Job Detail": {
                "route": "/jobs/detail",
                "method": "GET",
                "description": "Fetch job details",
                "payload": {
                    "job_id": "Required. LinkedIn job ID (e.g., 4011051212)"
                }
            }
        }
        base_url = "https://linkedin-scraper-api-real-time-fast-affordable.p.rapidapi.com"
        super().__init__(base_url, endpoints)
