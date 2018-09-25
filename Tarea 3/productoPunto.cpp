#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<limits>
#include <algorithm>

const int inf = std::numeric_limits<int>::max();
const int matrixSize = 8;

void printMatrix(int (&matrix)[matrixSize][matrixSize])
{
    for(int i=0; i < matrixSize; i++)
    {
        printf("[");
        for(int j=0; j < matrixSize; j++)
        {
            printf("%i ", matrix[i][j]);
        }
        printf("]\n");
    }
}

void point(int (&m1)[matrixSize][matrixSize], int (&m2)[matrixSize][matrixSize], int (&m3)[matrixSize][matrixSize])
{
    for(int row = 0; row < matrixSize; row++)
    {
        for(int colA = 0; colA < matrixSize; colA++)
        {
            for(int colB = 0; colB < matrixSize; colB++)
            {
                m3[row][colA] += m1[row][colB] * m2[colB][colA];
            }
        }
    }
}

void pointStrange(int (&m1)[matrixSize][matrixSize], int (&m2)[matrixSize][matrixSize], int (&m3)[matrixSize][matrixSize])
{
    //printMatrix(m1);
    //printf("\n\n|||||||||||||||||||||||||||||||||||||||||||\n\n");
    //printMatrix(m2);
    //printf("\n\n|||||||||||||||||||||||||||||||||||||||||||\n\n");
    //printMatrix(m3);
    for(int row = 0; row < matrixSize; row++)
    {
        for(int colA = 0; colA < matrixSize; colA++)
        {
            for(int colB = 0; colB < matrixSize; colB++)
            {
                //printf("m3[%i][%i] = %i\n", row, colA, m3[row][colA]);
                //printf("min(%i, %i) = %i\n", m3[row][colA], m1[row][colB] + m2[colB][colA], std::min(m3[row][colA], m1[row][colB] + m2[colB][colA]));
                if(m1[row][colB] == inf and m2[colB][colA] == inf)
                {
                    m3[row][colA] = std::min(m3[row][colA], inf);
                }
                else
                {
                    m3[row][colA] = std::min(m3[row][colA], m1[row][colB] + m2[colB][colA]);
                }
                
            }
        }
    }
}

int main()
{
    printf("Valor INF = %i \n", inf);
    int matrix[matrixSize][matrixSize]= { 
        0,inf,5,inf,inf,inf,inf,inf,
        inf,0,8,inf,inf,inf,8,inf,
        inf,inf,0,inf,6,inf,inf,inf,
        inf,5,inf,0,inf,inf,inf,inf,
        inf,inf,1,inf,0,inf,1,8,
        inf,inf,inf,inf,inf,0,inf,inf,
        inf,inf,inf,inf,4,inf,0,inf,
        inf,inf,inf,inf,inf,inf,1,0
    };

    int matrixResul[matrixSize][matrixSize]= {
        inf,inf,inf,inf,inf,inf,inf,inf,
        inf,inf,inf,inf,inf,inf,inf,inf,
        inf,inf,inf,inf,inf,inf,inf,inf,
        inf,inf,inf,inf,inf,inf,inf,inf,
        inf,inf,inf,inf,inf,inf,inf,inf,
        inf,inf,inf,inf,inf,inf,inf,inf,
        inf,inf,inf,inf,inf,inf,inf,inf,
        inf,inf,inf,inf,inf,inf,inf,inf
    };

    pointStrange(matrix, matrix, matrixResul);
    printMatrix(matrixResul);

    return 0;
}