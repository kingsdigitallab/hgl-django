from catalogue.models import *
import xmltodict


def process_dates(datestring):
    date = datestring.split("-")
    st = int(date[0])
    ed = int(date[1])
    dates = [st,ed]
    return dates

def importEad():
    #Open the file and convert into dict named data
    file = open("import/SLS_Calm_data.xml", "r")
    data = file.read()
    file.close()
    data =  xmltodict.parse(data)
    #Let's get rid of those top levels for now and define the archive var
    archive = data["ead"]["archdesc"]["dsc"]
    return archive

#pass the archive desc to this function:
def importItems(archive_item):
    counter = 0
    for item in archive_item["c"]:
        print(counter)
        createItem(item)
        counter += 1

def createItem(c, parent = None):
    #Create top level archive item ...
    ba = BasicArchiveModel()
    ba.unittitle = c["did"]["unittitle"]['#text']
    print(ba.unittitle)
    try:
        ba.unitstart_date = process_dates(c["did"]["unitdate"]["@normal"])[0]
        ba.unitend_date = process_dates(c["did"]["unitdate"]["@normal"])[1]
    except Exception: #No dates!!
        ba.unitstart_date = 1
        ba.unitend_date = 2
    try:
        level = Level.objects.get(desc=c["@level"])
    except Level.DoesNotExist:
        level = Level()
        level.desc = c["@level"]
        level.save()
    ba.level = level
    try:
        repo = Repository.objects.get(desc=c["did"]["repository"]["#text"])
        ba.repository = repo
    except Repository.DoesNotExist:
        repo = Repository()
        repo.desc = c["did"]["repository"]["#text"]
        repo.save()
    ba.repository = repo
    
    ba.save()

    try:
        addUnitId(c['did'], ba)
    except Exception as e:
        print('Unit id failed' + ' ' + str(ba.unittitle))
        print(e)

    if c["did"].get("langmaterial") != None:
        addLanguages( c["did"]["langmaterial"], ba)
    else:
        pass
        
    if c["did"].get("physdesc") != None:
        addPhysDesc(c["did"], ba)
    else:
        pass
        
    try:
        addNotes(c, ba)
    except Exception as e:
        print(e)
        

 
    try:
        ba.scopecontent = c["scopecontent"]['p']
    except Exception:
        pass
    try:
        ba.arrangement = c["arrangement"]['p']
    except Exception:
        pass
    try:
        ba.custodhist = c["custodhist"]['p']
    except Exception:
        pass
    try:
        ba.relatedmaterial = c["relatedmaterial"]['p']
    except Exception:
        pass
    try:
        ba.bioghist = c["bioghist"]["p"]
    except Exception:
        pass
    ba.save() #to make sure we have an ID
    if parent is not None:
        ba.parent = parent
    ba.save()
    try:
        for child in c['c']:
            createItem(child, parent = ba )
    except Exception as e:
        pass

def addNotes(c, ba):
    note_id = c['note']
    print('TYPE: {}'.format(type(note_id)))
    if isinstance(note_id, list):
        for note in note_id:
            #The note will always be unique
            NewNote = Note()
            try: #deal with types
                NewNoteType = NoteType.objects.get(desc=note['@type'])
                NewNote.type = NewNoteType
            except NoteType.DoesNotExist:
                NewNoteType = NoteType()
                NewNoteType.desc = note['@type']
                NewNoteType.save()
                NewNote.type = NewNoteType
            try: #deal with audiences
                NewNoteAudience = NoteAudience.objects.get(desc=note['@audience'])
                NewNote.audience = NewNoteAudience
            except NoteAudience.DoesNotExist :
                NewNoteAudience = NoteAudience()
                NewNoteAudience.desc = note['@audience']
                NewNoteAudience.save()
                NewNote.audience = NewNoteAudience
            NewNote.text = note['p']
            NewNote.item = ba
            NewNote.save()
    else:
        NewNote = Note()
        try:
            NewNoteType = NoteType.objects.get(desc=note_id['@type'])
            NewNote.type = NewNoteType
        except NoteType.DoesNotExist:
            NewNoteType = NoteType()
            NewNoteType.desc = note_id['@type']
            NewNote.type = NewNoteType
            NewNote.item = ba()    
        try: #deal with audiences
            NewNoteAudience = NoteAudience.objects.get(desc=note['@audience'])
            NewNote.audience = NewNoteAudience
        except NoteAudience.DoesNotExist :
            NewNoteAudience = NoteAudience()
            NewNoteAudience.desc = note['@audience']
            NewNoteAudience.save()
            NewNote.audience = NewNoteAudience
        NewNote.text = note['p']
        NewNote.save()
    ba.save()


