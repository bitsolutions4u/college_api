import os.path
import tablib

from System.resources import MenuResource,SubmenuResource,MenuitemResource
from Users.resources import  DjangoAppResource, ContentTypeDetailResource, PermissionDetailResource



#Export data

def export_menu_data():
    mypath="System/Data/"
    
    if not os.path.exists(mypath):
        os.mkdir(mypath)

    try:
        menu = MenuResource()
        dataset = menu.export()
        with open(mypath+'menu.json', 'w') as f:
            f.write(dataset.json)
        print("Success to Export Menu Data")
    except:
        print(" Failed to Export Menu Data ")



    try:
        submenu = SubmenuResource()
        dataset = submenu.export()
        with open(mypath+'submenu.json', 'w') as f:
            f.write(dataset.json)
        print("Success to Export Submenu Data")
    except:
        print(" Failed to Export Submenu Data ")
    


    try:
        menuitem = MenuitemResource()
        dataset = menuitem.export()
        with open(mypath+'menuitem.json', 'w') as f:
            f.write(dataset.json)
        print("Success to Export MenuItem Data")
    except:
        print(" Failed to Export MenuItem Data ")
    


    try:
        djangoapp = DjangoAppResource()
        dataset = djangoapp.export()
        with open(mypath+'djangoapp.json', 'w') as f:
            f.write(dataset.json)
        print("Success to Export DjangoApp Data")
    except:
        print(" Failed to Export DjangoApp Data ")



    try:
        contenttypedetail = ContentTypeDetailResource()
        dataset = contenttypedetail.export()
        with open(mypath+'contenttypedetail.json', 'w') as f:
            f.write(dataset.json)
        print("Success to Export ContentTypeDetail Data")
    except:
        print(" Failed to Export ContentTypeDetail Data ")
    


    try:
        permissiondetail = PermissionDetailResource()
        dataset = permissiondetail.export()
        with open(mypath+'permissiondetail.json', 'w') as f:
            f.write(dataset.json)
        print("Success to Export PermissionDetail Data")
    except:
        print(" Failed to Export PermissionDetail Data ")
    








#import data

def import_menu_data():

    mypath="System/Data/"


    menu = MenuResource()
    dataset = tablib.Dataset()
    dataset.json = open(mypath+'menu.json', "r").read()
    result = menu.import_data(dataset, dry_run=True)
    print("Processing a Import Menu Data")

    if not result.has_errors():
        result = menu.import_data(dataset, dry_run=False)
        print(' Success to Export Menu data ')

    else:
        print('Failed to Import Menu data has errors ')
        print(result.has_errors())
        print(result.has_validation_errors())
        print( result.row_errors())
        print(result.base_errors)
        print(result.invalid_rows)




    submenu = SubmenuResource()
    dataset = tablib.Dataset()
    dataset.json = open(mypath+'submenu.json', "r").read()
    result = submenu.import_data(dataset, dry_run=True)
    print("Processing a Import Submenu Data")

    if not result.has_errors():
        result = submenu.import_data(dataset, dry_run=False)
        print(' Success to Export Submenu data ')

    else:
        print('Failed to Import Submenu data has errors ')
        print(result.has_errors())
        print(result.has_validation_errors())
        print( result.row_errors())
        print(result.base_errors)
        print(result.invalid_rows)



    menuitem = MenuitemResource()
    dataset = tablib.Dataset()
    dataset.json = open(mypath+'menuitem.json', "r").read()
    result = menuitem.import_data(dataset, dry_run=True)
    print("Processing a Import Menuitem Data")

    if not result.has_errors():
        result = menuitem.import_data(dataset, dry_run=False)
        print(' Success to Export MenuItem data ')

    else:
        print('Failed to Import Menuitem data has errors ')
        print(result.has_errors())
        print(result.has_validation_errors())
        print( result.row_errors())
        print(result.base_errors)
        print(result.invalid_rows)



    djangoapp = DjangoAppResource()
    dataset = tablib.Dataset()
    dataset.json = open(mypath+'djangoapp.json', "r").read()
    result = djangoapp.import_data(dataset, dry_run=True)
    print("Processing a Import DjangoApp Data")

    if not result.has_errors():
        result = djangoapp.import_data(dataset, dry_run=False)
        print(' Success to Export DjangoApp data ')

    else:
        print('Failed to Import DjangoApp data has errors ')
        print(result.has_errors())
        print(result.has_validation_errors())
        print( result.row_errors())
        print(result.base_errors)
        print(result.invalid_rows)



    contenttypedetail = ContentTypeDetailResource()
    dataset = tablib.Dataset()
    dataset.json = open(mypath+'contenttypedetail.json', "r").read()
    result = contenttypedetail.import_data(dataset, dry_run=True)
    print("Processing a Import ContentTypeDetail Data")

    if not result.has_errors():
        result = contenttypedetail.import_data(dataset, dry_run=False)
        print(' Success to Export ContentTypeDetail data ')

    else:
        print('Failed to Import ContentTypeDetail data has errors ')
        print(result.has_errors())
        print(result.has_validation_errors())
        print( result.row_errors())
        print(result.base_errors)
        print(result.invalid_rows)




    permissiondetail = PermissionDetailResource()
    dataset = tablib.Dataset()
    dataset.json = open(mypath+'permissiondetail.json', "r").read()
    result = permissiondetail.import_data(dataset, dry_run=True)
    print("Processing a Import PermissionDetail Data")

    if not result.has_errors():
        result = permissiondetail.import_data(dataset, dry_run=False)
        print(' Success to Export Permissiondetail data ')

    else:
        print('Failed to Import PermissionDetail data has errors ')
        print(result.has_errors())
        print(result.has_validation_errors())
        print( result.row_errors())
        print(result.base_errors)
        print(result.invalid_rows)




