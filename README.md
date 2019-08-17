# im2txt_char
Im2txt adaptation using character-sized tokens for image captioning

The repository come with scripts helping to install all requirements, train the model and generate/evaluate captions from the trained model.

To evaluate captions the coco-caption library is used.
A modification on the metrics METEOR is made to allow custom parameters, and a new metric is added which finds all the words with correct stem but with missmatching prefix/suffix.
