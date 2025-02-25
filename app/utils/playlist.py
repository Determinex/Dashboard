import os
import xml.etree.ElementTree as ET
import eyed3

def generate_playlist_xml(directory, output_file):
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    playlist = ET.Element('playlist')

    for filename in os.listdir(directory):
        if filename.endswith('.mp3'):
            file_path = os.path.join(directory, filename)
            audiofile = eyed3.load(file_path)
            
            # Extract metadata
            title = audiofile.tag.title if audiofile.tag.title else os.path.splitext(filename)[0]
            artist = audiofile.tag.artist if audiofile.tag.artist else 'Unknown Artist'
            album_artist = audiofile.tag.album_artist if audiofile.tag.album_artist else None

            if artist and album_artist and artist != album_artist:
                artist = f"{artist} / {album_artist}"
            elif not artist and album_artist:
                artist = album_artist
            elif not artist:
                artist = 'Unknown Artist'
                print(f"No artist information found for file: {filename}")

            track = ET.SubElement(playlist, 'track')
            title_element = ET.SubElement(track, 'title')
            title_element.text = title
            artist_element = ET.SubElement(track, 'artist')
            artist_element.text = artist
            file_element = ET.SubElement(track, 'file')
            file_element.text = filename
            albumArt = ET.SubElement(track, 'albumArt')
            albumArt.text = 'default-album-art.jpg'
    tree = ET.ElementTree(playlist)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Playlist XML generated successfully at '{output_file}'.")

# Usage
script_dir = os.path.dirname(__file__)
media_dir = os.path.join(script_dir, '..', 'static', 'media')
output_file = os.path.join(media_dir, 'playlist.xml')
generate_playlist_xml(media_dir, output_file)