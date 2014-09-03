# -*- coding: utf-8 -*-

""" maak een lijstje van mijn sonos componenten

gesorteerd op naam of ip adres
----------------------------------------------------------------
2014-08-23, fout op vangen als bv speaker is uitgezet
----------------------------------------------------------------
"""
# pylint: disable=C0103, C0301
# pep8: disable=E501

from soco import SoCo


def getSonosCoordinator():
    """Geef terug ipadres van de box die coordinator is.
    """

    # haal info over alle speakers op die aanstaan
    speakers = getSonos()
    for speaker in speakers:
        if speaker['is_coordinator']:
            return speaker['ip_address']


def getSonos():
    """info over alle sonos componenten ophalen
    in: niets
    uit: list met dictionries, elke dictionary heeft info over een sonos component
    """

    # discover werkt niet, haal zelf 1e speaker op
    a = SoCo('192.168.1.13')  # 13, 2014-08, de bridge
    # print a.player_name

    # haal nu gehele zone op, alle speakers etc
    zones = a.all_zones

    # maak een dictionary, key: ip
    mijn = {}
    for speaker in zones:
        key = speaker.ip_address

        try:
            info = (speaker.get_speaker_info() or "x")
        except:
            # vangt fout op, als een speaker bv is uitgezet
            continue

        if info != 'x':
            key = info['zone_name']
        else:
            key = "Bridge"
        mijn[key] = speaker
        # mijn[key] = speaker.volume

    # sorteer de keys, nu op naam
    ips = mijn.keys()
    ips.sort()

    # geef nu alles weer, gesorteerd
    my_sonos = []       # vul list met alle speakers tbv web weergave
    my_speaker = {}     # per speaker dictionary vullen
    tel = 0
    for ip in ips:
        tel = tel + 1
        speaker = mijn[ip]
        # print tel, speaker.ip_address,
        my_speaker['volgnr'] = tel
        my_speaker['ip_address'] = speaker.ip_address

        speaker_info = speaker.get_speaker_info()
        if speaker.is_bridge:
            # print "bridge",
            my_speaker['zone_name'] = "BRIDGE"
            my_speaker['is_coordinator'] = False
            my_speaker['volume'] = ""
            my_speaker['loudness'] = ""
            my_speaker['treble'] = ""
            my_speaker['bass'] = ""
            my_speaker['mute'] = ""
            my_speaker['is_speaker'] = False    # is component speaker of niet
        else:
            # print speaker_info['zone_name'],
            my_speaker['zone_name'] = speaker_info['zone_name']
            if speaker.is_coordinator:
                my_speaker['is_coordinator'] = True
                # print " <--- de baas",
            else:
                # print " <- geen baas",
                my_speaker['is_coordinator'] = False
            my_speaker['volume'] = speaker.volume
            # print 'vol: ', speaker.volume,
            my_speaker['loudness'] = speaker.loudness
            # print 'loudness', speaker.loudness,
            my_speaker['treble'] = speaker.treble
            # print 'treble', speaker.treble,
            my_speaker['bass'] = speaker.bass
            # print 'bass', speaker.bass,
            my_speaker['mute'] = speaker.mute
            print 'uit', speaker.mute
            my_speaker['is_speaker'] = True         # is component speaker of niet

        my_speaker['status_light'] = speaker.status_light
        # print 'light: ', speaker.status_light
        my_sonos.append(my_speaker)
        my_speaker = {}

    return my_sonos
