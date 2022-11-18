import cv2 as cv

backSub = cv.createBackgroundSubtractorMOG2()

# backSub = cv.createBackgroundSubtractorKNN()
capture = cv.VideoCapture(0)
if not capture.isOpened():
    print("Cannot open camera")
    exit()

count = 0
Animal = ['ape', 'bull', 'cat', 'dog', 'elephant']
def reshape(img):
    shape = img.shape
    width = 800
    height = int(width * shape[0] / shape[1])
    return cv.resize(img, (width, height))

while True:
    ret, frame = capture.read()
    if frame is None:
        break
    
    fgMask = backSub.apply(frame)
    
    fgMask = cv.flip(fgMask, 1, dst=None)
    frame = cv.flip(frame, 1, dst=None)
    cv.rectangle(frame, (10, 2), (100,50), (255,255,255), -1)
    cv.putText(frame, Animal[0], (35, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
    cv.rectangle(frame, (140, 2), (230,50), (255,255,255), -1)
    cv.putText(frame, Animal[1], (165, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
    cv.rectangle(frame, (270, 2), (360,50), (255,255,255), -1)
    cv.putText(frame, Animal[2], (299, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
    cv.rectangle(frame, (400, 2), (490,50), (255,255,255), -1)
    cv.putText(frame, Animal[3], (433, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
    cv.rectangle(frame, (530, 2), (620,50), (255,255,255), -1)
    cv.putText(frame, Animal[4], (540, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
    
    cv.imshow('Frame', frame)
    # cv.imshow('FG Mask', fgMask)
    count += 1
    if count == 15:
        sum = []
        for i in range(5):
            sum.append(fgMask[2:50, (10 + i*130):(100+ i*130)].sum())
            count = 0
        index = [i for i in range(5) if sum[i] > 5000]
        if len(index) >= 2 or len(index) == 0 or sum[index[0]] < 30000:
            # print('wow')
            continue
        else:
            # print(index[0])
            animalImg = cv.imread('./images/' + Animal[index[0]] + '.jpg')
            animalImg = reshape(animalImg)
            cv.imshow(Animal[index[0]], animalImg)
            cv.waitKey()
            cv.destroyWindow(Animal[index[0]])

        # print(sum)
        count = 0
    if cv.waitKey(1) == ord('q'):
        break