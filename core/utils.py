from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

# Some  useful function


def rename_file(picture_name, user_id):
    ''' Rename picture in order to store them wit FileStorageSystem.
    With the connected user id and the type of picture '''
    new_name = '{}.{}'.format(user_id, picture_name.split('.')[1])
    return new_name


def resize_picture(img):
    with Image.open(img) as pict:
        SIZE = (140, 140)
        # resize picture
        cover = resizeimage.resize_cover(pict, SIZE)

        # after that save into an output
        output = BytesIO()
        cover.save(output, format='JPEG', quality=100)
        output.seek(0)
            # cover.save('core/media/user_avatar/thumbnail.png', pict.format)
    return cover

def create_avatar_pict(img):
    ''' returns a resized and a renamed picture '''

    img = Image.open(img)
    # convert all picture to jpg
    img = img.convert('RGB')
    # resize picture
    img = img.resize((140 , 140) , Image.ANTIALIAS)
    # make readable picture
    output = BytesIO()
    img.save(output, 'jpeg')
    output.seek(0)
    # return the new uploaded file
    return SimpleUploadedFile('temp', output.read())

def get_age(birth_year):
    import datetime
    this_year = datetime.date.today().year
    return this_year - birth_year