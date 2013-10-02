#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# pytimeo.py
#
# Copyright © 2013 Mathieu Gaborit (matael) <mathieu@matael.org>
#
#
# Distributed under WTFPL terms
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#

"""
Interface between Python and the SETRAM transportation service.
"""

import requests
import re
from bs4 import BeautifulSoup as BS

__version__='0.0.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['Timeo']


class Timeo:
    """ Interface entre Python et le service Timéo de la SETRAM """

    def __init__(self, URL="http://dev.actigraph.fr/actipages/setram/module/mobile/pivk/relais.html.php"):

        self.URL = URL

        self.session = requests.Session()

        # session init
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
            'Content-type': 'application/x-www-form-urlencoded'})
        self.session.get(URL)

        # regexs
        self.extr_name_code = re.compile("([^\(]+) \((\d+)\)")
        self.extr_code = re.compile("\((\d+)\)")


    def getall_arrets(self, lignesens, attr_to_extract="name"):
        """ Récupére les informations sur tous les arrêts d'une même ligne dans
        un sens de circulation donné (A ou R, voir API SETRAM... ahem.).

        lignesens -- ligne à parser et sens de circulation (ex: 8_R , T1_A, ...)
        attr_to_extract -- paramètre à extraire (par défaut : nom de l'arrêt)

        """

        POST_params_liste = {
           'a': 'recherche_ligne',
           'ligne_sens': lignesens
        }

        result = self.session.post(self.URL, POST_params_liste)
        options = BS(result.text).find_all('option')

        if attr_to_extract == "name":
            return dict([self.extr_name_code.search(_.text).group(1,2)[::-1] for _ in options])
        else:
            return {self.extr_code.search(_.text).group(1):_.get(attr_to_extract) for _ in options}


    def get_lignes(self):
        """ Récupère une hashtable entre les lignes (et leur direction) et le code de ligne correspondant """

        return {
            _.text:_.get('value') for _ in
            BS(self.session.get(self.URL).text).find_all('option')
            if _.text.find('>') > -1
        }

    def get_arret(self, lignesens, code):
        """ Récupère les prochains passages à un arret donné

        lignesens -- code de ligne (ligne+sens, voir get_ligne())
        code -- code timéo de l'arret
        """

        ligne,sens = lignesens.split('_')
        code = str(code)

        # get references
        refs_all = self.getall_arrets(lignesens, attr_to_extract='value')

        POST_params = {
            'a':'recherche_arrets',
            'refs': refs_all[code].split('_')[0],
            'code': code,
            'sens': sens,
            'ligne':ligne,
            'list_refs' : refs_all[code]+'_'+code
        }

        # first, get the ran param
        res = self.session.post(self.URL, data=POST_params)
        ran = re.search("ran=(\d+)", BS(res.text).find_all('script')[-1].text.splitlines()[-2]).group(1)

        POST_params2 = {
            'a' : 'refresh',
            'refs': POST_params['refs'],
            'ran' : ran
        }

        # then, get the page with real data
        res = self.session.post(self.URL, data=POST_params2)
        stops = [_.text for _ in BS(res.text).find_all('li')[1:]]

        stoptimes = []

        for i in stops:
            if i.find('imminent') > -1 or i.find('en cours') > -1: stoptimes.append("maintenant")
            elif i.find('Aucun') > -1 :
                pass # no dates available, let stoptimes as it is : empty.
            else:
                next = re.search("(\d+ minutes?)", i)
                if not next:
                    next = re.search("(\d+ H \d+)", i)

                stoptimes.append(next.group(1))

        return stoptimes

if __name__=='__main__':

    t = Timeo()

    print("Liste des lignes et des codes associés :")
    liste = t.get_lignes()
    for k,v in liste.items():
        print(k+' -> '+v)

    print("\n")
    print("Liste des arrêts et de leur code pour la ligne T1_R :")
    arrets = t.getall_arrets('T1_R')
    for k,v in arrets.items():
        print(k+' -> '+v)

    print("\n")
    print("Temps avant l'arrivé du prochain tram pour les arrêts de T1_R :")
    for k,v in arrets.items():
        print("Arrivé à l'arret "+v+" : "+t.get_arret('T1_R', k)[0])
