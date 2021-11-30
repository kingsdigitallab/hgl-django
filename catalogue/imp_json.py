from catalogue.models import *
import json


def process_dates(datestring):
    date = datestring.split("-")
    st = int(date[0])
    ed = int(date[1])
    dates = [st, ed]
    return dates


def importEad():
    # Open the file and convert into dict named data
    file = open("import/convertedjson.json", "r")
    data = file.read()
    file.close()
    data = json.loads(data)
    archive = data["dsc"]
    return archive


# pass the archive desc to this function:
def importItems(archive):
    for item in archive["c"]:
        createItem(item)


def createItem(c, parent=None):
    # Create top level archive item ...
    ba = BasicArchiveModel()
    try:
        ba.unittitle = c["did"]["unittitle"]["text"]
    except Exception:
        print("No unitittle")
    try:
        ba.unitstart_date = process_dates(c["did"]["unitdate"]["normal"])[0]
        ba.unitend_date = process_dates(c["did"]["unitdate"]["normal"])[1]
    except Exception:  # No dates!!
        ba.unitstart_date = 0
        ba.unitend_date = 0
    try:
        level = Level.objects.get(desc=c["level"])
    except Level.DoesNotExist:
        level = Level()
        level.desc = c["level"]
        level.save()
    ba.level = level
    repo = Repository.objects.all()[0]
    ba.repository = repo
    ba.save()

    try:
        addUnitId(c["did"]["unitid"], ba)
    except Exception as e:
        print(("Unit id failed" + " " + str(ba.unittitle)))
        print(e)

    if c["did"].get("langmaterial") != None:
        addLanguages(c["did"]["langmaterial"], ba)
    else:
        pass

    if c["did"].get("physdesc") != None:
        addPhysDesc(c["did"]["physdesc"], ba)
    else:
        pass

    try:
        addNotes(c["note"], ba)
    except Exception as e:
        print(e)

    try:
        ba.scopecontent = c["scopecontent"]["p"]
    except Exception:
        pass
    try:
        ba.arrangement = c["arrangement"]["p"]
    except Exception:
        pass
    try:
        ba.custodhist = c["custodhist"]["p"]
    except Exception:
        pass
    try:
        ba.relatedmaterial = c["relatedmaterial"]["p"]
    except Exception:
        pass
    try:
        ba.bioghist = c["bioghist"]["p"]
    except Exception:
        pass
    ba.save()  # to make sure we have an ID!
    if parent is not None:
        ba.parent = parent
    ba.save()
    if "c" in c:
        print(("Parent:", ba.unittitle))
        for child in c["c"]:
            print(("Child: ", child))
            # print("Child_did: " , child["did"])
            createItem(child, parent=ba)


def addNotes(notes, ba):
    for note in notes:
        # The note will always be unique
        NewNote = Note()
        try:  # deal with types
            NewNoteType = NoteType.objects.get(desc=note["type"])
            NewNote.type = NewNoteType
        except NoteType.DoesNotExist:
            NewNoteType = NoteType()
            NewNoteType.desc = note["type"]
            NewNoteType.save()
            NewNote.type = NewNoteType
        try:  # deal with audiences
            NewNoteAudience = NoteAudience.objects.get(desc=note["audience"])
            NewNote.audience = NewNoteAudience
        except NoteAudience.DoesNotExist:
            NewNoteAudience = NoteAudience()
            NewNoteAudience.desc = note["audience"]
            NewNoteAudience.save()
            NewNote.audience = NewNoteAudience
        NewNote.text = note["p"][0]  # Always first element?
        NewNote.item = ba
        NewNote.save()
    ba.save()


def addUnitId(unit_id, ba):
    for i in unit_id:
        try:
            NewID = UnitId()
            NewID.type = UnitIdType.objects.get(desc=i["label"])
            NewID.desc = i["text"]
            NewID.item = ba
            NewID.save()
            ba.save()
        except UnitIdType.DoesNotExist:
            NewID = UnitId()
            NewIDT = UnitIdType()
            NewIDT.desc = i["label"]
            NewIDT.save()
            NewID.type = NewIDT
            NewID.desc = i["text"]
            NewID.item = ba
            NewID.save()
            ba.save()


def addLanguages(langmaterial, ba):
    for lang in langmaterial:
        # print lang
        try:
            la = Language.objects.get(desc=lang["language"][0]["text"])
            ba.language.add(la)
        except Language.DoesNotExist:
            la = Language()
            la.desc = lang["language"]["text"]
            la.save()
            ba.language.add(la)
    ba.save()


def addPhysDesc(phys_desc, ba):
    for pd in phys_desc:
        NewPD = PhysDesc()
        try:
            NewPD.type = PhysDescType.objects.get(desc=pd["label"])
            if pd["label"] == "Extent":
                NewPD.desc = pd["extent"]
            else:
                NewPD.desc = pd["genreform"]
            NewPD.item = ba
            NewPD.save()
            ba.save()
        except PhysDescType.DoesNotExist:
            NewPDT = PhysDescType()
            NewPDT.desc = pd["label"]
            NewPDT.save()
            if pd["label"] == "Extent":
                NewPD.desc = pd["extent"]
            else:
                NewPD.desc = pd["genreform"]
            NewPD.type = NewPDT
            NewPD.item = ba
            NewPD.save()
            ba.save()
