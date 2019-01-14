from catalogue.models import *
import xmltodict
import re


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
    for item in archive_item["c"]:
        createItem(item)

def createItem(item):
    #Create top level archive item ...
    try:
        ba = BasicArchiveModel.objects.get(unittitle=\
        item["did"]["unittitle"])
    except BasicArchiveModel.DoesNotExist:
        ba = BasicArchiveModel()
    ba.unititle = item["did"]["unittitle"]
    ba.unitdate_start = process_dates(item["did"]["unitdate"]["@normal"])[0]
    ba.unitdate_end = process_dates(item["did"]["unitdate"]["@normal"])[1]
    print (ba.unitdate_start)

    try:
        level = Level.objects.get(desc=item["@level"])
        ba.level = level
        print('here it is')
    except Level.DoesNotExist:
        level = Level()
        level.desc = item["@level"]
        level.save()
        print("level: " + level.desc)
    ba.level = level
    print('Double checking here:' + ba.level.desc)
    try:
        repo = Repository.objects.get(desc=item["did"]["repository"]["#text"])
        ba.repository = repo
    except Repository.DoesNotExist:
        repo = Repository()
        repo.desc = item["did"]["repository"]["#text"]
        repo.save()
        print("repo: " + repo.desc)
    ba.repository = repo
    ba.scopecontent = item["scopecontent"]['p']
    ba.arrangement = item["arrangement"]['p']
    ba.custodhist = item["custodhist"]['p']
    ba.relatedmaterial = item["relatedmaterial"]['p']
    try:
        la = Language.objects.get(desc=item["did"]["langmaterial"]["language"]["#text"])
        ba.language = la
    except Language.DoesNotExist:
        la = Language()
        la.desc = item["did"]["langmaterial"]["language"]["#text"]
        la.save()
        print ('lang: ' + la.desc)
    ba.language = la
    ba.save()


        #That's all the main fields, now on to relations
        #descriptions
        #try:
        #    PhysDescType.objects.get(desc=data["archdesc"]["did"])

