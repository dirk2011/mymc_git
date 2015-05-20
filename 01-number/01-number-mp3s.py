
#!/usr/bin/python
# algemeen
import os
import fnmatch

# tbv mp3s
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, UFID
from mutagen.easyid3 import EasyID3

import ConfigParser     # tbv ini files

dirCol = "/media/multimedia/multimedia/muzik3/New/2014-08"
dirCol = "/media/rasp163-v/mymc/01-number/mp3s"
dirCol = "/media/rasp164-v/mymc/01-number/mp3s"

class MCNumber:
    """MCNumber, class voor afhandelen nummering
    """
    
    def __init__(self):
        # initialiseren
        self.fileMC = "mc.ini"
        self.config = ConfigParser.ConfigParser()
        self.next = -1          # unieke id voor nummeren mp3s

    def readNext(self):
        """readNext, lees volgend nummer uit mc.ini bestand
        """
        # laad bestand
        self.config.read(self.fileMC)

        # lees een waarde 
        self.next = self.config.get('mc', 'next')
    
    def saveNext(self):
        """saveNext, sla volgend nummer op in mc.ini bestand
        """
        # verhoog het nummer
        if self.next.isdigit():
            self.next = str(int(self.next) + 1)
            # print "nieuwe waarde: ", next
            self.config.set('mc', 'next', self.next)

        # bestand weer opslaan
        with open('mc.ini', 'wb') as self.configfile:
            self.config.write(self.configfile)


class Mp3:
    def __init__(self, fileMp3):
        """creatie Mp3 object
        """
        # mp3 bestand
        self.fileMp3 = fileMp3
        self.audio = ID3(self.fileMp3)

        self.length = -1
        self.bitrate = -1
        self.size = -1

        self.title = "#"
        self.album_artist = "#"
        self.artist = "#"
        self.album = "#"
        self.genre = "#"
        self.year = -1
        self.tracknumber = -1

        self.audio_get = "#"
        self.audio_data = "#"

    def readMp3Number(self):
        
        self.owner = "#"
        self.data  = "-1"

        if 'UFID:mc' not in self.audio.keys() :
            print 'onwaar tak -------------------'
            # als dit waar is bestaat UFID nog niet bij deze song
            self.audio_get = "#"
            self.audio_data = "#"

            number = MCNumber()
            number.readNext()
            print number.next
            self.audio.add(UFID(owner = 'mc', data = str(number.next)))
            print self.audio.get('UFID')
            
            self.audio.save()
            number.saveNext()
        else:
            # UFID bestaat !
            
            self.ufid_owner = self.audio.get('UFID:mc').owner
            self.ufid_data  = self.audio.get('UFID:mc').data
            print self.ufid_data
        
        

if __name__ == "__main__":
    print "* * * for real * * * "

    tel = 0
    for root, dir, files in os.walk(dirCol):
        # print dir
        for bestand in files:
            if fnmatch.fnmatch(bestand, "*.mp3"):
                tel = tel + 1
                print str(tel) + ": " + bestand
                song = Mp3(os.path.join(root, bestand))
                song.readMp3Number()
                # print song

# eof #
