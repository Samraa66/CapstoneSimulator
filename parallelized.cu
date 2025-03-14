%%writefile sequential.cu

#define AND  0
#define OR   1
#define NAND 2
#define NOR  3
#define XOR  4
#define XNOR 5

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__global__ void evaluate_cuda(int* a,int* b, int* op,int* result, int N)
{
    int idx = threadIdx.x;
    if (idx < N)
    {
        if (op[idx] == AND)
            result[idx] = a[idx] && b[idx];
        else if (op[idx] == OR)
            result[idx] = a[idx] || b[idx];
        else if (op[idx] == NAND)
            result[idx] = !(a[idx] && b[idx]);
        else if (op[idx] == NOR)
            result[idx] = !(a[idx] || b[idx]);
        else if (op[idx] == XOR)
            result[idx] = (a[idx] || b[idx]) && !(a[idx] && b[idx]);
        else if (op[idx] == XNOR)
            result[idx] = (!a[idx] && !b[idx]) || (a[idx] && b[idx]);
    }
}


int main(int argc,char* argv[])
{
    if(argc !=4)
    {
        printf("Error: Invalid number of arguments.\n");
        return 1;
    }
    int N = atoi(argv[2]);
    char *inputFile = argv[1];
    char *outputFile = argv[3];

    // Allocate host memory
    int *hostA = (int*)malloc(N * sizeof(int));
    int *hostB = (int*)malloc(N * sizeof(int));
    int *hostOp = (int*)malloc(N * sizeof(int));
    int *hostResult = (int*)malloc(N * sizeof(int));

    // Read input file
    FILE *fp1 = fopen(inputFile, "r");
    if (!fp1) {
        perror("Error opening input file");
        return 1;
    }
    for (int i = 0; i < N; i++) {
        fscanf(fp1, "%d,%d,%d", &hostA[i], &hostB[i], &hostOp[i]);
    }
    fclose(fp1);

    // Allocate GPU memory
    int *gpuA, *gpuB, *gpuOp, *gpuResult;
    cudaMalloc((void**)&gpuA, N * sizeof(int));
    cudaMalloc((void**)&gpuB, N * sizeof(int));
    cudaMalloc((void**)&gpuOp, N * sizeof(int));
    cudaMalloc((void**)&gpuResult, N * sizeof(int));

    // Copy data from host to GPU
    cudaMemcpy(gpuA, hostA, N * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(gpuB, hostB, N * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(gpuOp, hostOp, N * sizeof(int), cudaMemcpyHostToDevice);

    int blockSize = 256; // Standard CUDA block size
    int gridSize = (N + blockSize - 1) / blockSize;
    // Launch kernel with N threads (1 per operation)
    evaluate_cuda<<<gridSize, blockSize>>>(gpuA, gpuB, gpuOp, gpuResult, N);
     cudaDeviceSynchronize();

    // Check for CUDA errors
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        printf("CUDA Error: %s\n", cudaGetErrorString(err));
    }
    // Copy result from GPU to host
    cudaMemcpy(hostResult, gpuResult, N * sizeof(int), cudaMemcpyDeviceToHost);
    FILE *fp2 = fopen(outputFile, "w");
    if (!fp2) {
        perror("Error opening output file");
        return 1;
    }
    for (int i = 0; i < N; i++) {
        fprintf(fp2, "%d\n", hostResult[i]);
    }
    fclose(fp2);
    free(hostA); free(hostB); free(hostOp); free(hostResult);
    cudaFree(gpuA); cudaFree(gpuB); cudaFree(gpuOp); cudaFree(gpuResult);

    return 0;
}


