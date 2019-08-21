import cognitive_face as CF

CF.person_group.create('test', name='test')
siem = CF.person.create('test', name='siem')
CF.person.add_face(r'pictures_siem\IMG-20190317-WA0003.jpeg', person_group_id='test', person_id=siem['personId'])
CF.person.add_face(r'pictures_siem\IMG-20190402-WA0004.jpeg', 'test', siem['personId'])
CF.person.add_face(r'pictures_siem\IMG-20190405-WA0001.jpeg', 'test', siem['personId'])
CF.person.add_face(r'pictures_siem\IMG-20190406-WA0006.jpeg', 'test', siem['personId'])

