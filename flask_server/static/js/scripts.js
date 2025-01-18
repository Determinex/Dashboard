/**
 * Plays the previous track in the playlist.
 */
prevTrack() {
  try {
    if (this.currentTrackIndex > 0) {
      this.setTrack(this.currentTrackIndex - 1);
    }
  } catch (error) {
    console.error('Error going to previous track:', error);
  }
},

/**
 * Plays the next track in the playlist.
 */
nextTrack() {
  try {
    if (this.currentTrackIndex < this.tracks.length - 1) {
      this.setTrack(this.currentTrackIndex + 1);
    }
  } catch (error) {
    console.error('Error going to next track:', error);
  }
},

/**
 * Changes the current track to the specified audio source and album art.
 * @param {string} audioSrc - The source URL of the audio file.
 * @param {string} albumArtSrc - The source URL of the album art image.
 */
changeTrack(audioSrc, albumArtSrc) {
  try {
    this.audioPlayer.src = audioSrc;
    document.getElementById('albumArt').style.backgroundImage = `url(${albumArtSrc})`;
    this.audioPlayer.play();
  } catch (error) {
    console.error('Error changing track:', error);
  }
},

/**
 * Sets the current track to the specified index in the playlist.
 * @param {number} index - The index of the track to set.
 */
setTrack(index) {
  if (index >= 0 && index < this.tracks.length) {
    this.currentTrackIndex = index;
    const { file, albumArt } = this.tracks[index];
    this.changeTrack(file, albumArt);
  }
},

  /**
   * Fetches the playlist from an XML file and populates the playlist element.
   */
  fetchPlaylist() {
    fetch('media/playlist.xml')
      .then(response => response.text())
      .then(data => {
        try {
          const parser = new DOMParser();
          const xmlDoc = parser.parseFromString(data, 'text/xml');
          const tracks = xmlDoc.getElementsByTagName('track');
          this.playlist.innerHTML = '';
          this.tracks = [];
          for (let i = 0; i < tracks.length; i++) {
            const title = tracks[i].getElementsByTagName('title')[0].textContent;
            const file = tracks[i].getElementsByTagName('file')[0].textContent;
            const albumArt = tracks[i].getElementsByTagName('albumArt')[0].textContent;
            const track = document.createElement('div');
            track.className = 'playlist-item';
            track.textContent = title;
            track.dataset.src = file;
            track.dataset.albumArt = albumArt;
            track.onclick = () => this.changeTrack(file, albumArt);
            this.playlist.appendChild(track);
            this.tracks.push({ title, file, albumArt });
          }
        } catch (error) {
          console.error('Error parsing playlist XML:', error);
        }
      })
      .catch(error => console.error('Error fetching playlist:', error));
  },

  /**
   * Sets the current track to the specified index in the playlist.
   * @param {number} index - The index of the track to set.
   */
  setTrack(index) {
    if (index >= 0 && index < this.tracks.length) {
      this.currentTrackIndex = index;
      this.changeTrack(this.tracks[index].file, this.tracks[index].albumArt);
    }
  },