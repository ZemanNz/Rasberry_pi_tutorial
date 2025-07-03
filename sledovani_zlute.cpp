#include <opencv2/opencv.hpp>

// Funkce pro detekci a vykreslení kontur
void drawContours(cv::Mat& frame, const cv::Mat& mask, const cv::Scalar& color, const std::string& label) {
    std::vector<std::vector<cv::Point>> contours;
    cv::findContours(mask, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
    for (const auto& contour : contours)
    {
        cv::Rect bbox = cv::boundingRect(contour);
        if (bbox.area() > 300)
        {
            cv::rectangle(frame, bbox, color, 3);
            cv::putText(frame, label, 
                cv::Point(bbox.x, bbox.y - 10), 
                cv::FONT_HERSHEY_SIMPLEX, 0.8, color, 2);
        }
    }
}

int main()
{
    cv::VideoCapture cap(0);
    if (!cap.isOpened())
        return -1;

    // HSV rozsahy pro červenou
    cv::Scalar lower_red1(0, 100, 60), upper_red1(10, 255, 255);
    cv::Scalar lower_red2(160, 100, 60), upper_red2(179, 255, 255);
    // HSV rozsahy pro zelenou
    cv::Scalar lower_green(35, 100, 30), upper_green(85, 255, 255);
    // HSV rozsahy pro modrou
    cv::Scalar lower_blue(100, 100, 30), upper_blue(130, 255, 255);

    while (true)
    {
        cv::Mat frame, hsv;
        cap >> frame;
        if (frame.empty())
            break;

        cv::cvtColor(frame, hsv, cv::COLOR_BGR2HSV);

        // ČERVENÁ
        cv::Mat mask_red1, mask_red2, mask_red;
        cv::inRange(hsv, lower_red1, upper_red1, mask_red1);
        cv::inRange(hsv, lower_red2, upper_red2, mask_red2);
        cv::bitwise_or(mask_red1, mask_red2, mask_red);

        // ZELENÁ
        cv::Mat mask_green;
        cv::inRange(hsv, lower_green, upper_green, mask_green);

        // MODRÁ
        cv::Mat mask_blue;
        cv::inRange(hsv, lower_blue, upper_blue, mask_blue);

        // Zavolej funkci pro každou barvu
        drawContours(frame, mask_red,  cv::Scalar(0, 0, 255),   "RED");
        drawContours(frame, mask_green,cv::Scalar(0, 255, 0),   "GREEN");
        drawContours(frame, mask_blue, cv::Scalar(255, 0, 0),   "BLUE");

        cv::imshow("frame", frame);
        //cv::imshow("hsv", hsv);
        if (cv::waitKey(1) == 'q')
            break;
    }
    cap.release();
    cv::destroyAllWindows();
    return 0;
}
// g++ sledovani_zlute.cpp -o color_detect `pkg-config --cflags --libs opencv4`
//./color_detect