#!/usr/bin/env python3
"""Playlist Manager — graphical interface (Tkinter).

Run with:  python3 gui.py
"""
import tkinter as tk
from tkinter import ttk, messagebox

from playlist import Playlist, Song


class PlaylistApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎵 Playlist Manager")
        self.geometry("560x420")
        self.playlist = Playlist("My Playlist")

        self._build_add_form()
        self._build_song_list()
        self._build_footer()

    # --- UI construction -------------------------------------------------
    def _build_add_form(self):
        form = ttk.LabelFrame(self, text="Add a song", padding=10)
        form.pack(fill="x", padx=12, pady=(12, 6))

        ttk.Label(form, text="Title").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(form, width=24)
        self.title_entry.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(form, text="Artist").grid(row=0, column=2, sticky="w")
        self.artist_entry = ttk.Entry(form, width=20)
        self.artist_entry.grid(row=0, column=3, padx=6, pady=4)

        ttk.Label(form, text="Duration (sec)").grid(row=0, column=4, sticky="w")
        self.duration_entry = ttk.Entry(form, width=8)
        self.duration_entry.grid(row=0, column=5, padx=6, pady=4)

        ttk.Button(form, text="➕ Add", command=self.add_song).grid(
            row=0, column=6, padx=(10, 0))

    def _build_song_list(self):
        frame = ttk.LabelFrame(self, text="Playlist", padding=10)
        frame.pack(fill="both", expand=True, padx=12, pady=6)

        columns = ("title", "artist", "duration")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        self.tree.heading("title", text="Title")
        self.tree.heading("artist", text="Artist")
        self.tree.heading("duration", text="Duration")
        self.tree.column("title", width=240)
        self.tree.column("artist", width=180)
        self.tree.column("duration", width=80, anchor="e")
        self.tree.pack(fill="both", expand=True)

    def _build_footer(self):
        footer = ttk.Frame(self, padding=10)
        footer.pack(fill="x")
        self.total_label = ttk.Label(footer, text="Total: 0:00", font=("TkDefaultFont", 11, "bold"))
        self.total_label.pack(side="left")
        ttk.Button(footer, text="Sort by duration",
                   command=self.sort_by_duration).pack(side="right")
        ttk.Button(footer, text="Remove selected",
                   command=self.remove_selected).pack(side="right", padx=8)

    # --- Actions ----------------------------------------------------------
    def add_song(self):
        title = self.title_entry.get().strip()
        artist = self.artist_entry.get().strip()
        raw = self.duration_entry.get().strip()
        if not title or not artist:
            messagebox.showwarning("Missing fields", "Title and artist are required.")
            return
        try:
            duration = int(raw)
        except ValueError:
            messagebox.showerror("Invalid duration", "Duration must be a whole number of seconds.")
            return
        try:
            self.playlist.add_song(Song(title, artist, duration))
        except ValueError as err:
            messagebox.showerror("Error", str(err))
            return
        self.title_entry.delete(0, tk.END)
        self.artist_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.refresh()

    def remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        index = self.tree.index(selected[0])
        del self.playlist.songs[index]
        self.refresh()

    def sort_by_duration(self):
        self.playlist.songs = self.playlist.sorted_by_duration()
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for song in self.playlist.songs:
            self.tree.insert("", tk.END, values=(song.title, song.artist, song.duration_str()))
        self.total_label.config(text=f"Total: {self.playlist.total_duration_str()}")


if __name__ == "__main__":
    PlaylistApp().mainloop()
