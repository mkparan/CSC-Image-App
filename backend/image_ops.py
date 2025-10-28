import cv2
import numpy as np

def apply_operation(image, operation, params):
    if operation == 'grayscale':
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    elif operation == 'blur':
        kernel_size = int(params.get('kernel_size', 5))
        if kernel_size % 2 == 0: kernel_size += 1  # Must be odd
        return cv2.blur(image, (kernel_size, kernel_size))
    
    elif operation == 'gaussian_blur':
        kernel_size = int(params.get('kernel_size', 5))
        if kernel_size % 2 == 0: kernel_size += 1  # Must be odd
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    elif operation == 'median_blur':
        kernel_size = int(params.get('kernel_size', 5))
        if kernel_size % 2 == 0: kernel_size += 1  # Must be odd
        return cv2.medianBlur(image, kernel_size)
    
    elif operation == 'sharpen':
        amount = float(params.get('amount', 1.0))
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * amount
        return cv2.filter2D(image, -1, kernel)
    
    elif operation == 'threshold':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_value = int(params.get('threshold_value', 127))
        _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        return thresh
    
    elif operation == 'edge_detection':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return edges
    
    elif operation == 'dilation':
        kernel_size = int(params.get('kernel_size', 3))
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)
    
    elif operation == 'erosion':
        kernel_size = int(params.get('kernel_size', 3))
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.erode(image, kernel, iterations=1)
    
    elif operation == 'opening':
        kernel_size = int(params.get('kernel_size', 3))
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    
    elif operation == 'closing':
        kernel_size = int(params.get('kernel_size', 3))
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    
    return image
