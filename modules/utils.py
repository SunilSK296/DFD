import cv2

def draw_boxes(image_path, contours):
    image = cv2.imread(image_path)

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)

    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
