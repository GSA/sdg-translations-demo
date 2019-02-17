"""
Build multiple demos of Open SDG implementations, using all available languages.

After running this script, the demos should be available in a 'builds' folder.
"""

import fileinput
import os
import shutil
import glob
import sys
import subprocess
import yaml
from git import Repo

languages = [
    'en',
    'es',
    'fr',
    'ru',
    'ar',
    'zh-Hans',
    'am',
    'de',
]

demos = {
    'us': 'https://github.com/GSA/sdg-indicators-usa',
    'uk': 'https://github.com/ONSDigital/sdg-indicators',
}

for abbrev in demos:
    # Clone the site repository.
    site_folder = os.path.join('repos', abbrev)
    Repo.clone_from(demos[abbrev], site_folder)
    # Load the Jekyll configuration.
    config_file = os.path.join(site_folder, '_config.yml')
    with open(config_file, 'r') as stream:
        yamldata = (yaml.load(stream))
    # Set a new baseurl to match this project's name.
    yamldata['baseurl'] = '/sdg-translation-demo/' + abbrev
    # Point to the latest sdg-translations data.
    for item in yamldata['jekyll_get_data']:
        if item['data'] == 'translations':
            item['json'] = 'https://gsa.github.io/sdg-translations/translations.json'
    # Enable all languages.
    yamldata['languages'] = languages
    # Create any missing language files.
    for language in languages:
        if language == 'en':
            continue
        # We only care about these three Jekyll folders.
        for jekyll_folder in ['_indicators', '_goals', '_pages']:
            old_folder = os.path.join(site_folder, jekyll_folder)
            new_folder = os.path.join(old_folder, language)
            # Abort if folder already exists.
            if os.path.isdir(new_folder):
                continue
            # Create the folder.
            os.mkdir(new_folder)
            # Copy all files (but no folders) into the new folder.
            for filename in os.listdir(old_folder):
                source_file = os.path.join(old_folder, filename)
                new_file = os.path.join(new_folder, filename)
                if os.path.isdir(source_file):
                    continue
                shutil.copyfile(source_file, new_file)
            # Change the copied files to reflect the new language.
            for line in fileinput.input(glob.glob(new_folder + '/*'), inplace=True):
                # Skip a few unnecessary lines.
                if jekyll_folder == '_goals' and line.startswith('title:'):
                    continue
                if jekyll_folder == '_goals' and line.startswith('short:'):
                    continue
                if jekyll_folder == '_goals' and line.startswith(' '):
                    continue
                # Look for the permalink line, and add the language.
                if line.startswith('permalink: /'):
                    sys.stdout.write(line.replace('permalink: /', 'permalink: /' + language + '/'))
                    sys.stdout.write('language: ' + language + '\n')
                else:
                    sys.stdout.write(line)
