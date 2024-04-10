#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int gray;
    for (int i = 0; i<height; i++)
    {
        for (int j = 0; j<width; j++)
        {
            gray = round( (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue)/(double)3.0);
            image[i][j].rgbtRed = gray;
            image[i][j].rgbtBlue = gray;
            image[i][j].rgbtGreen = gray;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed, sepiaBlue, sepiaGreen;
    RGBTRIPLE buffer[height][width];
    
    
    for (int i = 0; i<height; i++)
    {
        for (int j = 0; j<width; j++)
        {
            sepiaRed = round( 0.393*image[i][j].rgbtRed   + 0.769*image[i][j].rgbtGreen   +  0.189*image[i][j].rgbtBlue );
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            buffer[i][j].rgbtRed = sepiaRed;

            sepiaBlue = round( 0.272*image[i][j].rgbtRed   + 0.534*image[i][j].rgbtGreen   +  0.131*image[i][j].rgbtBlue );
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            buffer[i][j].rgbtBlue = sepiaBlue;


            sepiaGreen = round( 0.349*image[i][j].rgbtRed   + 0.686*image[i][j].rgbtGreen   +  0.168*image[i][j].rgbtBlue );
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            buffer[i][j].rgbtGreen = sepiaGreen;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = buffer[i][j];
        }
    }


    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE buffer[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            buffer[i][j] = image[i][width - j - 1];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = buffer[i][j];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{   
    float counter = 0;
    int blurRed = 0, blurGreen = 0, blurBlue = 0;
    RGBTRIPLE buffer[height][width];
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    if (((i+k >= 0) && (i+k <height ))  &&  ((j+l >= 0 ) && (j + l < width)))
                    {
                        blurRed = image[i+k][j+l].rgbtRed + blurRed;
                        blurGreen = image[i+k][j+l].rgbtGreen + blurGreen;
                        blurBlue = image[i+k][j+l].rgbtBlue + blurBlue;
                        counter++;
                    }
                }
            }
                buffer[i][j].rgbtRed = round(blurRed/counter);
                blurRed = 0;
                buffer[i][j].rgbtGreen = round(blurGreen/counter);
                blurGreen = 0;
                buffer[i][j].rgbtBlue = round(blurBlue/counter);
                blurBlue = 0;
                counter = 0;
        }
    }    
    
    
    for (int m = 0; m < height; m++)
    {
        for (int n = 0; n < width; n++)
        {
            image[m][n] = buffer[m][n];
        }
    }
    return;
}
