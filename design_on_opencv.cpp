#include<iostream>
using namespace std;
#include<opencv2/opencv.hpp>
using namespace cv;

void find_rect( Mat &src, int limit_value)
{
	threshold(src, src, limit_value, 255, THRESH_BINARY);

	int _width = src.cols;
	int _height = src.rows;
	int half_width = 0.5 * _width;
	int half_height = 0.5 * _height;

	int left_x = 0, left_y = 0;
	int right_x = 0, right_y = 0;
	int up_x = 0, up_y = 0;
	int down_x = half_width, down_y = _height;

	int left_flag = 0;
	int right_flag = 0;
	int up_flag = 0;
	int down_flag = 0;
	for (int i = half_width, j = half_height; i > 5; i -= 2)
	{
		int box_mean = (src.at<cv::Vec3b>(j - 1, i - 1)[0] + src.at<cv::Vec3b>(j - 1, i)[0] + src.at<cv::Vec3b>(j - 1, i + 1)[0] +
			src.at<cv::Vec3b>(j, i - 1)[0] + src.at<cv::Vec3b>(j, i)[0] + src.at<cv::Vec3b>(j, i + 1)[0] +
			src.at<cv::Vec3b>(j + 1, i - 1)[0] + src.at<cv::Vec3b>(j + 1, i)[0] + src.at<cv::Vec3b>(j + 1, i + 1)[0]) / 9;
		if ((box_mean > limit_value)&&(!left_flag))
		{
			printf("[%d,%d]", i, j); left_x = i; left_y = j;
			left_flag = 1;
		}		
	}

	for (int i = half_width, j = half_height; i < _width - 5; i += 2)
	{
		int box_mean = (src.at<cv::Vec3b>(j - 1, i - 1)[0] + src.at<cv::Vec3b>(j - 1, i)[0] + src.at<cv::Vec3b>(j - 1, i + 1)[0] +
			src.at<cv::Vec3b>(j, i - 1)[0] + src.at<cv::Vec3b>(j, i)[0] + src.at<cv::Vec3b>(j, i + 1)[0] +
			src.at<cv::Vec3b>(j + 1, i - 1)[0] + src.at<cv::Vec3b>(j + 1, i)[0] + src.at<cv::Vec3b>(j + 1, i + 1)[0]) / 9;
		if ((box_mean > limit_value)&&(!right_flag))
		{
			printf("[%d,%d]", i, j); right_x = i; right_y = j;
			right_flag = 1;
		}
			
	}

	for (int i = half_width, j = half_height; j > 5; j -= 2)
	{
		int box_mean = (src.at<cv::Vec3b>(j - 1, i - 1)[0] + src.at<cv::Vec3b>(j - 1, i)[0] + src.at<cv::Vec3b>(j - 1, i + 1)[0] +
			src.at<cv::Vec3b>(j, i - 1)[0] + src.at<cv::Vec3b>(j, i)[0] + src.at<cv::Vec3b>(j, i + 1)[0] +
			src.at<cv::Vec3b>(j + 1, i - 1)[0] + src.at<cv::Vec3b>(j + 1, i)[0] + src.at<cv::Vec3b>(j + 1, i + 1)[0]) / 9;
		if ((box_mean > limit_value) && (!up_flag))
		{
			printf("[%d,%d]", i, j); up_x = i; up_y = j;
			up_flag = 1;
		}		
	}

	for (int i = half_width, j = half_height; j < _height - 5; j += 2)
	{
		int box_mean = (src.at<cv::Vec3b>(j-1, i-1)[0] + src.at<cv::Vec3b>(j - 1, i)[0] + src.at<cv::Vec3b>(j - 1, i + 1)[0] +
			src.at<cv::Vec3b>(j, i-1)[0] + src.at<cv::Vec3b>(j, i)[0] + src.at<cv::Vec3b>(j, i + 1)[0] +
			src.at<cv::Vec3b>(j + 1, i - 1)[0] + src.at<cv::Vec3b>(j + 1, i)[0] + src.at<cv::Vec3b>(j + 1, i + 1)[0])/9;
		if ((box_mean > limit_value)&&(!down_flag))
		{
			printf("[%d,%d]", i, j); down_x = i; down_y = j;
			down_flag = 1;
		}
	}

	rectangle(src, Rect(left_x, up_y, right_x - left_x, down_y - up_y), Scalar(0, 255, 0), 3);
}




int main()
{
	Mat src = imread("demo.jpg");

	find_rect(src, 100);

	imshow("0",src);
	waitKey(0);

	return 0;
}


