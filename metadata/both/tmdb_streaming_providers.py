import requests

# Variables (easy to configure)
API_KEY = "e2782ca426c18a84ad8a10ee08cfe155"  # TMDb API key
COUNTRY_CODE = "FR"  # Edit this to use another country code (e.g., "US")
FILE_NAME = "README.md"  # The output markdown file name

# Fetch providers for a specific type (movie or tv)
def fetch_providers(media_type, country=COUNTRY_CODE):
    url = f"https://api.themoviedb.org/3/watch/providers/{media_type}"
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "watch_region": country
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error: Unable to fetch {media_type} providers. Status Code: {response.status_code}")
        return []

# Combine and export providers
def export_providers_to_markdown(movie_providers, tv_providers, country, file_name=FILE_NAME):
    provider_map = {}

    # Add movie providers to the map
    for provider in movie_providers:
        provider_id = provider["provider_id"]
        provider_name = provider["provider_name"]
        if provider_id not in provider_map:
            provider_map[provider_id] = {"name": provider_name, "movies": "Yes", "tv": "No"}
        else:
            provider_map[provider_id]["movies"] = "Yes"

    # Add TV providers to the map
    for provider in tv_providers:
        provider_id = provider["provider_id"]
        provider_name = provider["provider_name"]
        if provider_id not in provider_map:
            provider_map[provider_id] = {"name": provider_name, "movies": "No", "tv": "Yes"}
        else:
            provider_map[provider_id]["tv"] = "Yes"

    # Prepare markdown content
    lines = [
        f"# Streaming Providers in {country.upper()}\n\n",
        "This table lists all streaming providers available in France, their TMDb IDs, and whether they support movies, TV shows, or both.\n\n",
        "Script is working with any country. Just edit with desired country code and run.\n\n",
        "Requirement: TMDb API key\n\n",
        "| Provider Name         | Provider ID | Movies   | TV       |\n",
        "|-----------------------|-------------|----------|----------|\n"
    ]
    for provider_id, details in sorted(provider_map.items(), key=lambda x: x[1]["name"]):
        lines.append(f"| {details['name']:<21} | {provider_id:<11} | {details['movies']:<8} | {details['tv']:<8} |\n")

    # Write to markdown file
    with open(file_name, "w") as file:
        file.writelines(lines)

    print(f"Results exported to {file_name}")

# Fetch movie and TV providers
movie_providers = fetch_providers("movie", country=COUNTRY_CODE)
tv_providers = fetch_providers("tv", country=COUNTRY_CODE)

# Export to Markdown
export_providers_to_markdown(movie_providers, tv_providers, country=COUNTRY_CODE)
