# The Archiver

The Archiver is a YouTube playlist title archiver. It was created to address issues of videos in playlists being privated, deleted, copyright-claimed, or otherwise removed. In this scenario, it would be near impossible to retrieve the original video or even know what the video was. There are already existing tools which solve this problem, namely playlist downloaders that can save YouTube playlists to your hard drive. 

However, in the case where knowing the title of the video alone is enough to retrieve the original video from the wider Internet, this tool can be an alternate, time and space-efficient solution. The Archiver saves the titles of videos in a YouTube playlist to a file in the corresponding folder of the same name. It also saves a diff file which will store the differences in the playlist since the last time the program was ran. This way, identifying videos that have disappeared will be trivial.


## How to Use

Clone the repository to your local workspace. cd into the archive directory, then run the program with the link to the YouTube playlist as the first input argument. Additionally, if a truth-y value, like "true", is presented as the second input argument, the program will save a separate diff file labeled with the current time and date instead of overwriting the default diff file. For example, 

```
python playlist_archiver.py https://www.youtube.com/playlist?list=PLSKe9tZtmkZ9L_8tBJu1mSBbVh5jO4jHD true
```
Running the following command will archive the playlist pointed to by that link, and a separate diff file will be saved for the current timestamp.

## Contributing
Pull requests are welcome. 