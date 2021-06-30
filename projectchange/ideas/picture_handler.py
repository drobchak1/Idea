import os
from PIL import Image
from flask import current_app

def add_idea_pic(pic_upload, idea_id):

    filename = pic_upload.filename
    #I.jpg ==== ext_type==jpg
    ext_type = filename.split('.')[-1]
    storage_filename = str(idea_id)+'.'+ext_type

    filepath = os.path.join(current_app.root_path,'static\idea_pics',storage_filename)

    output_size = (700,700) 

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename