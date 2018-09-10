import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="PennApps 2018-c1bab6b19fa1.json"

from google.cloud import vision_v1p3beta1 as vision

def localize_objects(path):
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
        image = vision.types.Image(content=content)
        objects = client.object_localization(
            image=image).localized_object_annotations

        print('Number of objects found: {}'.format(len(objects)))
        for object_ in objects:
            print('\n{} (confidence: {})'.format(object_.name, object_.score))
            print('Normalized bounding polygon vertices: ')
            for vertex in object_.bounding_poly.normalized_vertices:
                print(' - ({}, {})'.format(vertex.x, vertex.y))

localize_objects('download.jpeg')