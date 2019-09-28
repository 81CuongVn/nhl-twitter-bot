import logging
import os
from enum import Enum

from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps

from hockeygamebot.definitions import IMAGES_PATH, PROJECT_ROOT
from hockeygamebot.helpers import utils
from hockeygamebot.models.gameevent import GoalEvent
from hockeygamebot.models.game import Game


class Backgrounds:
    """ Paths to background images & files used in the imaging module. """

    PREGAME = os.path.join(IMAGES_PATH, "BG2019-Gameday-Pregame.png")
    STATS = os.path.join(IMAGES_PATH, "BG2019-Gameday-ScoreReport.png")


class Colors:
    """ Specifies commonly used colors. """

    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    BLACK = (0, 0, 0)


class FontFiles:
    """ Paths to font files used in the imaging module. """

    BITTER_REGULAR = os.path.join(PROJECT_ROOT, "resources/fonts/Bitter-Regular.ttf")
    BITTER_BOLD = os.path.join(PROJECT_ROOT, "resources/fonts/Bitter-Bold.ttf")


class FontSizes:
    """ Font sizes used in the imaging module. """

    TITLE = 80
    DETAIL_LARGE = 56
    DETAIL_SMALL = 50
    RECORD = 38
    GAMENUMBER = 40
    PRESEASON = 28
    STAT_TITLE = 19
    STAT_VALUE = 25
    SCORE = 75
    GOAL_SCORER = 14
    ASST_SCORER = 14
    NO_GOAL_TEXT = 30


class Constants:
    """ Constant chart-based values. """

    CHART_START_X = 35
    CHART_WIDTH = 690
    # CHART_END_X = 725
    CHART_END_X = CHART_START_X + CHART_WIDTH
    CHART_GOAL_SEPARATOR = 40

    GOALBOX_START_X = CHART_END_X + CHART_GOAL_SEPARATOR
    GOALBOX_START_Y = 200
    GOALBOX_TEAM_H = 25
    GOALBOX_W = 400
    GOALBOX_H = 220
    GOALBOX_SEPARATOR = 15


class StatTypes(Enum):
    """ Stat types used in our stat-bar image type. """

    SHOTS = 0
    BLOCKED_SHOTS = 1
    HITS = 2
    POWER_PLAYS = 3
    PENALTY_MINS = 4
    FACEOFF_PCT = 5


