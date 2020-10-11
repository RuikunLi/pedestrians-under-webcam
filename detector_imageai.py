import pandas as pd
import os
from imageai.Detection import ObjectDetection
import inspect
import time

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

thisdir = os.getcwd()

print('the current path is {}'.format(thisdir), lineno())
print('--- working on collector excel sheet---', lineno())
collector_xls = pd.ExcelFile('collector.xlsx')
collector_sheet_to_df_map = {}
for sheet_name in collector_xls.sheet_names:
    print(sheet_name, lineno())
    collector_sheet_to_df_map[sheet_name] = collector_xls.parse(sheet_name)

print('--- working on testset_baseline_annotation excel sheet---', lineno())
testset_baseline_xls = pd.ExcelFile('testset_baseline_annotation.xlsx')

testset_sheet_to_df_map = {}
for sheet_name in testset_baseline_xls.sheet_names:
    print(sheet_name, lineno())
    testset_sheet_to_df_map[sheet_name] = testset_baseline_xls.parse(sheet_name)
print('--- generating dfs ---', lineno())
df_dublin0 = pd.merge(testset_sheet_to_df_map['dublin0_baseline_annotation'], collector_sheet_to_df_map['dublin'], how='left', on='image_name')
df_NYC1 = pd.merge(testset_sheet_to_df_map['NYC1_baseline_annotation'], collector_sheet_to_df_map['nyc_1'], how='left', on='image_name')
df_venice0 = pd.merge(testset_sheet_to_df_map['venice0_baseline_annotation'], collector_sheet_to_df_map['venice'], how='left', on='image_name')
df_london3 = pd.merge(testset_sheet_to_df_map['london3_baseline_annotation'], collector_sheet_to_df_map['london_3'], how='left', on='image_name')
df_miami0 = pd.merge(testset_sheet_to_df_map['miami0_baseline_annotation'], collector_sheet_to_df_map['miami'], how='left', on='image_name')

def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

print('--- generating images lists ---', lineno())
for webcam in fast_scandir(thisdir):
    for r, d, f in os.walk(webcam):
        webcam_name = webcam.split('/')[-1]
        print('images:', webcam_name, lineno())
        vars()[str(webcam_name) + '_images'] = []
        imgs = eval(str(webcam_name) + '_images')
        for file in f:
            if 'png' in file:
                imgs.append(os.path.join(r, file))

def detection(webcam_name, algo, prob=30, classes='all'):
    algos = {
        "resnet": "models/resnet50_coco_best_v2.0.1.h5",
        "yolov3": "models/yolo.h5",
        "yolo_tiny": "models/yolo-tiny.h5"
    }
    if not os.path.isdir('{}_{}_{}_{}'.format(webcam_name, algo, classes, prob)):
        os.makedirs('{}_{}_{}_{}'.format(webcam_name, algo, classes, prob))
    print(webcam_name, algo, lineno())
    images = eval(str(webcam_name) + '_images')
    thisdir = os.getcwd()
    detector = ObjectDetection()
    if algo == "resnet":
        detector.setModelTypeAsRetinaNet()
    elif algo == "yolov3":
        detector.setModelTypeAsYOLOv3()
    elif algo == "yolo_tiny":
        detector.setModelTypeAsTinyYOLOv3()
    else:
        print("Given algorithm of object detection is invalid.", lineno())
        
    detector.setModelPath( os.path.join(thisdir , algos[algo]))
    detector.loadModel()
    all_boxes ={}
    exec_times = {}
    for img in images:
        start_time = time.time()
        target_image_name = img.split('/')[-1]
        print(target_image_name, lineno())
        if classes == 'all':
            detections = detector.detectObjectsFromImage(input_image=img, output_image_path=os.path.join(thisdir , "{}_{}_{}_{}/{}_{}_{}".format(webcam_name, algo, classes, prob, algo, target_image_name_prob)), minimum_percentage_probability=prob)
        elif classes == 'person':
            custom_objects=detector.CustomObjects(person=True)
            detections = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_image=img, output_image_path=os.path.join(thisdir , "{}_{}_{}_{}/{}_{}_{}".format(webcam_name, algo, classes, prob, algo, target_image_name_prob)), minimum_percentage_probability=prob)

        boxes = []
        for eachObject in detections:
    #         print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
    #         print("--------------------------------")
            box = eachObject["name"], eachObject["percentage_probability"], eachObject["box_points"]
            boxes.append(box)
        all_boxes[target_image_name] = boxes
        exec_time = time.time() - start_time
        exec_times[target_image_name] = round(exec_time,2)
    df = eval('df_'+ str(webcam_name))
    df['boxes_{}_{}_{}'.format(algo,classes_prob)] = df['image_name'].map(all_boxes)
    df['{}_{}_{}_exec_time'.format(algo,classes_prob)] = df['image_name'].map(exec_times)
    
print('--- detecting ---', lineno())

if not os.path.isdir('detections_csv'):
        os.makedirs('detections_csv')
for webcam in ['dublin0', 'london3','miami0','NYC1','venice0']:
#for webcam in ['dublin0']:
    for classes in ['all', 'person']:
        for prob in [15, 30, 50, 70]:
            for algo in ['resnet', 'yolov3', 'yolo_tiny']:
	
                print('-----------------')
                detection(webcam, algo, prob, classes)
            df = eval('df_'+ str(webcam))
            df.to_csv('detections_csv/{}_{}_{}detection.csv'.format(webcam, classes, prob))


