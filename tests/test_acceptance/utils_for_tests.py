#!/usr/bin/env python

"""
Helper functions for tests:
- function for filtring data in rules_*_data.py files.
"""

def filter_reactions(tags, data_set):
    """
    Filters reactions from MAPK_DATA according to given list of tags.
    """
    filtered_reactions = {}
    tags = set([str(tag).lower() for tag in tags])

    for reaction in data_set:
        reaction_tags = set([str(tag).lower() for tag in data_set[reaction]['Tags']])
        if tags.issubset(reaction_tags):
            filtered_reactions[reaction] = data_set[reaction]
    return filtered_reactions

def filter_exclude_reactions(tags, data_set):
    """
    Filters reactions from MAPK_DATA according to given list of tags.
    Exclude reactions with given tags.
    """
    filtered_reactions = {}
    tags = set([str(tag).lower() for tag in tags])

    for reaction in data_set:
        reaction_tags = set([str(tag).lower() for tag in data_set[reaction]['Tags']])
        if not tags.issubset(reaction_tags):
            filtered_reactions[reaction] = data_set[reaction]
    return filtered_reactions