from flask import Flask, jsonify
import feedparser
from flask_caching import Cache
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend communication

# Flask-Caching configuration
cache_config = {
    "CACHE_TYPE": "SimpleCache",  # Simple in-memory cache
    "CACHE_DEFAULT_TIMEOUT": 900  # 15 minutes
}

app.config.from_mapping(cache_config)
cache = Cache(app)

RSS_FEED_URL = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"

@app.route('/api/rss', methods=['GET'])
@cache.cached()
def get_rss_feed():
    # Fetch and parse the RSS feed using feedparser
    feed = feedparser.parse(RSS_FEED_URL)
    # Construct a JSON-friendly format to return to the frontend
    articles = [
        {
            "title": entry.title,
            "link": entry.link,
            "description": entry.summary,
            "published": entry.published,
            "image": entry.get("media_content", [{}])[0].get("url", "")  # Get image if present
        }
        for entry in feed.entries
    ]

    # Return the JSON response
    return jsonify({"items": articles})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
