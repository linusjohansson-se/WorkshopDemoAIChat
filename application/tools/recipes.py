import requests
from langchain_core.tools import tool

@tool
def fetch_recipes():
    """Fetch all available recipes"""
    response = requests.get("https://dummyjson.com/recipes")

    return response.content

@tool
def fetch_recipe_tags():
    """Fetch all available recipe tags"""
    response = requests.get("https://dummyjson.com/recipes/tags")

    return response.content

@tool
def get_recipe_by_tag(tag: str):
    """Fetch all recipes for a specific tag"""
    response = requests.get(f"https://dummyjson.com/recipes/tag/{tag}")

    return response.content