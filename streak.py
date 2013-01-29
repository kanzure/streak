# -*- coding: utf-8 -*-
"""
Streaks all over the repo.
"""

import os
import sys
import datetime
from PIL import Image

def pixel2bit(pixel, threshold=1):
    """
    Convert the pixel value to a bit.
    """
    if pixel != 0:
        return 1
    else:
        return 0

def pixels2bitmap(pixels, width=52, height=7):
    """
    Converts an image to a dictionary of weeks each with a dictionary of days.
    """
    weeks = {}
    for week in range(width):
        days = {}
        for day in range(height):
            days[day] = pixel2bit(pixels[week, day])
        weeks[week] = days
    return weeks

def bitmap2calendar(bitmap, start_date=None, end_date=None):
    """
    Returns a list of dates given a bitmap of weeks of days.
    """
    if not end_date:
        end_date = datetime.datetime.now()

    if not start_date:
        start_date = datetime.datetime.now() - datetime.timedelta(days=365)

    calendar = []
    current_date = start_date
    calendar.append(current_date)

    for week in bitmap.keys():
        for day in bitmap[week].keys():
            if bitmap[week][day] > 0:
                calendar.append(current_date)
            current_date += datetime.timedelta(days=1)

    return calendar

def print_row(bitmap, row_id):
    """
    Displays a line of text.
    """
    for week in range(52):
        if bitmap[week][row_id] > 0:
            sys.stdout.write("*")
        else:
            sys.stdout.write(" ")
    sys.stdout.write("\n")

def print_rows(bitmap):
    """
    Shows the banner.
    """
    print "Commencing streaking.."
    for row in range(7):
        print_row(bitmap, row)

def print_dates(calendar):
    """
    Just shows a list of dates.
    """
    for date in calendar:
        print date.strftime("%Y-%m-%d")

def git_barf(datestamp, commits=100, message="HTTP 418 I'm a teapot"):
    """
    Spoofs commits for a certain date.
    """
    git_author_date = datestamp.strftime("%a %b %d 02:00:00 %Y -700")
    for commit in range(commits):
        cmd = "export GIT_AUTHOR_DATE=\"" + git_author_date + "\"; "
        cmd += "export GIT_COMMITTER_DATE=\"" + git_author_date + "\"; "
        cmd += "git commit --allow-empty -m \"" + message + "\""
        os.system(cmd)

def calendar_barf(dates, commits=100):
    """
    Barfs on all of the dates. Makes lots of git commits. Destroys a git repo.
    """
    for date in dates:
        git_barf(date, commits=commits)

def load_bitmap(file_path):
    """
    Loads a 52x7 1-bit bitmap, then returns a histogram of dates.
    """
    image = Image.open(file_path)
    pixels = image.load()

    bitmap = pixels2bitmap(pixels)
    print_rows(bitmap)

    calendar = bitmap2calendar(bitmap)
    return calendar

if __name__ == "__main__":
    calendar = load_bitmap("input.bmp")
    # print_dates(calendar)

    calendar_barf(calendar)

