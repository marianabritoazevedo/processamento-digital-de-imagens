import cv2
import sys

def main():
    image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    cv2.imshow("image", image)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
