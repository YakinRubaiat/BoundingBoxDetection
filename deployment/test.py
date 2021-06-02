# Model path https://drive.google.com/drive/folders/1XSD11wDsW7MAOFXBq7FAR3oUZ957_vDy?usp=sharing

model1_path = './models/resnet50_csv_22.h5'
model1 = models.load_model(model1_path, backbone_name='resnet50', convert=True, nms=False)

model2_path = './models/resnet101_csv_21.h5'
model2 = models.load_model(model2_path, backbone_name='resnet101', convert=True, nms=False)
