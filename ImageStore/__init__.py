from DataFactory import dbImageStore
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
import logging

class AddUpdateImageStore(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        if self.request.get('imagestore_key'):
            image = dbImageStore.ImageStore.get(self.request.get('imagestore_key'))
        else:
            image = dbImageStore.ImageStore()
            
        image.name = self.request.get('image_name')
        image.description = self.request.get('image_description')
        
        upload_files =  self.get_uploads('image_file')
        logging.info(upload_files)
        if upload_files:
            image.imageUrl = images.get_serving_url(str(upload_files[0].key()))
        
        db.put(image)
    
        self.redirect('/edit/imageStore/?status=1&message=Image added/updated')