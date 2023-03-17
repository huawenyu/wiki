# Plex Music - Folder Structure & Naming

## Recognized Tags

If the Album Artist tag is not present, then Plex will try to treat the file as though it is a
part of a Various Artists album. You should be aware that Plex does not always use the Artist
tag to determine the actual artist, this is why the Album Artist tag is important and must be
present for all tracks that are not a part of a Various Artists album.

**Plex does not use all possible tags. Tags that Plex uses:**

1. Artist
2. Album Artist (leave blank for Various Artist albums only, must be included in all other tracks)
3. Album
4. Title
5. Year
6. Genre
7. Track Number
8. Cover Art


## Supplying Personal Artwork

You can supply your own artist photos, artist backdrops and album backdrops.
This however requires that your music files are organised in a folder structure like this:

```
Music/
    ./Albumartistname/
        artist-poster.jpg             # a photo of the artist
        artist-background.jpg         # a background/wallpaper particular to the artist
        ./Albumartistname - Albumtitle/  # [if not present, inherited from the 'albumartist' level]
            cover.jpg                 # album cover
            background.jpg            # album background/wallpaper
            1. Trackartist - Tracktitle.mp3
            1. Trackartist - Tracktitle.txt
            2. Trackartist - Tracktitle.mp3
            2. Trackartist - Tracktitle.lrc
```

# Multi_Disc

## Multi-Disk Albums

**Follow this Naming Scheme**

```
    ./Artist/
        ./Albumartist - Albumtitle/
            ./Disc 1/
                trackartist - tracktitle.mp3
                trackartist - tracktitle.mp3
            ./Disc 2/
                trackartist - tracktitle.mp3
                trackartist - tracktitle.mp3
```

# music_videos

## Plex Music Videos

You can add music videos for tracks you have in your library. To do so, ensure that the video files are named and organized appropriately.

**To have the music video associated with the track, it must start with the exact filename of the corresponding music track and must be in the same directory as that track.**

Music/Artist_Name - Album_Name/Track_Filename - Descriptive_Name-Video_Type.ext
Where -Video_Type is one of:

* -lyrics (lyrics music video)
* -video (regular music video)

Here are some examples of adding local artist and music videos.
```
/Music
   /Pink Floyd
      /The Wall
         101 - In the Flesh.mp3
         102 - The Thin Ice.mp3
         201 - Hey You.mp3
         202 - Is There Anybody Out There.mp3
      /Wish You Were Here
         01 - Shine On You Crazy Diamond (Parts I-V).m4a
         02 - Welcome to the Machine.mp3
         03 - Have a Cigar.mp3
   /Foo Fighters
      /One By One
      /There is Nothing Left to Lose
   /U2
      /Joshua Tree

/Music
   ./Bob Schneider - I'm Good Now/
      01-Come With Me Tonight.mp3
      02-Medicine.mp3
      02-Medicine - Medicine (extended jam)-lyrics.mp4
      03-A Long Way To Get.mp3
      Saxon Pub Dec 29, 2014-live.mp4
      Stephanie's Rock Show-interview.mp4

   ./Bob Schneider - Lonelyland/
      01-Metal and Steel.mp3
      01-Metal and Steel - Metal and Steel-video.mp4
      02-Big Blue Sea.mp3

**Note: Music videos can be placed in the same file as music, but must be named with the "-video" at the end**

**Example 1:**
    ./Radiohead/
        ./A Moon Shaped Pool/
            01 Burn The Witch.flac
            01 Burn The Witch - Burn The Witch-video.mkv

**Example 2:**
    ./Ice Cube/
        Ice Cube - Ghetto Vet -video.mp4
        Ice Cube - Friday -video.mp4
        Ice Cube - Race Card -video.mp4

```

# Global setting

## Global Music Videos Folder

Some users prefer to separate their musical videos from the actual audio files. This is supported through a global path setting for the location of the separate musical video content.

**Note: When using a `global` folder for your videos, if you
wish to have music videos associated with particular tracks in your library (so that they appear
on—and can be accessed with—the track), be sure to name the video file with the same track
name as the track.**

## Configure Local Media Assets Agent

To start, you need to specify the location of your “global” music videos folder. Note that
this is truly global and is not a per-library setting. The location is specified in your Local
Media Assets preferences.

Launch the Plex Web App

1. Choose Settings from the top right of the Home screen, then choose Server
2. Choose Agents
3. Choose Artists in the first row and then the Agent you want to change in the second row
4. Local Media Assets should already be enabled from earlier, so open the agent preferences via the gear icon on the right side
5. In the Local music video path field, specify the full filesystem path to the location of where your music videos are stored
6. _Save the path_