def team_colors(team_name):
    """ Accepts a team name and returns the background color & text color.

    Args:
        team_name: Full name of the NHL Team

    Returns:
        dict: Dictionary of primary & secondary colors
    """

    team_colors_dict = {
        "Anaheim Ducks": {
            "primary": {"bg": (252, 76, 2), "text": (255, 255, 255)},
            "secondary": {"bg": (162, 170, 173), "text": (0, 0, 0)},
        },
        "Arizona Coyotes": {
            "primary": {"bg": (134, 38, 51), "text": (255, 255, 255)},
            "secondary": {"bg": (221, 203, 164), "text": (0, 0, 0)},
        },
        "Boston Bruins": {
            "primary": {"bg": (255, 184, 28), "text": (255, 255, 255)},
            "secondary": {"bg": (255, 255, 255), "text": (0, 0, 0)},
        },
        "Buffalo Sabres": {
            "primary": {"bg": (4, 30, 66), "text": (255, 255, 255)},
            "secondary": {"bg": (162, 170, 173), "text": (0, 0, 0)},
        },
        "Calgary Flames": {
            "primary": {"bg": (200, 16, 46), "text": (255, 255, 255)},
            "secondary": {"bg": (241, 190, 72), "text": (0, 0, 0)},
        },
        "Carolina Hurricanes": {
            "primary": {"bg": (200, 16, 46), "text": (255, 255, 255)},
            "secondary": {"bg": (162, 170, 173), "text": (0, 0, 0)},
        },
        "Chicago Blackhawks": {
            "primary": {"bg": (204, 138, 0), "text": (255, 255, 255)},
            "secondary": {"bg": (255, 209, 0), "text": (0, 0, 0)},
        },
        "Colorado Avalanche": {
            "primary": {"bg": (111, 38, 61), "text": (255, 255, 255)},
            "secondary": {"bg": (35, 97, 146), "text": (0, 0, 0)},
        },
        "Columbus Blue Jackets": {
            "primary": {"bg": (200, 16, 46), "text": (255, 255, 255)},
            "secondary": {"bg": (4, 30, 66), "text": (0, 0, 0)},
        },
        "Dallas Stars": {
            "primary": {"bg": (0, 99, 65), "text": (255, 255, 255)},
            "secondary": {"bg": (138, 141, 143), "text": (0, 0, 0)},
        },
        "Detroit Red Wings": {
            "primary": {"bg": (200, 16, 46), "text": (255, 255, 255)},
            "secondary": {"bg": (255, 255, 255), "text": (0, 0, 0)},
        },
        "Edmonton Oilers": {
            "primary": {"bg": (207, 69, 32), "text": (255, 255, 255)},
            "secondary": {"bg": (0, 32, 91), "text": (0, 0, 0)},
        },
        "Florida Panthers": {
            "primary": {"bg": (4, 30, 66), "text": (255, 255, 255)},
            "secondary": {"bg": (185, 151, 91), "text": (0, 0, 0)},
        },
        "Los Angeles Kings": {
            "primary": {"bg": (162, 170, 173), "text": (255, 255, 255)},
            "secondary": {"bg": (255, 255, 255), "text": (0, 0, 0)},
        },
        "Minnesota Wild": {
            "primary": {"bg": (21, 71, 52), "text": (255, 255, 255)},
            "secondary": {"bg": (166, 25, 46), "text": (0, 0, 0)},
        },
        "Montréal Canadiens": {
            "primary": {"bg": (166, 25, 46), "text": (255, 255, 255)},
            "secondary": {"bg": (0, 30, 98), "text": (0, 0, 0)},
        },
        "Nashville Predators": {
            "primary": {"bg": (255, 184, 28), "text": (255, 255, 255)},
            "secondary": {"bg": (4, 30, 66), "text": (0, 0, 0)},
        },
        "New Jersey Devils": {
            "primary": {"bg": (200, 16, 46), "text": (255, 255, 255)},
            "secondary": {"bg": (255, 255, 255), "text": (0, 0, 0)},
        },
        "New York Islanders": {
            "primary": {"bg": (252, 76, 2), "text": (255, 255, 255)},
            "secondary": {"bg": (0, 48, 135), "text": (0, 0, 0)},
        },
        "New York Rangers": {
            "primary": {"bg": (0, 51, 160), "text": (255, 255, 255)},
            "secondary": {"bg": (200, 16, 46), "text": (0, 0, 0)},
        },
        "Ottawa Senators": {
            "primary": {"bg": (198, 146, 20), "text": (255, 255, 255)},
            "secondary": {"bg": (200, 16, 46), "text": (0, 0, 0)},
        },
        "Philadelphia Flyers": {
            "primary": {"bg": (250, 70, 22), "text": (255, 255, 255)},
            "secondary": {"bg": (255, 255, 255), "text": (0, 0, 0)},
        },
        "Pittsburgh Penguins": {
            "primary": {"bg": (255, 184, 28), "text": (255, 255, 255)},
            "secondary": {"bg": (255, 255, 255), "text": (0, 0, 0)},
        },
        "San Jose Sharks": {
            "primary": {"bg": (0, 98, 114), "text": (255, 255, 255)},
            "secondary": {"bg": (229, 114, 0), "text": (0, 0, 0)},
        },
        "St. Louis Blues": {
            "primary": {"bg": (0, 48, 135), "text": (255, 255, 255)},
            "secondary": {"bg": (4, 30, 66), "text": (0, 0, 0)},
        },
        "Tampa Bay Lightning": {
            "primary": {"bg": (0, 32, 91), "text": (255, 255, 255)},
            "secondary": {"bg": (255, 255, 255), "text": (0, 0, 0)},
        },
        "Toronto Maple Leafs": {
            "primary": {"bg": (0, 32, 91), "text": (255, 255, 255)},
            "secondary": {"bg": (255, 255, 255), "text": (0, 0, 0)},
        },
        "Vancouver Canucks": {
            "primary": {"bg": (0, 32, 91), "text": (255, 255, 255)},
            "secondary": {"bg": (151, 153, 155), "text": (0, 0, 0)},
        },
        "Vegas Golden Knights": {
            "primary": {"bg": (180, 151, 90), "text": (255, 255, 255)},
            "secondary": {"bg": (51, 63, 66), "text": (0, 0, 0)},
        },
        "Washington Capitals": {
            "primary": {"bg": (166, 25, 46), "text": (255, 255, 255)},
            "secondary": {"bg": (4, 30, 66), "text": (255, 255, 255)},
        },
        "Winnipeg Jets": {
            "primary": {"bg": (4, 30, 66), "text": (255, 255, 255)},
            "secondary": {"bg": (200, 16, 46), "text": (0, 0, 0)},
        },
    }

    return team_colors_dict[team_name]


