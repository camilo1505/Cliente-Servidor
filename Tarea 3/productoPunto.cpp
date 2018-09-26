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
            if(matrix[i][j] == inf)
            {
                printf("inf \t");
            }
            else
            {
                printf("%i \t", matrix[i][j]);                
            }
        }
        printf("]\n");
    }
}

void point(int (&m1)[matrixSize][matrixSize], int (&m2)[matrixSize][matrixSize], int (&m3)[matrixSize][matrixSize])
{
    for(int i = 0; i < matrixSize; i++)
    {
        for(int j = 0; j < matrixSize; j++)
        {
            for(int k = 0; k < matrixSize; k++)
            {
                m3[i][j] += m1[i][k] * m2[k][j];
            }
        }
    }
}

int suma(int a, int b)
{
    if(a == inf)
    {
        return a;
    }
    if(b == inf)
    {
        return b;
    }
    else
    {
        return a+b;
    }
}

void pointStrange(int (&m1)[matrixSize][matrixSize], int (&m2)[matrixSize][matrixSize], int (&m3)[matrixSize][matrixSize])
{
    for(int i = 0; i < matrixSize; i++)
    {
        for(int j = 0; j < matrixSize; j++)
        {
            for(int k = 0; k < matrixSize; k++)
            {
                m3[i][j] = std::min( m3[i][j], suma(m1[i][k],m2[k][j]) );          
            }
        }
    }
}

void powStrange(int (&m1)[matrixSize][matrixSize], int (&matrixResul)[matrixSize][matrixSize], int pot)
{
    for(int i = 1; i <= pot; i++)
    {
        if(i == 1)
        {
            pointStrange(m1, m1, matrixResul);
        }
        else
        {
            pointStrange(matrixResul, m1, matrixResul);
        }
    }
}

int main()
{
    printf("Valor INF = %i \n", inf);
    int matrix[matrixSize][matrixSize]= { 
        0,6,inf,inf,inf,2,inf,inf,
        inf,0,inf,8,inf,2,inf,inf,
        1,inf,0,inf,inf,inf,inf,inf,
        inf,8,inf,0,inf,inf,inf,inf,
        inf,inf,inf,inf,0,inf,inf,inf,
        inf,inf,inf,inf,inf,0,3,inf,
        inf,inf,inf,inf,inf,inf,0,4,
        inf,inf,inf,inf,inf,5,inf,0
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

    //pointStrange(matrix, matrix, matrixResul);
    powStrange(matrix, matrixResul, matrixSize);
    printMatrix(matrixResul);

    return 0;
}