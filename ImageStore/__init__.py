from DataFactory import dbImageStore
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
import Settings
import logging

class AddUpdateImageStore(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        if self.request.get('imagestore_key'):
            image = dbImageStore.ImageStore.get(self.request.get('imagestore_key'))
        else:
            image = dbImageStore.ImageStore()
            
        image.name = self.request.get('image_name')
        
        upload_files =  self.get_uploads('image_file')
        
        if upload_files:
            image.imageUrl = images.get_serving_url(str(upload_files[0].key()))
        
        imageKey = db.put(image)
    
        for language in Settings.languages:
            description = self.request.get('image_description_' + language)
            if description:
                logging.info(description)
                imageDescription = dbImageStore.ImageDescription.gql('WHERE imageEntry = :imageEntry AND lang = :lang', imageEntry = imageKey, lang = language).get()
                if imageDescription is None:
                    imageDescription = dbImageStore.ImageDescription()
                    imageDescription.imageEntry = imageKey
                    imageDescription.lang = language
                
                imageDescription.description = description
                db.put(imageDescription)
    
        self.redirect('/edit/imageStore/?status=1&message=Image added/updated')