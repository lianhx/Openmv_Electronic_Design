#include<iostream>
using namespace std;
#include<opencv2/opencv.hpp>
using namespace cv;

void find_rect16(Mat &src, int limit_value)
{
	Mat example(Size(src.cols, src.rows), CV_8UC3);
	for (int i = 0; i < src.rows - 2; i+=4)
	{
		for (int j = 0; j < src.cols - 2; j+=4)
		{
			if (((src.at<Vec3b>(i, j)[0] + src.at<Vec3b>(i + 1, j)[0] + src.at<Vec3b>(i + 2, j)[0] + src.at<Vec3b>(i + 3, j)[0] +
				src.at<Vec3b>(i, j + 1)[0] + src.at<Vec3b>(i + 1, j + 1)[0] + src.at<Vec3b>(i + 2, j + 1)[0] + src.at<Vec3b>(i + 3, j + 1)[0] +
				src.at<Vec3b>(i, j + 1)[0] + src.at<Vec3b>(i + 1, j + 1)[0] + src.at<Vec3b>(i + 2, j + 1)[0] + src.at<Vec3b>(i + 3, j + 1)[0] +
				src.at<Vec3b>(i, j + 1)[0] + src.at<Vec3b>(i + 1, j + 1)[0] + src.at<Vec3b>(i + 2, j + 1)[0] + src.at<Vec3b>(i + 3, j + 1)[0]) / 16) < limit_value)
			circle(example, Point(j, i), 1, Scalar(0, 255, 0), 2);
		}
	}
	imshow("example", example);
}
void find_rect9(Mat &src, int limit_value)
{
	Mat example(Size(src.cols, src.rows), CV_8UC3);
	for (int i = 0; i < src.rows - 2; i += 4)
	{
		for (int j = 0; j < src.cols - 2; j += 4)
		{
			if (((src.at<Vec3b>(i, j)[0] + src.at<Vec3b>(i + 1, j)[0] + src.at<Vec3b>(i + 2, j)[0] +
				src.at<Vec3b>(i, j + 1)[0] + src.at<Vec3b>(i + 1, j + 1)[0] + src.at<Vec3b>(i + 2, j + 1)[0] +
				src.at<Vec3b>(i, j + 1)[0] + src.at<Vec3b>(i + 1, j + 1)[0] + src.at<Vec3b>(i + 2, j + 1)[0] + 
				src.at<Vec3b>(i, j + 1)[0] + src.at<Vec3b>(i + 1, j + 1)[0] + src.at<Vec3b>(i + 2, j + 1)[0] ) / 9) > limit_value)
				circle(example, Point(j, i), 1, Scalar(0, 255, 0), 2);
		}
	}
	imshow("example", example);
}





int main()
{

	Mat src = imread("demo.jpg");


	threshold(src, src, 120,255,0);
	find_rect9(src, 200);
	//findContours(src, contours, 0, 0);
	imshow("0",src);
	waitKey(0);

	//system("pause");
	return 0;
}


