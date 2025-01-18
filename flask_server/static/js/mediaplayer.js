const MP3Player = {
    audioPlayer: new Audio(),
    playButton: document.getElementById('playButton'),
    pauseButton: document.getElementById('pauseButton'),
    muteButton: document.getElementById('muteButton'),
    volumeButton: document.getElementById('volumeButton'),
    shuffleButton: document.getElementById('shuffleButton'),
    repeatButton: document.getElementById('repeatButton'),
    playlistElement: document.getElementById('playlist'),
    currentTrackIndex: 0,
    playlist: [],
    isShuffling: false,
    repeatMode: 'none', // 'none', 'one', 'all'

    playAudio() {
      try {
        this.audioPlayer.play();
      } catch (error) {
        console.error('Error playing audio:', error);
      }
    },

    pauseAudio() {
      try {
        this.audioPlayer.pause();
      } catch (error) {
        console.error('Error pausing audio:', error);
      }
    },

    setTrack(index) {
      if (index >= 0 && index < this.playlist.length) {
        this.currentTrackIndex = index;
        const { file, albumArt } = this.playlist[index];
        this.changeTrack(file, albumArt);
      }
    },

    changeTrack(audioSrc, albumArtSrc) {
      try {
        this.audioPlayer.src = `/static/media/${audioSrc}`;
        document.getElementById('albumArt').innerHTML = `<img src="/static/media/${albumArtSrc}" alt="Album Art" style="max-width: 100%;">`;
        this.playAudio();
      } catch (error) {
        console.error('Error changing track:', error);
      }
    },

    prevTrack() {
      try {
        if (this.currentTrackIndex > 0) {
          this.setTrack(this.currentTrackIndex - 1);
        }
      } catch (error) {
        console.error('Error going to previous track:', error);
      }
    },

    nextTrack() {
      try {
        if (this.isShuffling) {
          this.setTrack(Math.floor(Math.random() * this.playlist.length));
        } else if (this.currentTrackIndex < this.playlist.length - 1) {
          this.setTrack(this.currentTrackIndex + 1);
        } else if (this.repeatMode === 'all') {
          this.setTrack(0);
        }
      } catch (error) {
        console.error('Error going to next track:', error);
      }
    },

    togglePlayPause() {
      try {
        if (this.audioPlayer.paused) {
          this.playButton.style.display = 'none';
          this.pauseButton.style.display = 'inline-block';
          this.playAudio();
        } else {
          this.playButton.style.display = 'inline-block';
          this.pauseButton.style.display = 'none';
          this.pauseAudio();
        }
      } catch (error) {
        console.error('Error toggling play/pause:', error);
      }
    },

    toggleMute() {
      try {
        this.audioPlayer.muted = !this.audioPlayer.muted;
        this.updateMuteButton();
      } catch (error) {
        console.error('Error toggling mute:', error);
      }
    },

    setVolume(volume) {
      try {
        this.audioPlayer.volume = volume;
        this.updateMuteButton();
      } catch (error) {
        console.error('Error setting volume:', error);
      }
    },

    updateMuteButton() {
      try {
        if (this.audioPlayer.muted) {
          this.muteButton.style.display = 'inline-block';
          this.volumeButton.style.display = 'none';
        } else {
          this.muteButton.style.display = 'none';
          this.volumeButton.style.display = 'inline-block';
        }
      } catch (error) {
        console.error('Error updating mute button:', error);
      }
    },

    toggleShuffle() {
      this.isShuffling = !this.isShuffling;
      this.shuffleButton.classList.toggle('active', this.isShuffling);
      if (this.isShuffling) {
        this.shufflePlaylist();
      } else {
        this.fetchPlaylist(); // Reset to original order if shuffle is turned off
      }
    },

    shufflePlaylist() {
      const currentTrack = this.playlist[this.currentTrackIndex];
      const remainingTracks = this.playlist.filter((_, index) => index !== this.currentTrackIndex);
      for (let i = remainingTracks.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [remainingTracks[i], remainingTracks[j]] = [remainingTracks[j], remainingTracks[i]];
      }
      this.playlist = [currentTrack, ...remainingTracks];
      this.renderPlaylist();
    },

    renderPlaylist() {
      this.playlistElement.innerHTML = '';
      this.playlist.forEach((track, index) => {
        const trackElement = document.createElement('div');
        trackElement.className = 'playlist-item';
        trackElement.textContent = track.title;
        trackElement.dataset.src = track.file;
        trackElement.dataset.albumArt = track.albumArt;
        trackElement.onclick = () => this.setTrack(index);
        this.playlistElement.appendChild(trackElement);
      });
    },

    toggleRepeatMode() {
      if (this.repeatMode === 'none') {
        this.repeatMode = 'one';
        this.repeatButton.innerHTML = '<i class="fas fa-redo"></i><span class="fa-repeat-1">1</span>';
        this.repeatButton.classList.add('active');
      } else if (this.repeatMode === 'one') {
        this.repeatMode = 'all';
        this.repeatButton.innerHTML = '<i class="fas fa-redo"></i>';
        this.repeatButton.classList.add('active');
      } else {
        this.repeatMode = 'none';
        this.repeatButton.innerHTML = '<i class="fas fa-redo"></i>';
        this.repeatButton.classList.remove('active');
      }
    },

    fetchPlaylist() {
      fetch('/static/media/playlist.xml')
        .then(response => response.text())
        .then(data => {
          try {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(data, 'text/xml');
            const tracks = xmlDoc.getElementsByTagName('track');
            this.playlistElement.innerHTML = '';
            this.playlist = [];
            for (let i = 0; i < tracks.length; i++) {
              const title = tracks[i].getElementsByTagName('title')[0].textContent;
              const file = tracks[i].getElementsByTagName('file')[0].textContent;
              const albumArt = tracks[i].getElementsByTagName('albumArt')[0].textContent;
              const track = document.createElement('div');
              track.className = 'playlist-item';
              track.textContent = title;
              track.dataset.src = file;
              track.dataset.albumArt = albumArt;
              track.onclick = () => this.setTrack(i);
              this.playlistElement.appendChild(track);
              this.playlist.push({ title, file, albumArt });
            }
            console.log('Playlist fetched and parsed successfully.');
          } catch (error) {
            console.error('Error parsing playlist XML:', error);
          }
        })
        .catch(error => console.error('Error fetching playlist:', error));
    },

    initialize() {
      try {
        this.fetchPlaylist();
        this.playButton.addEventListener('click', () => {
          if (!this.audioPlayer.src) {
            this.setTrack(0); // Set the first track if no track is set
          }
          this.togglePlayPause();
        });
        this.pauseButton.addEventListener('click', () => this.togglePlayPause());
        this.muteButton.addEventListener('click', () => this.toggleMute());
        this.volumeButton.addEventListener('click', () => this.toggleMute());
        this.shuffleButton.addEventListener('click', () => this.toggleShuffle());
        this.repeatButton.addEventListener('click', () => this.toggleRepeatMode());
        document.getElementById('prevTrack').addEventListener('click', () => this.prevTrack());
        document.getElementById('nextTrack').addEventListener('click', () => this.nextTrack());

        // Sync play/pause button states with audio element controls
        this.audioPlayer.addEventListener('play', () => {
          this.playButton.style.display = 'none';
          this.pauseButton.style.display = 'inline-block';
        });
        this.audioPlayer.addEventListener('pause', () => {
          this.playButton.style.display = 'inline-block';
          this.pauseButton.style.display = 'none';
        });

        // Sync mute/unmute button states with audio element controls
        this.audioPlayer.addEventListener('volumechange', () => {
          this.updateMuteButton();
        });

        // Handle track end event
        this.audioPlayer.addEventListener('ended', () => {
          if (this.repeatMode === 'one') {
            this.playAudio();
          } else {
            this.nextTrack();
          }
        });

        // Initialize mute button state
        this.updateMuteButton();
      } catch (error) {
        console.error('Error initializing MP3 player:', error);
      }
    }
  };

  document.addEventListener('DOMContentLoaded', () => {
    MP3Player.initialize();

    // Accordion functionality
    const accordions = document.getElementsByClassName('accordion');
    for (let i = 0; i < accordions.length; i++) {
      accordions[i].addEventListener('click', function() {
        this.classList.toggle('active');
        const panel = this.nextElementSibling;
        if (panel.style.display === 'block') {
          panel.style.display = 'none';
        } else {
          panel.style.display = 'block';
        }
      });
    }
  });