def center_text(draw, left, top, width, text, color, font, vertical=False, height=None):
    """ Draws text (at least) horizontally centered in a specified width. Can also
        center vertically if specified.

    Args:
        draw: Current PIL draw Object
        left: left coordinate (x) of the bounding box
        top: top coordinate (y) of the bounding box
        width: width of the bounding box
        text: text to draw
        color: color to draw the text in
        font: ImageFont instance

        vertical: align vertically
        height: height of the box to align vertically

    Returns:
        None
    """

    # Get text size (string length & font)
    w, h = draw.textsize(text, font)
    left_new = left + ((width - w) / 2)

    if not vertical:
        coords_new = (left_new, top)
        # Draw the text with the new coordinates
        draw.text(coords_new, text, fill=color, font=font, align="center")
    else:
        _, offset_y = font.getoffset(text)
        top_new = top + ((height - h - offset_y) / 2)
        coords_new = (left_new, top_new)
        # Draw the text with the new coordinates
        draw.text(coords_new, text, fill=color, font=font, align="center")


def valign_center_text(draw, left, top, height, text, color, font):
    """ Draws text centered in the vertical orientation in a specified height.

    Args:
        draw: Current PIL draw Object
        left: left coordinate (x) of the bounding box
        top: top coordinate (y) of the bounding box
        width: width of the bounding box
        text: text to draw
        color: color to draw the text in
        font: ImageFont instance

    Returns:
        None
    """

    # Get text size (string length & font)
    _, h = draw.textsize(text, font)

    # Get offset & new coordinates
    _, offset_y = font.getoffset(text)
    top_new = top + ((height - h - offset_y) / 2)
    coords_new = (left, top_new)

    # Draw the text with the new coordinates
    draw.text(coords_new, text, color, font, align="center")