def addUnitId(did, ba):
    unit_id = did['unitid']
    print('TYPE: {}'.format(type(unit_id)))
    if isinstance(unit_id, list): #Need to iterate
        for i in unit_id:
            try:
                NewID = UnitId()
                NewID.type = UnitIdType.objects.get(desc=i['@label'])
                NewID.desc = i['#text']
                NewID.item = ba
                NewID.save()
                ba.save()
            except UnitIdType.DoesNotExist:
                NewID = UnitId()
                NewIDT = UnitIdType()
                NewIDT.desc = i['@label']
                NewIDT.save()
                NewID.type = NewIDT
                NewID.desc = i['#text']
                NewID.item = ba
                NewID.save()
                ba.save()
    else: #Just gonna be Dict
        try:
            NewID = UnitId()
            NewID.type = UnitIdType.objects.get(unit_id['@label'])
            NewID.desc = unit_id['#text']
            NewID.item = ba
            NewID.save()
            ba.save()
        except UnitIdType.DoesNotExist:
            NewID = UnitId()
            NewIDT = UnitIdType()
            NewIDT.desc = unit_id['@label']
            NewIDT.save()
            NewID.type = NewIDT
            NewID.desc = unit_id['#text']
            NewID.item = ba
            NewID.save()
            ba.save()

def addLanguages(langmat, ba):
    langs = langmat['language'] # 
    print('TYPE: {}'.format(type(langs)))
    if isinstance(langs, list): #Need to iterate
        for lang in langs:
            try:
                la = Language.objects.get(desc=lang['#text'])
                ba.language.add(la)
            except Language.DoesNotExist:
                la = Language()
                la.desc = lang['#text']
                la.save()
                ba.language.add(la)
    else:
        try:
            la = Language.objects.get(desc=langs['#text'])
            ba.language.add(la)
        except Language.DoesNotExist:
            la = Language()
            la.desc = langs['#text']
            la.save()
            ba.language.add(la)
    ba.save()       
            
     
def addPhysDesc(did, ba):
    phys_desc = did['physdesc']
    print('TYPE: {}'.format(type(phys_desc)))
    if isinstance(phys_desc, list):
        for pd in phys_desc:
            NewPD = PhysDesc()
            try:
                NewPD.type = PhysDescType.objects.get(desc=pd['@label'])
                if pd['@label'] == 'Extent':
                    NewPD.desc = pd['extent']
                else:
                    NewPD.desc = pd['genreform']
                NewPD.item = ba
                NewPD.save()
                ba.save()
            except PhysDescType.DoesNotExist:
                NewPDT = PhysDescType()
                NewPDT.desc = pd['@label']
                NewPDT.save()
                if pd['@label'] == 'Extent':
                    NewPD.desc = pd['extent']
                else:
                    NewPD.desc = pd['genreform']
                NewPD.type = NewPDT
                NewPD.item = ba
                NewPD.save()
                ba.save()               
    else:
        NewPD = PhysDesc()
        try:
            NewPD.type = PhysDescType.objects.get(desc=phys_desc['@label'])
            if phys_desc['@label'] == 'Extent':
                NewPD.desc = phys_desc['extent']
            else:
                NewPD.desc = phys_desc['genreform']
            NewPD.item = ba
            NewPD.save()
            ba.save()
        except PhysDescType.DoesNotExist:
            NewPDT = PhysDescType()
            NewPDT.desc = phys_desc['@label']
            NewPDT.save()
            if phys_desc['@label'] == 'Extent':
                NewPD.desc = phys_desc['extent']
            else:
                NewPD.desc = phys_desc['genreform']
            NewPD.type = NewPDT
            NewPD.item = ba
            NewPD.save()
            ba.save()


