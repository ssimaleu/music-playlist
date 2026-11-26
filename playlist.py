"""Playlist Manager — a tiny music library for managing songs and playlists.

Run as a CLI:
    python playlist.py add "Song Title" "Artist" 215
    python playlist.py list
    python playlist.py total
"""
from dataclasses import dataclass
import json
import sys


@dataclass
class Song:
    title: str
    artist: str
    duration_sec: int  # length in seconds

    def duration_str(self) -> str:
        """Format duration as M:SS (e.g. 215 -> '3:35')."""
        minutes, seconds = divmod(self.duration_sec, 60)
        return f"{minutes}:{seconds:02d}"


class Playlist:
    def __init__(self, name: str = "My Playlist"):
        self.name = name
        self.songs: list[Song] = []

    def add_song(self, song: Song) -> None:
        """Add a song to the playlist."""
        if song.duration_sec < 0:
            raise ValueError("Duration cannot be negative")
        self.songs.append(song)

    def total_duration_sec(self) -> int:
        """Total playtime of all songs, in seconds."""
        return sum(s.duration_sec for s in self.songs)

    def total_duration_str(self) -> str:
        return Song("total", "", self.total_duration_sec()).duration_str()

    def by_artist(self, artist: str) -> list[Song]:
        """Return songs by a given artist (case-insensitive)."""
        return [s for s in self.songs if s.artist.lower() == artist.lower()]

    def sorted_by_duration(self) -> list[Song]:
        """Return songs sorted by duration, shortest first."""
        return sorted(self.songs, key=lambda s: s.duration_sec)

    def to_json(self) -> str:
        return json.dumps(
            [{"title": s.title, "artist": s.artist, "duration_sec": s.duration_sec}
             for s in self.songs], indent=2)


def main() -> None:
    pl = Playlist()
    if len(sys.argv) < 2:
        print("Usage: playlist.py <add|list|total> [args]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) == 5:
        pl.add_song(Song(sys.argv[2], sys.argv[3], int(sys.argv[4])))
        print(pl.to_json())
    elif cmd == "total":
        print(pl.total_duration_str())
    else:
        print("Commands: add <title> <artist> <seconds> | total")
        sys.exit(1)


if __name__ == "__main__":
    main()
