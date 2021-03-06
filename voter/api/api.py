import json
from datetime import datetime
from flask import Blueprint, request, jsonify, make_response

with open("data.json", "r", encoding="utf8") as read_data:
    channels = json.load(read_data)

api_channels = Blueprint('api_channels', __name__)


@api_channels.route("/channels/all")
def list_channels():
    """ Lists all channels in the database. """

    return jsonify(channels)


@api_channels.route("/channels/<channel>")
def get_channel(channel):
    """
    If no query specified, prints the name of the
    YouTube channel typed. When a query with the
    name "vote" is given, adds or substracts 1
    from the specified YouTube score.
    """

    if "vote" in request.args:
        vote = str(request.args["vote"])

        if channel in channels:
            # Adds/substracts 1 from the channel.
            if vote == "upvote":
                channels[channel] += 1
            elif vote == "downvote":
                channels[channel] -= 1
            else:
                return "Vote word not recognised."

            # Write to database file.
            with open("data.json", "w", encoding="utf8") as write_data:
                json.dump(channels, write_data, indent=4)

            # Write to log file.
            with open("log.txt", "a") as append:
                today = datetime.today().strftime('%Y-%m-%d-%H:%M')
                append.write(f"\n{vote.title()}d {channel} on {today}")

            return f"You {vote}d successfully the channel {channel}."
        else:
            return "Channel not found on the list."
    else:
        if channel in channels:
            return "Channel: " + channel
        else:
            return "Channel not found on the list."


@api_channels.route("/channels/<channel>/image.svg")
def img_channel(channel):
    """ Returns the YouTube score in a svg image. """

    svg_image = f"""
                <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
                width="52px" height="22px" viewBox="0 0 52 22" fill="none">
                <style>
                    .text {{
                        font-family: "Segoe UI", Ubuntu, Sans-Serif;
                        font-weight: bold;
                    }}
                    </style>
                    <rect x="0.5" y="0.5" height="99%" width="51" fill="none"/>
                    <g>
                        <text x="5" y="15" fill="#00b4f0" class="text">
                            {channels[channel]}
                        </text>
                    </g>
                </svg>
                """

    if channel in channels:
        response = make_response(svg_image)
        response.headers.set('Content-Type', 'image/svg+xml')
        return response
    else:
        return "Channel not found on the list"