## Plex Music with Embedded Metadata

Some applications embed metadata in the music files, generally as an ID3 or M4A tag. If your music files have embedded data you'd like to use, you can:

1. Ensure `Local Media Assets` has been enabled for the Agent you’re using in your music Library
2. Make sure that `Local Media Assets` is at the top of the Agents list
3. When creating or editing the music library, ensure that the Use `embedded tags` advanced option is enabled

    `Music/ArtistName/AlbumName/TrackNumber - TrackName.ext`

**Example:**

```
/Music
   ./Pink Floyd/
      ./Wish You Were Here/
         01 - Shine On You Crazy Diamond (Parts I-V).m4a
         02 - Welcome to the Machine.mp3
         03 - Have a Cigar.mp3

   ./Foo Fighters/
      ./One By One/
      ./There is Nothing Left to Lose/
   ./U2/
      /Joshua Tree/

```

## Music Labelling when embedded metadata is not present in tracks

    `Music/ArtistName - AlbumName/TrackNumber - TrackName.ext`

**Example:**
```
/Music
    ./Pink Floyd - Wish You Were Here/
        01 - Shine On You Crazy Diamond (Parts I-V).m4a
        02 - Welcome to the Machine.mp3
        03 - Have a Cigar.mp3

   ./Foo Fighters - One By One/
   ./Foo Fighters - There is Nothing Left to Lose/
   ./U2 - Joshua Tree/
```

# Adding_lyrics

## Lyrics: Naming and Organization

### Adding Local Lyrics

**Supported Lyric Formats**

The following formats are supported for external/sidecar lyric files:

* LRC (.lrc) – timed lyric file using the LRC format
* TXT (.txt) – plain text file with lyrics

If you have your own lyric files, you can keep them alongside your actual music tracks. Lyrics are identified by using specific naming and must be placed in the same directory as the corresponding, identically-named music track.


### File Structure

Music/ArtistName - AlbumName/TrackNumber - TrackName.ext

**Where .ext is one of:**

.lrc (timed lyrics file)
.txt (basic, untimed lyrics)
```
**Example:**

/Music
   >/Bob Schneider - I'm Good Now

  >>01-Come With Me Tonight.mp3
      01-Come With Me Tonight.lrc
      02-Medicine.mp3
      02-Medicine.txt
      03-A Long Way To Get.mp3

   >/Bob Schneider - Lonelyland

  >>01-Metal and Steel.mp3
     01-Metal and Steel.txt
      02-Big Blue Sea.mp3

```
# music_videos

## Adding Videos to Music Files

### Local Videos

**Inline Videos**

You can keep your videos alongside your actual music files. Videos are identified by using
specific naming and must be placed in a directory that contains a music track from the same artist.

**Artist Videos**

Interviews with the artists, behind the scenes footage, and more can be added to the artist
in your library. In order to do so, you’ll need to ensure that the video files are named and
organized appropriately.

**Example:**
```
Music/Artist_Name - Album_Name/Descriptive_Name-Video_Type.ext
```

Where -Video_Type is one of:
* -behindthescenes (behind the scenes)
* -concert (concert performance)
* -interview (artist interview)
* -live (live music video)
* -lyrics (lyrics music video
* -video (regular music video)

### Artist Videos

Interviews with the artists, behind the scenes footage, and more can be added to the artist
in your library. In order to do so, you’ll need to ensure that the video files are named and
organized appropriately.

**GlobalFolder/Artist_Name - Descriptive_Name-Video_Type.ext or**
**GlobalFolder/Artist_Name/Artist_Name(optional) - Descriptive_Name-Video_type.ext**

Tip!: If you organize the videos into directories based on the artist as in the second option, the artist name is optional in the filename.

Where -Video_Type is one of:
* -behindthescenes (behind the scenes)
* -concert (concert performance)
* -interview (artist interview)
* -live (live music video)
* -lyrics (lyrics music video
* -video (regular music video)

:small_red_triangle: If you exclude the “type” from the filename, it will default to the -video type.

**Examples:**

Here are some examples of content in a Global Music Videos Folder. We’ll assume this content is in the /MusicVideos folder specified in the path example.
```
/MusicVideos
   >ABBA - Concert at Royal Albert Hall-concert.mp4
   ABBA - Dancing Queen.mp4
   ABBA - The Making of Dancing Queen-behindthescenes.mkv

>/ABBA
    >>ABBA - Take a Chance on Me-video.mp4
      Knowing Me Knowing You-live.mp4
      Super Trouper.mkv
```