def pregame_image(game: Game):
    """ Generates the pre-game image that is sent to social media platforms at the first
        run of the hockeygamebot script per day.

    Args:
        game: Current Game object

    Returns:
        bg: Finished Image instance
    """

    # Fonts used within the pregame image
    FONT_TITLE = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.TITLE)
    FONT_RECORD = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.RECORD)
    FONT_DETAIL_LARGE = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.DETAIL_LARGE)
    FONT_DETAIL_SMALL = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.DETAIL_SMALL)
    FONT_GAMENUMBER = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.GAMENUMBER * 3)

    # Pre-game specific constant values (incl coordinates)
    HEADER_TEXT = "PRE-GAME MATCHUP"
    LOGO_Y = 150
    COORDS_HOME_X = 245
    COORDS_AWAY_X = 650
    COORDS_HOME_LOGO = (COORDS_HOME_X, LOGO_Y)
    COORDS_AWAY_LOGO = (COORDS_AWAY_X, LOGO_Y)
    COORDS_GAME_NUM = (-90, 80)
    TEAM_RECORD_Y = LOGO_Y + 200

    # Generate records, venue & other strings
    home_pts = game.home_team.points
    home_record_str = f"{home_pts} PTS • {game.home_team.current_record}"
    away_pts = game.away_team.points
    away_record_str = f"{away_pts} PTS • {game.away_team.current_record}"

    text_gamenumber = "PRESEASON" if game.game_type == "PR" else f"{game.preferred_team.games + 1} OF 82"

    text_datetime = f"{game.game_date_short} • {game.game_time_local}"
    text_hashtags = f"{utils.team_hashtag(game.preferred_team.team_name, game.game_type)} • {game.game_hashtag}"

    bg = Image.open(Backgrounds.PREGAME)
    bg_w, bg_h = bg.size

    away_team = game.away_team.team_name.replace(" ", "")
    home_team = game.home_team.team_name.replace(" ", "")
    away_logo = Image.open(os.path.join(PROJECT_ROOT, f"resources/logos/{away_team}.png"))
    home_logo = Image.open(os.path.join(PROJECT_ROOT, f"resources/logos/{home_team}.png"))

    # Paste the home / away logos with the mask the same as the image
    bg.paste(away_logo, COORDS_AWAY_LOGO, away_logo)
    bg.paste(home_logo, COORDS_HOME_LOGO, home_logo)

    # Generates a 'draw' object that we use to draw on top of the image
    draw = ImageDraw.Draw(bg)

    # Draw text items on the background now
    # fmt: off
    center_text(
        draw=draw, left=0, top=0, width=bg_w, text=HEADER_TEXT, color=Colors.WHITE, font=FONT_TITLE
    )

    center_text(
        draw=draw, left=COORDS_HOME_X, top=TEAM_RECORD_Y, width=300,
        text=home_record_str, color=Colors.WHITE, font=FONT_RECORD
    )

    center_text(
        draw=draw, left=COORDS_AWAY_X, top=TEAM_RECORD_Y, width=300,
        text=away_record_str, color=Colors.WHITE, font=FONT_RECORD
    )

    center_text(
        draw=draw, left=0, top=480, width=bg_w,
        text=text_datetime, color=Colors.WHITE, font=FONT_DETAIL_LARGE,
    )

    center_text(
        draw=draw, left=0, top=540, width=bg_w,
        text=game.venue.upper(), color=Colors.WHITE, font=FONT_DETAIL_LARGE,
    )

    center_text(
        draw=draw, left=0, top=600, width=bg_w,
        text=text_hashtags, color=Colors.WHITE, font=FONT_DETAIL_SMALL,
    )
    # fmt: on

    # Create a new image to put the game number & cleanly rotate it
    txt = Image.new("L", (900, 900))
    d = ImageDraw.Draw(txt)
    center_text(draw=d, left=0, top=0, width=900, text=text_gamenumber, color=255, font=FONT_GAMENUMBER)
    w = txt.rotate(315, expand=True, resample=Image.BICUBIC)
    w_resize = w.resize((300, 300), Image.ANTIALIAS)
    bg.paste(w_resize, COORDS_GAME_NUM, w_resize)

    return bg


