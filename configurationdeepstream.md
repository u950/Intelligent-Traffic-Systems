Here is the **README.md** file code for your GitHub repository that includes the installation instructions and necessary commands for setting up **DeepStream 6.0**:

```markdown
# DeepStream 6.0 Installation Guide

This repository provides a step-by-step guide to install NVIDIA DeepStream SDK 6.0 on a compatible system.

## Prerequisites

Before you begin, ensure your system meets the following requirements:
- Ubuntu 18.04 or Ubuntu 20.04
- NVIDIA GPU with CUDA support
- CUDA Toolkit (compatible with your GPU)
- TensorRT

You can check your CUDA and TensorRT versions by running the following commands:

```bash
nvcc --version
dpkg -l | grep TensorRT
```

## Step 1: Add NVIDIA DeepStream Repository

Add the necessary repositories to your system:

```bash
sudo add-apt-repository universe
sudo add-apt-repository multiverse
sudo add-apt-repository ppa:jonathonf/ffmpeg-4
sudo apt-get update
```

## Step 2: Install Dependencies

To install DeepStream, you need several dependencies. Run the following command to install all the required packages:

```bash
sudo apt-get install -y \
    libssl1.0.0 \
    libssl-dev \
    libcrypto++6 \
    libcrypto++-dev \
    libcurl4 \
    libopencv-dev \
    libcudnn8 \
    libnvinfer8 \
    libnvinfer-dev \
    libnvinfer-plugin8 \
    libnvparsers-dev \
    libnvparsers8 \
    python3 \
    python3-pip \
    python3-dev \
    python3-libnvinfer-dev \
    python3-libnvinfer \
    python3-numpy \
    python3-wheel \
    python3-setuptools \
    libgstrtspserver-1.0-0
```

## Step 3: Install DeepStream SDK

Once the dependencies are installed, you can install the DeepStream SDK by running the following command:

```bash
sudo apt-get install deepstream-6.0
```

## Step 4: Verification

After installation, verify that DeepStream has been installed correctly by checking the version:

```bash
deepstream-app --version
```

You should see the version of DeepStream installed on your system.

## Running Sample Application

Once DeepStream is installed, you can run the sample application to verify that everything is working correctly. Follow these steps:

1. Navigate to the sample apps directory:

    ```bash
    cd /opt/nvidia/deepstream/deepstream-6.0/sources/apps/sample