def generate_stats_bar(draw, stat, pref_value, other_value, pref_color, other_color):
    """ Used in conjunction with the stats_image function to draw the label & the actual
        value bars of each stat from the boxscore for each preferred & other teams.

    Args:
        draw: Current PIL draw Object
        stat: boxscore stat name (used for special coordinate cases)
        pref_value: value of the stat for the preferred team
        other_value: value of the stat for the other team
        pref_color: color of the value bar for the preferred team
        other_color: color of the value bar for the other team

    Returns:
        None (just draws a rectangle)
    """
    # Fonts used within the stats bar
    FONT_STAT_TITLE = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.STAT_TITLE)
    FONT_STAT_VALUE = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.STAT_VALUE)

    # Pre-game specific constant values (incl coordinates)
    STAT_TITLE_WIDTH = 240
    STAT_VALUE_SPACING = 15
    TOTAL_BAR_WIDTH = 445
    BAR_START_X = 278  # Arbitrary start number based on text label size
    BAR_END_X = 722
    CHART_START_X = 35
    CHART_START_Y = 150
    CHART_RECT_H = 55
    CHART_SEPARATOR = 35

    logging.info("Drawing stat bar for %s", stat)

    # Iterate over each possible type of passed stat
    if stat == StatTypes.SHOTS:
        stat_total = pref_value + other_value
        stat_title = f"SHOTS: {stat_total}"
    elif stat == StatTypes.BLOCKED_SHOTS:
        stat_total = pref_value + other_value
        stat_title = f"BLOCKED SHOTS: {stat_total}"
    elif stat == StatTypes.HITS:
        stat_total = pref_value + other_value
        stat_title = f"HITS: {stat_total}"
    elif stat == StatTypes.FACEOFF_PCT:
        stat_total = pref_value + other_value
        stat_title = f"FACEOFF %"
    elif stat == StatTypes.PENALTY_MINS:
        stat_total = pref_value + other_value
        stat_title = f"PENALTY MINUTES: {stat_total:.0f}"
    elif stat == StatTypes.POWER_PLAYS:
        pref_pp, pref_ppg = pref_value
        other_pp, other_ppg = other_value
        power_play_pref = f"{int(pref_ppg)} / {int(pref_pp)}"
        power_play_other = f"{int(other_ppg)} / {int(other_pp)}"
        pref_value = pref_pp
        other_value = other_pp
        stat_total = pref_pp + other_pp
        stat_title = f"POWER PLAYS: {int(stat_total)}"

    # fmt: off
    # Draws the stat label for the stat bar
    chart_top_y = CHART_START_Y + (stat.value * CHART_RECT_H) + (stat.value * CHART_SEPARATOR)
    center_text(
        draw=draw, left=CHART_START_X, top=chart_top_y, width=STAT_TITLE_WIDTH, text=stat_title,
        color=Colors.BLACK, font=FONT_STAT_TITLE, vertical=True, height=CHART_RECT_H,
    )

    # Draws the actual stat bar for both teams (proportioned correctly to the stat)
    # And also draws the stat value within the bar itself
    if stat_total == 0:
        stat_bar_pref_end_x = BAR_START_X + int(0.5 * TOTAL_BAR_WIDTH)
    else:
        stat_bar_pref_end_x = BAR_START_X + int((pref_value / stat_total) * TOTAL_BAR_WIDTH)

    draw.rectangle(
        ((BAR_START_X, chart_top_y), (stat_bar_pref_end_x, chart_top_y + CHART_RECT_H)),
        fill=pref_color['bg'], outline=(255, 255, 255), width=2
    )

    draw.rectangle(
        ((stat_bar_pref_end_x, chart_top_y), (BAR_END_X, chart_top_y + CHART_RECT_H)),
        fill=other_color['bg'], outline=(255, 255, 255), width=2
    )

    if pref_value > 0:
        # If Power Play stats are being printed, re-assign the stat value text
        pref_value = power_play_pref if stat == StatTypes.POWER_PLAYS else pref_value
        valign_center_text(
            draw=draw, left=(BAR_START_X + STAT_VALUE_SPACING), top=chart_top_y,
            height=CHART_RECT_H, text=str(pref_value), color=pref_color['text'], font=FONT_STAT_VALUE
        )

    if other_value > 0:
        # If Power Play stats are being printed, re-assign the stat value text
        other_value = power_play_other if stat == StatTypes.POWER_PLAYS else other_value
        valign_center_text(
            draw=draw, left=(stat_bar_pref_end_x + STAT_VALUE_SPACING), top=chart_top_y,
            height=CHART_RECT_H, text=str(other_value), color=other_color['text'], font=FONT_STAT_VALUE
        )

    # fmt: on


def draw_goal_text(draw, pref_other, number, goal, assist_p, assist_s, strength, period, time, team_color):
    """ Draws goal text (scorer & assists in the goals box).

    Args:
        TBD

    Returns:
        None
    """

    FONT_GOAL = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.GOAL_SCORER)
    FONT_TIME = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.GOAL_SCORER)
    FONT_ASST = ImageFont.truetype(FontFiles.BITTER_REGULAR, FontSizes.ASST_SCORER)

    # Instantiate shorter namespace for Constants
    c = Constants

    # Setup Goal Iterator (for spacing)
    goal_iter = number

    LEFT_OFFSET = 7
    HEIGHT = 35
    LEFT = c.GOALBOX_START_X + LEFT_OFFSET
    TOP = (
        c.GOALBOX_START_Y + c.GOALBOX_TEAM_H
        if pref_other == "pref"
        else c.GOALBOX_START_Y + c.GOALBOX_H + c.GOALBOX_SEPARATOR + c.GOALBOX_TEAM_H
    )

    # Draw Goal Scorer Text (Bold) & then get font size (to offset assists)
    TOP = TOP + (goal_iter * (10 + FontSizes.GOAL_SCORER))
    goal_text = f"{goal} - {strength}" if strength != "EVEN" else goal
    valign_center_text(draw=draw, left=LEFT, top=TOP, height=HEIGHT, text=goal_text, color=Colors.BLACK, font=FONT_GOAL)
    goal_w, _ = draw.textsize(goal_text, FONT_GOAL)

    # Generate assists texts (or unassisted) via list comprehension
    assist_p = " ".join(assist_p.split()[1:]) if assist_p else assist_p
    assist_s = " ".join(assist_s.split()[1:]) if assist_s else assist_s
    assists = [assist_p, assist_s]
    assists = [i for i in assists if i]
    assist_text = "Unassisted" if not assists else ", ".join(assists)
    assist_text = f"({assist_text})"

    # Draw assists text (non-bold) * then get font size (to offset time)
    valign_center_text(
        draw, LEFT + goal_w + 5, TOP, height=HEIGHT, text=assist_text, color=Colors.BLACK, font=FONT_ASST
    )
    asst_w, _ = draw.textsize(assist_text, FONT_ASST)

    # Generate time / period text & draw it
    time_period_text = f"[{time} / {period}]" if number < 7 else f"[{time} / {period}]   & MORE!"
    valign_center_text(
        draw, LEFT + goal_w + asst_w + 15, TOP, height=HEIGHT, text=time_period_text, color=team_color, font=FONT_TIME
    )


def stats_image(game: Game, game_end: bool, boxscore: dict):
    """ Generates the intermission & final image that contains bar chart starts & goal scorers.
        This is sent to social media platforms at each PERIOD_END & GAME_END event.

    Args:
        game: Current Game object
        boxscore: Boxscore of the game (for stats & goal scorers)

    Returns:
        bg: Finished Image instance
    """

    # Fonts used within the stats image
    FONT_TITLE = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.TITLE)
    FONT_RECORD = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.RECORD)
    FONT_DETAIL_LARGE = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.DETAIL_LARGE)
    FONT_DETAIL_SMALL = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.DETAIL_SMALL)
    FONT_GAMENUMBER = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.GAMENUMBER * 3)
    FONT_SCORE = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.SCORE)
    FONT_STAT_TITLE = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.STAT_TITLE)
    FONT_NO_GOAL = ImageFont.truetype(FontFiles.BITTER_BOLD, FontSizes.NO_GOAL_TEXT)

    # Pre-game specific constant values (incl coordinates)
    HEADER_TEXT = "END OF GAME RECAP!" if game_end else "INTERMISSION REPORT!"
    LOGO_Y = 110
    COORDS_HOME_X = 775
    COORDS_AWAY_X = 975
    LOGO_SCORE_SPACING = 50
    COORDS_HOME_LOGO = (COORDS_HOME_X, LOGO_Y)
    COORDS_AWAY_LOGO = (COORDS_AWAY_X, LOGO_Y)

    CHART_START_X = 35
    CHART_END_X = 725
    CHART_START_Y = 150
    CHART_RECT_H = 55
    CHART_SEPARATOR = 35
    CHART_GOAL_SEPARATOR = 40
    GOAL_START_Y = 200
    GOAL_SCORER_BOX_W = 400
    GOAL_SCORER_BOX_H = 220
    GOAL_SCORER_BOX_TEAM_H = 25
    GOAL_SCORE_BOX_W = 100
    GOAL_SCORER_BOX_SEPARATOR = 15

    # Setup Colors (via functions)
    pref_colors = team_colors(game.preferred_team.team_name)
    other_colors = team_colors(game.other_team.team_name)

    logging.debug("Pref Colors - %s // Other Colors - %s", pref_colors, other_colors)

    if pref_colors["primary"]["bg"] == other_colors["primary"]["bg"]:
        logging.info("Primary team colors are the same - swap other to secondary!")
        pref_colors = pref_colors["primary"]
        other_colors = other_colors["secondary"]
    else:
        pref_colors = pref_colors["primary"]
        other_colors = other_colors["primary"]

    # Load background & pasted resized logos
    bg = Image.open(Backgrounds.STATS)
    bg_w, bg_h = bg.size

    away_team = game.away_team.team_name.replace(" ", "")
    home_team = game.home_team.team_name.replace(" ", "")
    away_logo = Image.open(os.path.join(PROJECT_ROOT, f"resources/logos/{away_team}.png"))
    home_logo = Image.open(os.path.join(PROJECT_ROOT, f"resources/logos/{home_team}.png"))

    # Resize & paste the home / away logos with the mask the same as the image
    # TODO: Convert losing team to black & white (code snippet below)
    LOGO_RESIZE = (120, 120)
    home_logo.thumbnail(LOGO_RESIZE, Image.ANTIALIAS)
    away_logo.thumbnail(LOGO_RESIZE, Image.ANTIALIAS)
    bg.paste(away_logo, COORDS_AWAY_LOGO, away_logo)
    bg.paste(home_logo, COORDS_HOME_LOGO, home_logo)

    # if game.preferred_team.score > game.other_team.score:
    #     bg.paste(pref_logo, COORDS_PREF_LOGO, pref_logo)
    #     bg.paste(other_logo.convert('LA'), COORDS_OTHER_LOGO, other_logo)
    # else:
    #     bg.paste(pref_logo.convert('LA'), COORDS_PREF_LOGO, pref_logo)
    #     bg.paste(other_logo, COORDS_OTHER_LOGO, other_logo)

    # Generates a 'draw' object that we use to draw on top of the image
    draw = ImageDraw.Draw(bg)

    center_text(draw=draw, left=0, top=0, width=bg_w, text=HEADER_TEXT, color=Colors.WHITE, font=FONT_TITLE)

    # Draw the scores on the image
    # fmt:off
    center_text(
        draw=draw, left=COORDS_HOME_X + LOGO_SCORE_SPACING, top=LOGO_Y, width=190,
        text=str(game.home_team.score), color=Colors.WHITE, font=FONT_SCORE, vertical=True, height=FontSizes.SCORE
    )
    center_text(
        draw=draw, left=COORDS_AWAY_X + LOGO_SCORE_SPACING, top=LOGO_Y, width=190,
        text=str(game.away_team.score), color=Colors.WHITE, font=FONT_SCORE, vertical=True, height=FontSizes.SCORE
    )
    # fmt: on

    # Draw the boxes where Goal Scorers information goes
    draw.rectangle(
        (
            (725 + CHART_GOAL_SEPARATOR, GOAL_START_Y),
            (725 + CHART_GOAL_SEPARATOR + GOAL_SCORER_BOX_W, GOAL_START_Y + GOAL_SCORER_BOX_H),
        ),
        fill=(255, 255, 255),
    )
    draw.rectangle(
        (
            (725 + CHART_GOAL_SEPARATOR, GOAL_START_Y),
            (725 + CHART_GOAL_SEPARATOR + GOAL_SCORER_BOX_W, GOAL_START_Y + GOAL_SCORER_BOX_TEAM_H),
        ),
        fill=pref_colors["bg"],
    )
    draw.rectangle(
        (
            (725 + CHART_GOAL_SEPARATOR, GOAL_START_Y + GOAL_SCORER_BOX_SEPARATOR + GOAL_SCORER_BOX_H),
            (
                725 + CHART_GOAL_SEPARATOR + GOAL_SCORER_BOX_W,
                GOAL_START_Y + 2 * GOAL_SCORER_BOX_H + GOAL_SCORER_BOX_SEPARATOR,
            ),
        ),
        fill=(255, 255, 255),
    )
    draw.rectangle(
        (
            (725 + CHART_GOAL_SEPARATOR, GOAL_START_Y + GOAL_SCORER_BOX_SEPARATOR + GOAL_SCORER_BOX_H),
            (
                725 + CHART_GOAL_SEPARATOR + GOAL_SCORER_BOX_W,
                GOAL_START_Y + GOAL_SCORER_BOX_H + GOAL_SCORER_BOX_SEPARATOR + GOAL_SCORER_BOX_TEAM_H,
            ),
        ),
        fill=other_colors["bg"]
    )

    # fmt: off
    center_text(
        draw=draw, left=725 + CHART_GOAL_SEPARATOR, top=GOAL_START_Y, width=GOAL_SCORER_BOX_W,
        text=f"{game.preferred_team.tri_code} GOALS", color=pref_colors["text"], font=FONT_STAT_TITLE,
        vertical=True, height=GOAL_SCORER_BOX_TEAM_H,
    )
    center_text(
        draw=draw, left=725 + CHART_GOAL_SEPARATOR, top=GOAL_START_Y + GOAL_SCORER_BOX_SEPARATOR + GOAL_SCORER_BOX_H,
        width=GOAL_SCORER_BOX_W, text=f"{game.other_team.tri_code} GOALS", color=other_colors["text"],
        font=FONT_STAT_TITLE, vertical=True, height=GOAL_SCORER_BOX_TEAM_H)
    # fmt: on

    # Draw the stats base chart rectangles
    for i in range(6):
        CHART_TOP_Y = CHART_START_Y + (i * CHART_RECT_H) + (i * CHART_SEPARATOR)
        CHART_BOTTOM_Y = CHART_START_Y + ((i + 1) * CHART_RECT_H) + (i * CHART_SEPARATOR)
        draw.rectangle(((CHART_START_X, CHART_TOP_Y), (CHART_END_X, CHART_BOTTOM_Y)), fill=Colors.WHITE)

    # Get the boxscores for each team (via the homeaway variable)
    boxscore_pref = boxscore["teams"][game.preferred_team.home_away]
    boxscore_other = boxscore["teams"][game.other_team.home_away]
    preferred_stats = boxscore_pref["teamStats"]["teamSkaterStats"]
    other_stats = boxscore_other["teamStats"]["teamSkaterStats"]

    # fmt: off
    # Generate each stats bar via the function & box score
    # Shots, Blocked, Hits & FO% are always there with no logic necessary
    generate_stats_bar(
        draw=draw, stat=StatTypes.SHOTS, pref_value=preferred_stats["shots"],
        other_value=other_stats["shots"], pref_color=pref_colors, other_color=other_colors
    )

    generate_stats_bar(
        draw=draw, stat=StatTypes.BLOCKED_SHOTS, pref_value=preferred_stats["blocked"],
        other_value=other_stats["blocked"], pref_color=pref_colors, other_color=other_colors
    )

    generate_stats_bar(
        draw=draw, stat=StatTypes.HITS, pref_value=preferred_stats["hits"],
        other_value=other_stats["hits"], pref_color=pref_colors, other_color=other_colors
    )

    generate_stats_bar(
        draw=draw, stat=StatTypes.FACEOFF_PCT, pref_value=float(preferred_stats["faceOffWinPercentage"]),
        other_value=float(other_stats["faceOffWinPercentage"]), pref_color=pref_colors, other_color=other_colors
    )

    generate_stats_bar(
        draw=draw, stat=StatTypes.PENALTY_MINS, pref_value=preferred_stats["pim"],
        other_value=other_stats["pim"], pref_color=pref_colors, other_color=other_colors
    )

    # Power Plays takes a tuple instead of single values (opporunities & goals)
    pref_pp = (preferred_stats["powerPlayOpportunities"], preferred_stats["powerPlayGoals"])
    other_pp = (other_stats["powerPlayOpportunities"], other_stats["powerPlayGoals"])
    generate_stats_bar(
        draw=draw, stat=StatTypes.POWER_PLAYS, pref_value=pref_pp,
        other_value=other_pp, pref_color=pref_colors, other_color=other_colors
    )

    # Loop through preferred goals (unless there are none)
    if not game.pref_goals:
        center_text(
            draw, Constants.GOALBOX_START_X, top=Constants.GOALBOX_START_Y, width=Constants.GOALBOX_W,
            text="NO GOALS!", color=Colors.GRAY, font=FONT_NO_GOAL, vertical=True, height=Constants.GOALBOX_H,
        )

    for idx, goal in enumerate(game.pref_goals):
        period = goal.period_ordinal
        time = goal.period_time_remain_str
        strength = goal.strength_code
        goal_scorer = goal.scorer_name
        assist_primary = goal.primary_name
        assist_secondary = goal.secondary_name

        draw_goal_text(
            draw=draw, pref_other="pref", number=idx, goal=goal_scorer, assist_p=assist_primary,
            assist_s=assist_secondary, strength=strength, period=period, time=time, team_color=pref_colors["bg"],
        )

    # Loop through other goals (unless there are none)
    if not game.pref_goals:
        TOP = Constants.GOALBOX_START_Y + Constants.GOALBOX_H + Constants.GOALBOX_SEPARATOR
        center_text(
            draw, Constants.GOALBOX_START_X, top=TOP, width=Constants.GOALBOX_W,
            text="NO GOALS!", color=Colors.GRAY, font=FONT_NO_GOAL, vertical=True, height=Constants.GOALBOX_H,
        )

    for idx, goal in enumerate(game.other_goals):
        period = goal.period_ordinal
        time = goal.period_time_remain_str
        strength = goal.strength_code
        goal_scorer = goal.scorer_name
        assist_primary = goal.primary_name
        assist_secondary = goal.secondary_name

        draw_goal_text(
            draw=draw, pref_other="other", number=idx, goal=goal_scorer, assist_p=assist_primary,
            assist_s=assist_secondary, strength=strength, period=period, time=time, team_color=other_colors["bg"],
        )
    # fmt: on

    bg.show()
